import face_recognition
import cv2
import numpy as np
import env
from motor import MotorClient

db = MotorClient(env.py)['projectx']

def compare(img1, img2):
    known_encoding = face_recognition.face_encodings(img1)[0]
    unknown_encoding = face_recognition.face_encodings(img2)[0]

    results = 1-face_recognition.face_distance([known_encoding], unknown_encoding)

    return results


def predict(img1):
    cursor = db.orphan_image.find()
    max_score = 0.4
    img_hash = None
    while(yield cursor.fetch_next):
        data = cursor.next_object()

        img2 = data["img"]

        score = compare(img1, img2)

        if score[0] > max_score:
            max_score = score[0]
            img_hash = data["img_hash"]

    return img_hash, max_score