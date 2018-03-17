import face_recognition as fr
import csv
import os
from scipy.ndimage import imread

def generate_encodings(image, name):
    '''
    generate all image encodings and write  to a csv
    :param image:numpy array of img preferably
    :param name: label of images
    :return:
    '''

    file = open('generated.csv', 'a')
    writer = csv.writer(file)

    encoding = fr.face_encodings(image)
    writer.writerows([[str(name), encoding]])

    print('complete writing')


def load_images():
    dir = 'testdata'

    filenames = os.listdir(dir)

    for f in filenames:
        name, _ = f.split('_')
        print(name)
        img = imread(dir + '/' + f)
        generate_encodings(img, name)

load_images()