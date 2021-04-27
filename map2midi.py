import mido

msg = mido.Message('note_on', note=60)

port = mido.open_output('New Port', virtual=True)

while True:
    pass
