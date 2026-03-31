import json
from types import SimpleNamespace

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f, object_hook=lambda d: SimpleNamespace(**d))

config = load_config()