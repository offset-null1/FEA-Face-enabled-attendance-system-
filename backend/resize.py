#!/usr/bin/python3

import cv2
from imutils import paths
import logging
import os

cwd = os.getcwd()
default_path = os.path.join(cwd,'cropped')

def resize(source=None,destination = os.path.join(os.getcwd(),'resized'), size=(244,224), interpolation=cv2.INTER_LANCZOS4): 
    
    if not os.path.isabs(destination):
        default_path = os.path.join(os.getcwd(),destination)

    if not os.path.exists(destination):
            os.mkdir(destination) 

    if source:  
        images = list(paths.list_images(source))   
        for (i,image) in enumerate(images):
            logging.info(f' Processing img: {i}/{len(images)}')
            img = cv2.imread(image)
            resized = cv2.resize(img, size, interpolation=interpolation)
            sub_dir = image.split(os.path.sep)[-2]
            abs_sub_dir = os.path.join(default_path,sub_dir)
            if not os.path.exists(abs_sub_dir):
                os.mkdir(abs_sub_dir)
            flag=cv2.imwrite(os.path.join(abs_sub_dir,f'{str(i).zfill(5)}.png'),resized)
            if flag: 
                logging.info(f' Writing to parent dir: {default_path} :: sub dir(class): {sub_dir} ')
            else:
                logging.error(f' Img {image} writing failed')
                
    else:
        logging.warning( 'No source path given, ABORTING')


