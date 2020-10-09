import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import logging
import numpy as np 
import pickle
import os,sys
import cv2
from matplotlib import pyplot as plt

fileName = sys.argv[0]

cwd = os.getcwd()

if fileName.startswith('.'):
    PATH = cwd + fileName[1:]
elif fileName.startswith('/'):
    PATH = fileName
else:
    PATH = cwd + '/' + fileName

logging.info(f' PATH to executable {PATH}')

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


logging.basicConfig(
    filename=PATH + '-application.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


class kernel:
    def __init__(self, **kwargs):
        try: 
            self.label = kwargs['label'] 
            self.data_dict = kwargs['data_dict']
            print(self.data_dict['frame_batch'].shape)
            logging.info(' Loading network...')
            self.model = VGG16(weights='imagenet', include_top=False)
                
                
        except KeyError as err:
            logging.critical(' No parameters passed')
            return

    def embedding(self):
        batch =[]
        for i,image in self.data_dict.items():
            print(image.shape)
            image = img_to_array(image)
            image = np.expand_dims(image,axis=0)
            image = preprocess_input(image)
            batch.append(image)
            batch = np.vstack(batch)
            logging.info(image.shape)
            features = self.model.predict(batch)
            print(features.shape)
            features = features.reshape((features.shape[0], 7*7*512))
        
        
        self.data_dict['embeddings']=features
            
if __name__ == '__main__':
    print('Raw kernel')
else:
    print("Running imported code from kernel.py")