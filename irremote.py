import time
from enum import Enum, IntEnum
from math import fabs

from gpiozero import DigitalInputDevice

from util import list_right_index, thread_it


class Command(IntEnum):
    Power = 209
    Mode = 177
    Mute = 241
    Play = 145
    Back = 129
    Forward = 225
    Eq = 240
    Down = 212
    Shuffle = 204
    Weird_Button = 216
    Up = 200
    Zero = 180
    One = 152
    Two = 140
    Three = 189
    Four = 136
    Five = 156
    Six = 173
    Seven = 161
    Eight = 165
    Nine = 169


class PulseType(Enum):
    Start = (9, 4.5)
    One = (.56, 1.69)
    Zero = (.56, .56)
    Mystery = (0, 10000)  # a wild pulse has appeared

    @staticmethod
    def find_type(pulse_length_ms, pause_after_pulse_ms, tolerance_ms=.2):
        def within_tolerance(x, y):
            return fabs(x - y) < tolerance_ms

        for type in PulseType:
            t = type.value
            if within_tolerance(t[0], pulse_length_ms) and within_tolerance(t[1], pause_after_pulse_ms):
                return type
        return PulseType.Mystery


# Handles NEC remote standard
# http://www.sbprojects.com/knowledge/ir/nec.php
class IrRemote:
    def __init__(self, pin=20, when_pressed=lambda: None):

        self.last_pulse_end = None  # time the last pulse stopped at
        self.last_pulse_duration = None  # how long was the last pulse
        self.when_pressed = when_pressed
        self.input = DigitalInputDevice(pin, pull_up=True)
        #        self.queue = GPIOQueue(self.input, 1)
        #        self.queue.start()

        self.pulses = []
        self.current_val = False
        self.last_time = time.time()
        self.start_pulse_time = None
        self.in_pulse = False
        thread_it(lambda: self.watch_ir())

    # basically a state machine to watch the pulses
    def watch_ir(self):

        while True:
            # everything inside here needs to be ridiculously fast
            # or you cause latency which messes up measurements
            current_time = time.time()
            self.last_time = current_time
            state = self.input.value

            def pulse_start():
                self.start_pulse_time = current_time
                # check if we had a preceding pulse
                # if self.last_pulse_end is not None:
                #    create_pulse()
                #    self.last_pulse_duration = None

            def create_pulse():
                # uncomment for raw ir feed
                # print(self.last_pulse_duration, (current_time - self.last_pulse_end) * 1000)
                pulse_type = PulseType.find_type(self.last_pulse_duration, (current_time - self.last_pulse_end) * 1000)
                self.pulses.append(pulse_type)

            def pulse_end():
                self.last_pulse_duration = (current_time - self.start_pulse_time) * 1000
                self.start_pulse_time = None
                self.last_pulse_end = current_time

            # after we haven't heard anything in a bit call this
            def end_of_pulses():
                create_pulse()
                self.start_pulse_time = None
                self.last_pulse_end = None
                emit_command()

            def emit_command():
                def type_to_str(p):
                    if p is PulseType.One:
                        return "1"
                    else:
                        return "0"

                try:
                    self.pulses = list(filter(lambda i: i is not PulseType.Mystery, self.pulses))
                    if len(self.pulses) <= 0:
                        # it was all junk
                        return
                    elif len(self.pulses) < 32:
                        print("partial ir heard, ignoring, pulses:", self.pulses)
                        return

                    # trim off anything before the start pulse
                    try:
                        i = list_right_index(self.pulses, PulseType.Start)
                    except:
                        return

                    self.pulses = self.pulses[i:]
                    bits = ''.join(list(map(type_to_str, self.pulses[16:][:8])))
                    code = int(bits, 2)
                    try:
                        command = Command(code)
                    except:
                        print("Invalid command code, ignoring", code)
                        return
                    # split into a separate thread to make sure we can continue reading quickly!
                    thread_it(lambda: self.when_pressed(command))
                except:
                    print("In IR land something strange happened (prob ufos)", self.pulses)
                finally:
                    self.pulses = []

            if state is False and self.last_pulse_end is not None and (current_time - self.last_pulse_end) > .3:
                end_of_pulses()
            if state and self.start_pulse_time is None:
                pulse_start()
            elif state is False and self.start_pulse_time is not None:
                pulse_end()
