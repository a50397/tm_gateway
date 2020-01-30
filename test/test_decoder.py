from decoder import decodePayload
from pydantic import ValidationError
import unittest

data = [
  { "device": "367EEF",
     "provider": "sigfox",
     "seqNumber": "2440",
     "time": 1538731834,
     "snr": 23.97,
     "data": "14b6b8e622262e8408000000" },
   { "device": "367EEF",
     "provider": "orange",
    "seqNumber": "0",
    "time": 1538731802,
    "snr": 5,
    "data": "11bba6ce02b6700500268000" },
  { "device": "367EEF",
    "provider": "sigfox",
    "seqNumber": "3024",
    "time": 1538731853,
    "snr": 9.8,
    "data": "14b6f8be2726306b0d800000",
    "additional":"whatever"
  },
  { "provider": "sigfox",
    "seqNumber": "3024",
    "time": 1538731853,
    "snr": 9.8,
    "data": "14b6f8be2726306b0d800000"
  } 
]

class decoder_test(unittest.TestCase):

  def test_decode_existing(self):
    decoded = decodePayload("MeteoHelix IoT", data[0])
    self.assertEqual(decoded['deviceId'], "367EEF")
    self.assertEqual(decoded['Pressure'], 56105)

  def test_decode_missing(self):
    with self.assertRaises(ValueError):
      decoded = decodePayload("Unknown device", data[0])
  
  def test_device_missing(self):
    with self.assertRaises(ValidationError):
      decoded = decodePayload("MeteoHelix IoT", data[3])
  
  def test_additional_data_ignored(self):
    decoded = decodePayload("MeteoHelix IoT", data[2])
    self.assertNotIn('addidional', decoded)

if __name__ == '__main__':
    unittest.main()