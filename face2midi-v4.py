import mido
from time import sleep
from PIL import ImageGrab
import cv2
import numpy as np

from face import Face
from midi_device import MidiDevice

face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

Y_MIN = 0
Y_MAX = 1440

X_MIN = 0
X_MAX = 2560

MIDI_MIN = 40
MIDI_MAX = 90

vcv_midi_device = MidiDevice()


def x_coordinate_to_midi(coordinate):
    value = float(coordinate) / float(X_MAX)

    mapped_value = int(value * MIDI_MAX)
    print(mapped_value)

    return mapped_value


# def y_coordinate_to_midi(coordinate):
#     value = float(coordinate) / float(Y_MAX)
#
#     mapped_value = int(value * MIDI_MAX)
#     print(mapped_value)
#
#     return mapped_value
#
#
# def x_coordinate_to_midi(coordinate):
#     value = float(coordinate) / float(X_MAX)
#
#     mapped_value = int(value * MIDI_MAX)
#     print(mapped_value)
#
#     return mapped_value

def translate_x_to_midi(value): #https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
    # Figure out how 'wide' each range is
    leftSpan = X_MAX - X_MIN
    rightSpan = MIDI_MAX - MIDI_MIN

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - X_MIN) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(MIDI_MIN + (valueScaled * rightSpan))


def translate_y_to_midi(value): #https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
    # Figure out how 'wide' each range is
    leftSpan = Y_MAX - Y_MIN
    rightSpan = MIDI_MAX - MIDI_MIN

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - Y_MIN) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(MIDI_MIN + (valueScaled * rightSpan))

def main():
    while True:
        screen = np.array(ImageGrab.grab(bbox=(X_MIN, Y_MIN, X_MAX, Y_MAX)))
        faces = face_cascade.detectMultiScale(screen, 1.35, 5)

        if len(faces) > 0:

            for (x, y, w, h) in faces:
                face = Face(x, y, w, h)
                break

            x_note = translate_x_to_midi(face.x)
            y_note = translate_y_to_midi(face.y)

            vcv_midi_device.send_midi_velocity_note_to_channel(x_note, channel=0)
            print(f'SENT VALUE {x_note} TO CHANNEL 0')
            vcv_midi_device.send_midi_velocity_note_to_channel(y_note, channel=1)
            print(f'SENT VALUE {y_note} TO CHANNEL 1')

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            # sleep(3)

            # turn_off_all_notes()


main()
