import mido
from time import sleep
from PIL import ImageGrab
import cv2
import numpy as np

from midi_device import MidiDevice
from face import Face

face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

Y_MIN = 0
Y_MAX = 1440

X_MIN = 0
X_MAX = 2560

MIDI_MAX = 80

COORD_DISTANCE_TOLERANCE = 20

vcv_midi_device = MidiDevice()

old_heads = []


def x_coordinate_to_midi(coordinate):
    value = float(coordinate) / float(X_MAX)

    mapped_value = int(value * MIDI_MAX)
    print(mapped_value)

    return mapped_value


def y_coordinate_to_midi(coordinate):
    value = float(coordinate) / float(Y_MAX)

    mapped_value = int(value * MIDI_MAX)
    print(mapped_value)

    return mapped_value


def main():
    global old_heads
    channel_counter = 0
    heads = []
    while True:
        screen = np.array(ImageGrab.grab(bbox=(X_MIN, Y_MIN, X_MAX, Y_MAX)))
        faces = face_cascade.detectMultiScale(screen, 1.35, 5)

        if len(faces) > 0:

            for (x, y, w, h) in faces:
                face = Face(x, y, w, h)

                face.x_channel = channel_counter
                channel_counter += 1
                face.y_channel = channel_counter
                channel_counter += 1

                # cv2.rectangle(screen, (face.x, face.y), (face.x + face.width, face.y + face.height), (255, 255, 0), 2)
                heads.append(face)

            for face in heads:
                if len(old_heads) > 0:
                    for old_face in old_heads:
                        if abs(face.x - old_face.x < COORD_DISTANCE_TOLERANCE):
                            print('found the same face')
                            vcv_midi_device.send_cc_message(channel=old_face.x_channel,
                                                            value=x_coordinate_to_midi(face.x))
                            vcv_midi_device.send_cc_message(channel=old_face.y_channel,
                                                            value=y_coordinate_to_midi(face.y))

                            face.x_channel = old_face.x_channel
                            face.y_channel = old_face.y_channel

            old_heads = heads.copy()
            heads.clear()
            channel_counter = 0

            # cv2.imshow('img', screen)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


main()
