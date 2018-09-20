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

    # Midi instrument and percussion list
    # https://www.midi.org/specifications-old/item/gm-level-1-sound-set

    instruments = {
    1: "Acoustic Grand Piano",
    2: "Bright Acoustic Piano",
    3: "Electric Grand Piano",
    4: "Honky-tonk Piano",
    5: "Electric Piano 1",
    6: "Electric Piano 2",
    7: "Harpsichord",
    8: "Clavi",
    9: "Celesta",
    10: "Glockenspiel",
    11: "Music Box",
    12: "Vibraphone",
    13: "Marimba",
    14: "Xylophone",
    15: "Tubular Bells",
    16: "Dulcimer",
    17: "Drawbar Organ",
    18: "Percussive Organ",
    19: "Rock Organ",
    20: "Church Organ",
    21: "Reed Organ",
    22: "Accordion",
    23: "Harmonica",
    24: "Tango Accordion",
    25: "Acoustic Guitar (nylon)",
    26: "Acoustic Guitar (steel)",
    27: "Electric Guitar (jazz)",
    28: "Electric Guitar (clean)",
    29: "Electric Guitar (muted)",
    30: "Overdriven Guitar",
    31: "Distortion Guitar",
    32: "Guitar harmonics",
    33: "Acoustic Bass",
    34: "Electric Bass (finger)",
    35: "Electric Bass (pick)",
    36: "Fretless Bass",
    37: "Slap Bass 1",
    38: "Slap Bass 2",
    39: "Synth Bass 1",
    40: "Synth Bass 2",
    41: "Violin",
    42: "Viola",
    43: "Cello",
    44: "Contrabass",
    45: "Tremolo Strings",
    46: "Pizzicato Strings",
    47: "Orchestral Harp",
    48: "Timpani",
    49: "String Ensemble 1",
    50: "String Ensemble 2",
    51: "SynthStrings 1",
    52: "SynthStrings 2",
    53: "Choir Aahs",
    54: "Voice Oohs",
    55: "Synth Voice",
    56: "Orchestra Hit",
    57: "Trumpet",
    58: "Trombone",
    59: "Tuba",
    60: "Muted Trumpet",
    61: "French Horn",
    62: "Brass Section",
    63: "SynthBrass 1",
    64: "SynthBrass 2",
    65: "Soprano Sax",
    66: "Alto Sax",
    67: "Tenor Sax",
    68: "Baritone Sax",
    69: "Oboe",
    70: "English Horn",
    71: "Bassoon",
    72: "Clarinet",
    73: "Piccolo",
    74: "Flute",
    75: "Recorder",
    76: "Pan Flute",
    77: "Blown Bottle",
    78: "Shakuhachi",
    79: "Whistle",
    80: "Ocarina",
    81: "Lead 1 (square)",
    82: "Lead 2 (sawtooth)",
    83: "Lead 3 (calliope)",
    84: "Lead 4 (chiff)",
    85: "Lead 5 (charang)",
    86: "Lead 6 (voice)",
    87: "Lead 7 (fifths)",
    88: "Lead 8 (bass + lead)",
    89: "Pad 1 (new age)",
    90: "Pad 2 (warm)",
    91: "Pad 3 (polysynth)",
    92: "Pad 4 (choir)",
    93: "Pad 5 (bowed)",
    94: "Pad 6 (metallic)",
    95: "Pad 7 (halo)",
    96: "Pad 8 (sweep)",
    97: "FX 1 (rain)",
    98: "FX 2 (soundtrack)",
    99: "FX 3 (crystal)",
    100: "FX 4 (atmosphere)",
    101: "FX 5 (brightness)",
    102: "FX 6 (goblins)",
    103: "FX 7 (echoes)",
    104: "FX 8 (sci-fi)",
    105: "Sitar",
    106: "Banjo",
    107: "Shamisen",
    108: "Koto",
    109: "Kalimba",
    110: "Bag pipe",
    111: "Fiddle",
    112: "Shanai",
    113: "Tinkle Bell",
    114: "Agogo",
    115: "Steel Drums",
    116: "Woodblock",
    117: "Taiko Drum",
    118: "Melodic Tom",
    119: "Synth Drum",
    120: "Reverse Cymbal",
    121: "Guitar Fret Noise",
    122: "Breath Noise",
    123: "Seashore",
    124: "Bird Tweet",
    125: "Telephone Ring",
    126: "Helicopter",
    127: "Applause",
    128: "Gunshot",
    }

    percussion = {
    35: "Acoustic Bass Drum",
    36: "Bass Drum 1",
    37: "Side Stick",
    38: "Acoustic Snare",
    39: "Hand Clap",
    40: "Electric Snare",
    41: "Low Floor Tom",
    42: "Closed Hi Hat",
    43: "High Floor Tom",
    44: "Pedal Hi-Hat",
    45: "Low Tom",
    46: "Open Hi-Hat",
    47: "Low-Mid Tom",
    48: "Hi-Mid Tom",
    49: "Crash Cymbal 1",
    50: "High Tom",
    51: "Ride Cymbal 1",
    52: "Chinese Cymbal",
    53: "Ride Bell",
    54: "Tambourine",
    55: "Splash Cymbal",
    56: "Cowbell",
    57: "Crash Cymbal 2",
    58: "Vibraslap",
    59: "Ride Cymbal 2",
    60: "Hi Bongo",
    61: "Low Bongo",
    62: "Mute Hi Conga",
    63: "Open Hi Conga",
    64: "Low Conga",
    65: "High Timbale",
    66: "Low Timbale",
    67: "High Agogo",
    68: "Low Agogo",
    69: "Cabasa",
    70: "Maracas",
    71: "Short Whistle",
    72: "Long Whistle",
    73: "Short Guiro",
    74: "Long Guiro",
    75: "Claves",
    76: "Hi Wood Block",
    77: "Low Wood Block",
    78: "Mute Cuica",
    79: "Open Cuica",
    80: "Mute Triangle",
    81: "Open Triangle",
    }

    percussive_instruments = []
    #percussive_instruments += [i for i in range(25,30)]
    percussive_instruments += [i for i in range(113,129)]
    
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

    def generate_midi_data(self, midifile, instrument_name):
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
            check_notes = True
            for y in x:
                # Increment time
                try:
                    tick_time += y.tick
                except:
                    pass

                # Check and skip non-piano notes
                if y.name == "Program Change" and instrument_name == "piano_solo":
                    if y.channel == 9:
                        try:
                            print("Skipping instrument: " + self.percussion[y.data[0]+1])
                        except:
                            print("Skipping instrument: unknown")
                        # Percussion channel
                        check_notes = False
                    elif y.data[0]+1 in self.percussive_instruments:
                        try:
                            print("Skipping instrument: " + self.instruments[y.data[0]+1])
                        except:
                            print("Skipping instrument: unknown")
                        check_notes = False
                        # TODO: Add future check for non-piano instruments?
                        #print("P", str(y.channel+1), str(y.data[0]+1), instruments[y.data[0]+1])
                    else:
                        check_notes = True

                # Check for note presses
                if y.name == "Note On" and check_notes:
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

    def play_midi(self, midifile, instrument_name):
        self.generate_midi_data(midifile, instrument_name)
        self.play_midi_data()
        





