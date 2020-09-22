from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import os
import argparse
import imutils
import dlib
import cv2

shape_predictor = os.path.join(os.environ['HOME'], '.local/lib/python3.6/site-packages/face_recognition_models/models/shape_predictor_68_face_landmarks.dat')


def aligner(img):
	detector = dlib.get_frontal_face_detector()
	
	predictor = dlib.shape_predictor(shape_predictor)
	fa = FaceAligner(predictor, desiredFaceWidth=224)
	image=img.copy()
	image = imutils.resize(image, width=800)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	rects = detector(gray, 2)

	for rect in rects:
		(x, y, w, h) = rect_to_bb(rect)
		faceOrig = imutils.resize(image[y:y + h, x:x + w], width=224)
		faceAligned = fa.align(image, gray, rect)
		return faceAligned
    
        
