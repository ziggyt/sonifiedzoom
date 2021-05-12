import mido
from time import sleep
from PIL import ImageGrab
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

Y_MIN = 0
Y_MAX = 1440

X_MIN = 0
X_MAX = 2560

MIDI_MAX = 80

virtual_midi_out = mido.open_output('Sonified Zoom', virtual=True)


def send_midi_note(note: int, state: bool = True):
    midi_state = 'note_on' if state else 'note_off'

    msg = mido.Message(midi_state, note=note)

    virtual_midi_out.send(msg)


def x_coordinate_to_midi(coordinate):
    value = float(coordinate) / float(X_MAX)

    mapped_value = int(value * MIDI_MAX)
    print(mapped_value)

    return mapped_value


def turn_off_all_notes():
    for i in range(127):
        send_midi_note(i, False)


def main():
    while True:
        screen = np.array(ImageGrab.grab(bbox=(X_MIN, Y_MIN, X_MAX, Y_MAX)))
        faces = face_cascade.detectMultiScale(screen, 1.35, 5)

        if len(faces) > 0:

            face = faces[0]

            cv2.rectangle(screen, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (255, 255, 0), 2)

            cv2.imshow('img', screen)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            send_midi_note(x_coordinate_to_midi(face[0]))

            # sleep(3)

            # turn_off_all_notes()


main()
