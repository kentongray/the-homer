import os

import broadlink
import time

import sys

devices = broadlink.discover(timeout=5)
devices[0].auth()
devices[0].enter_learning()
command = sys.argv[1]
print("hit the button on the remote", command)
time.sleep(5)
ir_packet = devices[0].check_data()
print("got packet writing file", command, ir_packet)

# record learned code to file
f = open(os.path.relpath('broadlink-codes/', command + '.ir'), 'w')
f.write(str(ir_packet))
f.close()