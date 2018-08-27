import time
import sys
from os.path import normpath, basename, splitext
import midi
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

class MusicPlayer:
    song_name = ""
    midi_data = {}
    midi_time_data = {}
    end_time = 0
    tick_delays = {}
    
    midi_mapping = {
    21: "A0",
    22: "A0+",
    23: "B0",
    24: "C1",
    25: "C1+",
    26: "D1",
    27: "D1+",
    28: "E1",
    29: "F1",
    30: "F1+",
    31: "G1",
    32: "G1+",
    33: "A1",
    34: "A1+",
    35: "B1",
    36: "C2",
    37: "C2+",
    38: "D2",
    39: "D2+",
    40: "E2",
    41: "F2",
    42: "F2+",
    43: "G2",
    44: "G2+",
    45: "A2",
    46: "A2+",
    47: "B2",
    48: "C3",
    49: "C3+",
    50: "D3",
    51: "D3+",
    52: "E3",
    53: "F3",
    54: "F3+",
    55: "G3",
    56: "G3+",
    57: "A3",
    58: "A3+",
    59: "B3",
    60: "C4",
    61: "C4+",
    62: "D4",
    63: "D4+",
    64: "E4",
    65: "F4",
    66: "F4+",
    67: "G4",
    68: "G4+",
    69: "A4",
    70: "A4+",
    71: "B4",
    72: "C5",
    73: "C5+",
    74: "D5",
    75: "D5+",
    76: "E5",
    77: "F5",
    78: "F5+",
    79: "G5",
    80: "G5+",
    81: "A5",
    82: "A5+",
    83: "B5",
    84: "C6",
    85: "C6+",
    86: "D6",
    87: "D6+",
    88: "E6",
    89: "F6",
    90: "F6+",
    91: "G6",
    92: "G6+",
    93: "A6",
    94: "A6+",
    95: "B6",
    96: "C7",
    97: "C7+",
    98: "D7",
    99: "D7+",
    100: "E7",
    101: "F7",
    102: "F7+",
    103: "G7",
    104: "G7+",
    105: "A7",
    106: "A7+",
    107: "B7",
    108: "C8"
    }
    
    osc_key_states = {
    "A0" : 0,
    "A0+" : 0,
    "B0" : 0,
    "C1" : 0,
    "C1+" : 0,
    "D1" : 0,
    "D1+" : 0,
    "E1" : 0,
    "F1" : 0,
    "F1+" : 0,
    "G1" : 0,
    "G1+" : 0,
    "A1" : 0,
    "A1+" : 0,
    "B1" : 0,
    "C2" : 0,
    "C2+" : 0,
    "D2" : 0,
    "D2+" : 0,
    "E2" : 0,
    "F2" : 0,
    "F2+" : 0,
    "G2" : 0,
    "G2+" : 0,
    "A2" : 0,
    "A2+" : 0,
    "B2" : 0,
    "C3" : 0,
    "C3+" : 0,
    "D3" : 0,
    "D3+" : 0,
    "E3" : 0,
    "F3" : 0,
    "F3+" : 0,
    "G3" : 0,
    "G3+" : 0,
    "A3" : 0,
    "A3+" : 0,
    "B3" : 0,
    "C4" : 0,
    "C4+" : 0,
    "D4" : 0,
    "D4+" : 0,
    "E4" : 0,
    "F4" : 0,
    "F4+" : 0,
    "G4" : 0,
    "G4+" : 0,
    "A4" : 0,
    "A4+" : 0,
    "B4" : 0,
    "C5" : 0,
    "C5+" : 0,
    "D5" : 0,
    "D5+" : 0,
    "E5" : 0,
    "F5" : 0,
    "F5+" : 0,
    "G5" : 0,
    "G5+" : 0,
    "A5" : 0,
    "A5+" : 0,
    "B5" : 0,
    "C6" : 0,
    "C6+" : 0,
    "D6" : 0,
    "D6+" : 0,
    "E6" : 0,
    "F6" : 0,
    "F6+" : 0,
    "G6" : 0,
    "G6+" : 0,
    "A6" : 0,
    "A6+" : 0,
    "B6" : 0,
    "C7" : 0,
    "C7+" : 0,
    "D7" : 0,
    "D7+" : 0,
    "E7" : 0,
    "F7" : 0,
    "F7+" : 0,
    "G7" : 0,
    "G7+" : 0,
    "A7" : 0,
    "A7+" : 0,
    "B7" : 0,
    "C8" : 0
    }

    def setup_osc(self):
        #parser = argparse.ArgumentParser()
        #parser.add_argument("--ip", default="127.0.0.1",
        #    help="The ip of the OSC server")
        #parser.add_argument("--port", type=int, default=9000,
        #    help="The port the OSC server is listening on")
        #args = parser.parse_args()
        #
        #client = udp_client.SimpleUDPClient(args.ip, args.port)
        client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        return client
    
    def press_osc(self, key_name):
        try:
            piano_key = self.adjusted_key_mapping[key_name]
        except:
            piano_key = key_name
        try:
            self.osc_key_states[piano_key] = 1 - self.osc_key_states[piano_key]
            state = self.osc_key_states[piano_key]
            #print("/PianoKeys/"+piano_key)
            #print(state)
            self.client.send_message("/PianoKeys/"+piano_key, state)
        except:
            print("Invalid Key: " + piano_key)
            return

    def clear_osc(self):
        self.client.send_message("/PianoKeys/OSCDisable", 1)
        time.sleep(0.5)
        for piano_key in self.midi_mapping.values():
            self.client.send_message("/PianoKeys/"+piano_key, 0)
        time.sleep(0.5)
        self.client.send_message("/PianoKeys/OSCDisable", 0)
        self.osc_key_states = {key: 0 for key in self.osc_key_states}

    def set_tick_delays(self, pattern):
        # Default tempo
        tempo = 500000
        tick_delay = tempo / pattern.resolution
        tick_delay /= 1000
        self.tick_delays = {0: tick_delay}
        instrument = 0
        for x in pattern:
            instrument += 1
            time = 0
            for y in x:
                try:
                    if pattern.tick_relative:
                        time += y.tick
                    else:
                        time = y.tick
                except:
                    continue
                if y.name == "Set Tempo":
                    tempo = (y.data[0] << 16) + (y.data[1] << 8) + y.data[2]
                    tick_delay = tempo / pattern.resolution
                    tick_delay /= 1000
                    self.tick_delays[int(time/10)] = tick_delay

    def generate_midi_data(self, midifile):
        self.song_name = splitext(basename(normpath(midifile)))[0]
        self.midi_data = {}
        self.midi_time_data = {}
        pattern = midi.read_midifile(midifile)
        self.set_tick_delays(pattern)
        instrument = 0
        self.end_time = 0
        for x in pattern:
            instrument += 1
            tick_time = 0
            for y in x:
                try:
                    tick_time += y.tick
                except:
                    pass
                if y.name == "Note On":
                    try:
                        # data = [key, velocity]
                        # velocity = strength note is pressed
                        # 0 means not pressed
                        # Run if note is ON (pressed)
                        if y.data[1] > 0:
                            time = int(tick_time / 10)
                            if time not in self.midi_data.keys():
                                self.midi_data[time] = []
                            self.midi_data[time].append(self.midi_mapping[y.data[0]])
                            if time > self.end_time:
                                self.end_time = time
                    except:
                        pass

        # Time data
        tick_delay = 0
        tick_delay_index = 0
        midi_time = 0
        self.midi_time_data = {}
        for i in range(self.end_time+1):
            if i in self.tick_delays.keys():
                tick_delay = self.tick_delays[i]
            if i in self.midi_data.keys():
                key_names = self.midi_data[i]
                approx_midi_time = int(midi_time)
                self.midi_time_data[approx_midi_time] = key_names
            midi_time += tick_delay

    def play_midi_data(self):
        print("Now Playing: " + self.song_name)
        print("Press Ctrl+C to stop")

        tick_delay = 0.0
        self.client = self.setup_osc()
        self.clear_osc()
        for i in range(self.end_time+1):
            if i in self.tick_delays.keys():
                tick_delay = self.tick_delays[i]
            if i in self.midi_data.keys():
                key_names = self.midi_data[i]
                for key_name in key_names:
                    self.press_osc(key_name)
            # 0.001 is the press time delay
            sleep_time = (tick_delay/100) - 0.001
            if sleep_time < 0:
                sleep_time = 0
            time.sleep(sleep_time)

    def play_midi(self, midifile):
        self.generate_midi_data(midifile)
        self.play_midi_data()
        





