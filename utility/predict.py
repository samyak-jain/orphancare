import face_recognition
import numpy as np
from motor import MotorClient


db = MotorClient("mongodb://user:pass@ds143030.mlab.com:43030/projectx")['projectx']

def compare(known_encoding, unknown_encoding):
    # unknown_encoding = face_recognition.face_encodings(img2)[0]

    results = 1 - face_recognition.face_distance([known_encoding], unknown_encoding)
    return results


async def predict(img2):
    # img1 = face_recognition.load_image_file('current.jpeg')
    img2_encoded = face_recognition.face_encodings(np.array(img2))

    cursor = db['image_encodings'].find()
    max_score = 0.6
    img_label = None
    found = False

    if len(img2_encoded)<=0:
        return {'found':False,'img_label':img_label,'max_score':max_score}
    img2_encoded = img2_encoded[0]
    while(await cursor.fetch_next):
        data = cursor.next_object()

        img1_encoded = np.array(data["Image"][1:-1].split()).astype('float32')

        score = compare(img1_encoded, img2_encoded)

        if score[0] > max_score:
            max_score = score[0]
            img_label = data["Labels"]
            found = True

    return {
        'found': found,
        'img_label': img_label,
        'max_score': max_score
    }

if __name__ == "__main__":
    utility.predict.predict(BytesIO(file_body))
