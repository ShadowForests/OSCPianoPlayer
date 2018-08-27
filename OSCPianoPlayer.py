import MusicPlayerOSC as mp
import argparse
import time
import sys

#parser.add_argument("--midi", default="",
#    help="The midi file to play")
        
musicPlayer = mp.MusicPlayer()
try:
    song_test = sys.argv[1]
except:
    print("OSCPianoPlayer v.1.0 by ShadowForest")
    print("Source: https://github.com/ShadowForests/OSCPianoPlayer")
    print("----------------------------------------------")
    print("Note: Please only play one song at a time, and don't play if someone else is playing!")
    print("      Don't play song animations in game while a song is playing!")
    print("")
    print("Usage:")
    print(" 1. First, launch VRChat and visit the Self-Playing Piano [MIDI/OSC] world, by ShadowForest.")
    print(" 2. Next, download a midi file (.mid). It is recommended to use a song written for piano.")
    print("    If you need help finding midis, you can add 'piano' and/or 'midi' while searching.")
    print("    Alternatively, visit musescore.com, flat.io, or other sheet music sites with midi downloads.")
    print(" 3. Drag the midi file into this console, and the file path will be pasted, then hit enter.")
    print(" 4. Watch and listen to the piano play itself!")
    print(" 5. Press Ctrl+C in this console to stop the current song.")
    print(" 6. You can also directly drag and drop a midi onto the exe file to play a single song.")
    while True:
        try:
            print("----------------------------------------------")
            midifile = input("Drop midi file here and hit enter: ")
            try:
                musicPlayer.play_midi(midifile)
                print("Finished playing.")
            except KeyboardInterrupt:
                print("Stopped song.")
        except KeyboardInterrupt:
            print("\nShutting down...")
            time.sleep(0.25)
            sys.exit()
        except EOFError:
            try:
                time.sleep(0.25)
            except:
                print("\nShutting down...")
                time.sleep(0.25)
                sys.exit()
        except Exception as e:
            print(e)
            print("Error: Invalid midi file, try again")
try:
    musicPlayer.play_midi(sys.argv[1])
    print("Finished playing.")
except:
    print("Stopped song.")
print("Shutting down...")
time.sleep(0.25)
sys.exit()
    






