from typing import List, Dict, AnyStr, Set
from datetime import datetime
import time
from operator import itemgetter
from pydantic import create_model
from mapper.object_mapper import ObjectMapper
from bitstring import BitArray

from os import getcwd, walk
from os.path import join
import json

import logging

logging.basicConfig()
logger = logging.getLogger('tmgw_decoder')
logger.setLevel('DEBUG')

__all__ = ["decodePayload", "addDefinition"]

decoders = {}

class TM_decoder():
  _dataTypes = {
    'str': AnyStr,
    'int': int,
    'float': float,
    'datetime': datetime,
    'object': Dict,
    'array': List,
    'dict': Dict,
    'set': Set
  }

  _functions = {
      'add': lambda a, b: a + b,
      'mul': lambda a, b: a * b,
      'pow': lambda a, b: a ** b,
      'app': lambda a, b: a + b,
      'pre': lambda a, b: b + a,
      'ubin': lambda data, limits: data[limits[0] : limits[1]].uint,
      'bin': lambda data, limits: data[limits[0] : limits[1]].int,
  }

  class _DictToObject(object):
      def __init__(self, dictionary, name = None):
        def _traverse(key, element):
          if isinstance(element, dict) and '_tm_type' not in element and '_tm_field' not in element:
            return key, _DictToObject(element)
          elif isinstance(element, dict) and ('_tm_type' in element or '_tm_field' in element):
            return key,''
          else:
            return key, element

        objd = dict(_traverse(k, v) for k, v in dictionary.items())
        self.__dict__.update(objd)
        if name:
          self.__class__.__name__ = name
    
  def __init__(self, name: str, definition: Dict):
    try:
      self.name = name  
      self._definition = definition
      decoder, modifiers = itemgetter('decoder', 'modifiers')(self._definition)
    except KeyError as e:
      logger.debug('Bad decoder structure')
      raise ValueError('Bad decoder structure')
    self._inputChecker = self._create_decoder(decoder)
    self._decoder = self._create_translator(decoder, modifiers)

  def decode(self, reading: dict):
    try:
      check = self._inputChecker.validate(reading)
      readingObject = self.__class__._DictToObject(reading)
      decoded = self._decoder.map(readingObject, allow_unmapped=True)
      return decoded.__dict__
    except Exception as e:
      logger.debug(f'Decode exception {e}')
      raise e

  def _parseModFns(self, modifiers: dict) -> dict:
    
    def modFn(field: str, functionList: List[object]):
      '''Return modification function'''
      def inner(data: object):
        fns = self.__class__._functions

        if len(list(filter(lambda d: d['func'].count('bin') > 0, functionList))) > 0:
          value = BitArray('0x' + data.__getattribute__(field))
        else:
          value = data.__getattribute__(field)
        for mod in functionList:
          try:
            value = fns[mod['func']](value, mod['value']) if mod['func'] in fns else value        
          except Exception as e:
            logger.debug(f'Modifier exception {e}')
            pass
        if isinstance(value, float):
          value = round(value, 5)
        return value 
      return inner

    output = {}
    for field in modifiers:
      output[field] = modFn(modifiers[field].get("_tm_field"), modifiers[field].get("mods", []))

    return output

  def _create_translator(self, decoder: dict, modifiers: dict):
    destinationClass = type('outputClass', (object,), modifiers)
    sourceObject = self.__class__._DictToObject(decoder)
    mapper = ObjectMapper()
    modFns = self._parseModFns(modifiers)
    mapper.create_map(sourceObject.__class__, destinationClass, modFns)
    return mapper
  
  def _create_type(self, field: str):
    tfield = self.__class__._dataTypes[field.get('_tm_type', 'str')]
    tdefault = field.get('default', Ellipsis)
    return (tfield, tdefault)
  
  def _create_decoder(self, decoder: dict):
    keys = decoder.keys()
    fields = list(map(lambda field: self._create_type(decoder[field]), keys))
    decoderDict = dict(zip(keys, fields))
    try:
      model = create_model(self.name, **decoderDict)
    except Exception as e:
      logger.debug(f'Decoder creation exception {e}')
      raise e
    return model

# INITIALIZE BUILT-IN DEVICE DEFINITIONS

def loadBuiltinDefinitions():
  currdir = join(getcwd(), 'decoder', 'device_definitions')
  for _, _, files in walk(currdir):
    for f in files:
      with open(join(currdir, f)) as json_file:
        try:
          data = json.load(json_file)
          for device in data:
            decoders[device] = TM_decoder(device, data[device])
        except Exception as e:
          logger.debug(f'Built-in decoder loading exception {e}')
          pass

def addDefinition(definitions: dict):
  for device in definitions:
    if isinstance(definitions[device], dict) and \
       isinstance(definitions[device].get('decoder'), dict) and \
       isinstance(definitions[device].get('modifiers'), dict):
      decoders[device] = TM_decoder(device, definitions[device])

def decodePayload(deviceType: str, payload: dict) -> dict:
  if len(decoders) == 0:
    loadBuiltinDefinitions()
  if deviceType in decoders and isinstance(payload, dict):
    return decoders[deviceType].decode(payload)
  else:
    logger.debug(f'Device type {deviceType} not found in decoders')
    raise ValueError(f'Device type {deviceType} not found in decoders')