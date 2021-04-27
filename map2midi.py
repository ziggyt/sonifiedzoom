from time import sleep

import mido

port = mido.open_output('Sonified Zoom', virtual=True)

for i in range(60):
    msg = mido.Message('note_on', note=60 + i)
    port.send(msg)
    sleep(0.5)
    msg = mido.Message('note_off', note=60 + i)
    port.send(msg)
    sleep(0.1)


