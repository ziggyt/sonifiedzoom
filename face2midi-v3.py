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

COORD_DISTANCE_TOLERANCE = 10

vcv_midi_device = MidiDevice()


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
    channel_counter = 15

    old_heads = []
    heads = []

    while True:
        screen = np.array(ImageGrab.grab(bbox=(X_MIN, Y_MIN, X_MAX, Y_MAX)))
        faces = face_cascade.detectMultiScale(screen, 1.35, 5)

        if len(faces) > 0:

            for (x, y, w, h) in faces:
                face = Face(x, y, w, h)

            for face in heads:
                if len(old_heads) > 0:
                    for old_face in old_heads:
                        if abs(face.x - old_face.x) < COORD_DISTANCE_TOLERANCE:

                            if old_face.y_channel == -1 and channel_counter >= 0:
                                old_face.x_channel = channel_counter
                                channel_counter -= 1
                                old_face.y_channel = channel_counter
                                channel_counter -= 1

                            if old_face.y_channel != -1:

                                print(f'found the same face with channels {old_face.x_channel}, {old_face.y_channel}')
                                vcv_midi_device.send_midi_note_to_channel(channel=old_face.x_channel,
                                                                          note=x_coordinate_to_midi(face.x))

                                vcv_midi_device.send_midi_note_to_channel(channel=old_face.y_channel,
                                                                          note=y_coordinate_to_midi(face.y))

                                old_face.x = face.x
                                old_face.y = face.y

                                # face.x_channel = old_face.x_channel
                                # face.y_channel = old_face.y_channel

                                face.flagged = True

            for face in heads:
                if face.flagged:
                    heads.remove(face)
                    print("removed face")

            old_heads += heads

            print(old_heads)
            heads.clear()


            # cv2.imshow('img', screen)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


main()
