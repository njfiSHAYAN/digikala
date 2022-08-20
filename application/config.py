import os
import json

CONFIG_FILE = os.getenv('CONFIG_ADDR', 'conf.json')

CONFIG_DATA = json.load(open(CONFIG_FILE))

