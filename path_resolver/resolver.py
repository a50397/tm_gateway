
_paths = {}

def add_path(path: str, decoder: str):
  if not path or not decoder:
    raise ValueError("Add path: missing path or decoder")
  _paths[path] = decoder

def remove_path(path: str):
  if not path:
    raise ValueError("Remove path: missing path")
  if path in _paths:
    del _paths[path]

def get_decoder(path: str) -> str:
  if not path:
    raise ValueError("Get decoder: missing path")
  if path not in _paths:
    raise ValueError("Get decoder: unknown path")
  return _paths[path]

__all__ = ["add_path", "remove_path", "get_decoder"]
