import mido
import time
import requests
import argparse
import glob
import os

def main(midiFileName):
    midifile = mido.MidiFile(f'midifiles/{midiFileName}', clip=True)
    mod = 5
    midi_port = "Microsoft GS Wavetable Synth 0"

    # Shelly to note mapping. Make sure to have the same ammount of shellys as you have defined for the modolus (mod)
    # Note Number : Shelly IP : Relay 
    shellyNoteMapping = {
        100: ["192.168.2.142", "0", "note_off"], 
        101: ["192.168.2.141", "0", "note_off"], 
        102: ["192.168.2.138", "0", "note_off"], 
        103: ["192.168.2.167", "1", "note_off"], # Shelly 2.5 Example
        104: ["192.168.2.139", "0", "note_off"],
    }

    on_off_Mapping = {
        "note_on" : "on",
        "note_off" : "off"
    }

    print("Preping light show. Turn off all Shellys....")
    for shelly in shellyNoteMapping:
        print(f"http://{shellyNoteMapping[shelly][0]}/relay/{shellyNoteMapping[shelly][1]}?turn=off")
        r = requests.get(f"http://{shellyNoteMapping[shelly][0]}/relay/{shellyNoteMapping[shelly][1]}?turn=off")


    with mido.open_output(midi_port) as output:
        try:
            t0 = time.time()
            for message in midifile.play():
                output.send(message)
                if message.type in ["note_on", "note_off"]:
                    note = (message.note%mod) + 100
                    
                    if message.type != shellyNoteMapping[note][2]:
                        shellyNoteMapping[note][2] = message.type
                        print(f"{note}  -   {message.type}      http://{shellyNoteMapping[note][0]}/relay/{shellyNoteMapping[note][1]}?turn={on_off_Mapping[message.type]}")
                        r = requests.get(f"http://{shellyNoteMapping[note][0]}/relay/{shellyNoteMapping[note][1]}?turn={on_off_Mapping[message.type]}")
            
            print('play time: {:.2f} s (expected {:.2f})'.format(
                time.time() - t0, midifile.length))
        except KeyboardInterrupt:
            print()
            output.reset()


def scanFiles():
    for file in glob.glob("midifiles/*.mid"):
        print(os.path.basename(file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Add more options if you like
    parser.add_argument(
        "--song",
        dest="midiFileName",
        help="Midi File",
        metavar="FILE",
    )
    parser.add_argument(
        "--files",
        dest="files",
        action='store_true'
    )
  
    args = parser.parse_args()

    if args.files:
        scanFiles()
    elif args.midiFileName:
        main(args.midiFileName)
    else:
        parser.print_help()

