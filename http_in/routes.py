from fastapi import APIRouter, Body, HTTPException
from path_resolver import get_decoder
from decoder import decodePayload

router = APIRouter()

@router.post('/{path:path}')
async def default_path(path: str, payload: dict):
  if len(path) > 0:
    try:
      decoder = get_decoder(path)
      decoded = decodePayload(decoder, payload)
      return {'decoded': decoded}
    except Exception as e:
      raise HTTPException(status_code=400, detail=f'Bad request')
