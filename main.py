import logging

import server
from dream_machine import DreamMachine

logging.basicConfig()


dream_machine = DreamMachine()
server.run(dream_machine)
