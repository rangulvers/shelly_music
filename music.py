import mido
import time
import requests

midifile = mido.MidiFile('beethoven_fur_elise.mid', clip=True)

mod = 5

# Shelly not mapping. Make sure to have the same ammount of shellys as you have defined for the modolus 
# Note Number : Shelly IP : Relay 
shellyNoteMapping = {
    60: ["192.168.2.142", "0"], # Haustür
    61: ["192.168.2.141", "0"], # Garage Einfahrt
    62: ["192.168.2.138", "0"],  # Erker
    63: ["192.168.2.167", "1"], # Terrasse
    64: ["192.168.2.139", "0"] # Küche
}

on_off_Mapping = {
    "note_on" : "on",
    "note_off" : "off"
}

print("Preping light show. Turn off all Shellys....")
for shelly in shellyNoteMapping:
    print(f"http://{shellyNoteMapping[shelly][0]}/relay/{shellyNoteMapping[shelly][1]}?turn=off")
    r = requests.get(f"http://{shellyNoteMapping[shelly][0]}/relay/{shellyNoteMapping[shelly][1]}?turn=off")


with mido.open_output("Microsoft GS Wavetable Synth 0") as output:
    try:
        t0 = time.time()
        for message in midifile.play():
            # print(message)
            output.send(message)
            if message.type in ["note_on", "note_off"]:
                note = (message.note%mod) + 60
                print(f"{note} - {message.type}")
                print(f"http://{shellyNoteMapping[note][0]}/relay/{shellyNoteMapping[note][1]}?turn={on_off_Mapping[message.type]}")
                r = requests.get(f"http://{shellyNoteMapping[note][0]}/relay/{shellyNoteMapping[note][1]}?turn={on_off_Mapping[message.type]}")
        print('play time: {:.2f} s (expected {:.2f})'.format(
            time.time() - t0, midifile.length))
    except KeyboardInterrupt:
        print()
        output.reset()
