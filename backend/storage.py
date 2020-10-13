import pickle
import os
import pickle
import logging,sys

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
    filename=PATH +'-application.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

PATH = os.path.join(os.getcwd(),'embeddings_store')

class Storage:
    def __init__(self,PATH=None,branch=None,sem=None):
        self.PATH = globals()["PATH"]
        if branch:
            self.branch = branch
            self.PATH = os.path.join(self.PATH,self.branch)
        if sem:
            self.sem = sem
            self.PATH = os.path.join(self.PATH,self.sem)

    def read_bytes(self):
        if os.path.isabs(self.PATH) and self.PATH.endswith('.png'):
            with open(self.PATH,'rb') as f:
                data=pickle.load(f)
            return zip(data, self.PATH.split('.')[-2])
        else:
            logging.critical(f' Absolute FILE path must be given.')
            logging.critical(f' Skipping read for: {self.PATH}')
            
    def write_bytes(self,data=None,usn=None):
        if os.path.isabs(self.PATH):
            if not os.path.exists(self.PATH):
                os.makedirs(self.PATH)
            p = os.path.join(self.PATH,f'{usn}.pickle')
            with open(p,'wb') as f:
                pickle.dump(data,f)
            logging.info(f' Dumped image for the usn:{usn} of branch: {self.branch} of sem {self.sem}')
            return p