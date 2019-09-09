# Taken from
# https://github.com/AhmadMoussa/Python-Midi-Ableton/blob/master/Readme.md
# This with the help of a virtual port links python to a midi port readable by a daw.

import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# here we're printing the ports to check that we see the one that loopMidi created.
# In the list we should see a port called "loopMIDI port".
print(available_ports)

# Attempt to open the port
if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")

note_on = [0x90, 70, 112]
note_off = [0x80, 70, 0]
midiout.send_message(note_on)
time.sleep(0.5)
# I tried running the script without having to invoke the sleep function but it doesn't work.
# If someone could enlighten me as to why this is, I'd be more than grateful.
midiout.send_message(note_off)

del midiout