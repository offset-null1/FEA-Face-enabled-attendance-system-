from facenet_pytorch import MTCNN
import torch
import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)
class camera:
    def __init__(self,source=None):
        try:
            self.cap = cv2.VideoCapture(source)
            logger.debug(f'Camera obj:{self.cap}')
        except:
            logger.critical('Video capture failed, please check the given video source is valid')
            logger.critical('Returning...')
            return
            
        
    def __del__ (self):
        self.cap.release()
        logger.info(' VideoCapture source released')
        
    def getRawFrames(self):    
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            logger.warning(' VideoCapture source is not opened.')
            logger.critical(' Returning None')
            return


class detector(camera):
    def __init__(self,source=0):
        super(detector,self).__init__(source=source)         
    
    def detect(self):
        frame = self.getRawFrames()
        
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        logger.info(f'Running on device: {device}')
        mtcnn = MTCNN(keep_all=True, device=device)

        boxes,_ = mtcnn.detect(frame)
        if boxes.any():
            frame_draw = frame.copy()

            for box in boxes:
                cv2.rectangle(frame_draw, (box[0],box[1]),(box[2],box[3]), (240,126,190),1) 

            _, jpeg_draw = cv2.imencode('.png', np.float32(frame_draw))
            return jpeg_draw.tobytes(),frame_draw
        
        _, jpeg_orig = cv2.imencode('.png', frame)
        return jpeg_orig.tobytes(),frame

                
if __name__ == '__main__':
    print('Raw detector module')
else:
    print("Running imported code of detect_faces")