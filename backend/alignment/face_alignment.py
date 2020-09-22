from .helpers import FACIAL_LANDMARKS_IDXS
from .helpers import shape_to_np
import numpy as np
import cv2

class FaceAligner:
    def __init__(self, predictor, desiredLeftEye=(0.35, 0.35), desiredFaceWidth = 256, desiredFaceHeight = None):
        self.predictor = predictor
        self.desiredLeftEye = desiredLeftEye
        self.desiredFaceWidth = desiredFaceWidth
        self.desiredFaceHeight = desiredFaceHeight
        
        if self.desiredFaceHeight is None:
            self.desiredFaceHeight = self.desiredFaceWidth
            
    def align(self, image, gray, rect):
        shape = self.predictor(gray,rect)
        shape = shape_to_np(shape)
        (startL, endL) = FACIAL_LANDMARKS_IDXS['left_eye']
        (startR, endR) = FACIAL_LANDMARKS_IDXS['right_eye']
        leftEyePts = shape[startL,endL]
        rightEyePts = shape[startR, endR]
        leftEyeCentre = leftEyePts.mean(axis=0).astype('int')
        rightEyeCentre = rightEyePts.mean(axis=0).astype('int')
        dy = rightEyeCentre[1] - leftEyeCentre[1]
        dx = rightEyeCentre[0] - leftEyeCentre[0]
        angle = np.degrees(np.arctan2(dy,dx)) - 180
        desiredRightEyeX = 1.0 - self.desiredLeftEye[0] 
        dist = np.sqrt((dx**2)+(dy**2))
        desiredDist = (desiredRightEyeX - self.desiredLeftEye)
        desiredDist *= self.desiredFaceWidth         
        scale = desiredDist/dist
        
        eyeCentre = ((leftEyeCentre[1]+ rightEyeCentre[1])//2 , (leftEyeCentre[0]+ rightEyeCentre[0])//2)
        M = cv2. getRotationMatrix2D(eyeCentre, angle, scale)
        tX = self.desiredFaceWidth * 0.5
        tY = self.desiredFaceHeight *self.desiredLeftEye[1]
        M[0,1] += (tX, eyeCentre[0])
        M[1,2] += (tY, eyeCentre[1])
        
        (w, h) = (self.desiredFaceWidth, self.desiredFaceHeight)
        output = cv2.warpAffine(image, M, (w, h),flags=cv2.INTER_CUBIC)
        return output
        