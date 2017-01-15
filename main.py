import logging

import server
from dream_machine import DreamMachine

logging.basicConfig()

cfg = None
try:
    import config
    cfg = config
except:
    print("no config found, see ReadMe for setup instructions")


dream_machine = DreamMachine(cfg)
server.run(dream_machine)
