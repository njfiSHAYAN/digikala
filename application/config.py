import os
import json

CONFIG_FILE = os.getenv("CONFIG_ADDR", "application/config.json")


CONFIG_DATA = json.load(open(CONFIG_FILE))
