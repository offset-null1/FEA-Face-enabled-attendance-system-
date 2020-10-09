from cv2 import data
import logging
import lmdb
import pickle
import os


PATH = os.path.join(os.getcwd(),'students_embedding.db') 

class lmdatab:
    def __init__(self,PATH=None,map_size=None,readonly=False):
        if data.any():
            self.map_size = map_size #data.nbytes*10       
            self.path = PATH
            self.env = lmdb.open(PATH,map_size=self.map_size,readonly=readonly,create=True)    
            
    def store(self,image=None,usn=None):
       
        with self.env.begin(write=True) as txn:
            logging.info(f'Txn initiated with mode {self.mode}')
            value = [image,name]
            key = usn 
            txn.put(key.encode('ascii'),pickle.dumps(value))
            logging.debug(f' Wrote to path {self.path} :: usn {usn} ::name {name} ')
    
    def read(self,usn):
        with self.env.begin() as txn:
            key = txn.get(usn.encode('ascii'))
            data = pickle.loads(key)
            image = data[0]
            name = data[1]
        return image,name
    
    def close(self):
        logging.info( 'Closing env..')
        self.env.close()
        
    