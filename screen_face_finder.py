from time import sleep

from PIL import ImageGrab
import cv2
import numpy as np


face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')


# def process_img(image):
#     processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
#     return processed_img
#

def main():
    while True:
        screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
        faces = face_cascade.detectMultiScale(screen, 1.35, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(screen, (x, y), (x + w, y + h), (255, 255, 0), 2)

        cv2.imshow('img', screen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        sleep(0.5)


main()
