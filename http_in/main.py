from fastapi import FastAPI
import logging
from http_in.routes import router
from path_resolver import add_path

logging.basicConfig()
logging.getLogger('tmgw_http').setLevel('DEBUG')

tmgw_http = FastAPI()

@tmgw_http.on_event('startup')
async def startup():
  pass

@tmgw_http.on_event('shutdown')
async def shutdown():
  pass

tmgw_http.include_router(router, prefix='/in')
