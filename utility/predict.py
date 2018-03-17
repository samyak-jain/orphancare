import face_recognition
import cv2
import numpy as np
import env
from motor import MotorClient

db = MotorClient(env.py)['projectx']

def compare(img1, img2):
    known_encoding = face_recognition.face_encodings(img1)[0]
    unknown_encoding = face_recognition.face_encodings(img2)[0]

    results = face_recognition.face_distance([known_encoding], unknown_encoding)

    return results


def predict(img)
    cursor = db.orphan_image.find()
