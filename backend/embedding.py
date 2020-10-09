# import tensorflow as tf
import os,sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import logging
import numpy as np 
from scipy import spatial


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
        except KeyError as err:
            logging.critical(' No parameters passed')
            return

    @staticmethod
    def load_model():
        logging.info(' Loading network...')
        model = VGG16(weights='imagenet', include_top=False)
        return model
    
    @staticmethod 
    def cosine_similarity(embedding1=None, embedding2=None):
            similarity = 1-spatial.distance.cosine(embedding1,embedding2)
            return similarity


    def embedding(self,model):
        batch =[]
        logging.info(f' Building embeddings')
        image = img_to_array(self.data_dict['image'])
        logging.debug(f' Received shape type {type} :: shape {image.shape}')
        image = np.expand_dims(image,axis=0)
        image = preprocess_input(image)
        batch.append(image)
        batch = np.vstack(batch)
        logging.debug(f' Batch shape: {batch.shape}')
        features = model.predict(batch)
        logging.info(f' Raw feature shape: {features.shape}')
        features = features.reshape((features.shape[0], 7*7*512))  
        self.data_dict['embedding']=features
        logging.debug(f' Return embedding shape {features.shape}')
        return self.data_dict
    
    
    # db_embedding= {label:' ', embedding: 'vector' or file input}
    def similarity(self, db_embeddings=None,model=None):
        if db_embeddings.any():
            cur_embedding = self.embedding(model)
            cur_embedding = cur_embedding['embedding']
            similarity = kernel.cosine_similarity(db_embeddings,cur_embedding)
            return similarity
        
            
if __name__ == '__main__':
    print('Raw embedding module')
else:
    pass