import face_recognition
import numpy as np
import time
import sys
import logging
import cv2
import os
import requests


fileName = sys.argv[0]

cwd = os.getcwd()

if fileName.startswith("."):
    PATH = cwd + fileName[1:]
elif fileName.startswith("/"):
    PATH = fileName
else:
    PATH = cwd + "/" + fileName

logging.info(f" PATH to executable {PATH}")


logging.basicConfig(
    filename=PATH + "-application.log",
    format="%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

'''
Camera class to access system webcam
'''
class camera:
    def __init__(self, source=0):
        try:
            self.cap = cv2.VideoCapture(int(source))
            logging.debug(f"Camera obj:{self.cap}")
        except:
            logging.critical(
                "Video capture failed, please check the given video source is valid"
            )
            logging.critical("Returning...")
            return

    def __del__(self):
        self.cap.release()
        logging.info(" VideoCapture source released")

    def getRawFrames(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            logging.warning(" VideoCapture source is not opened.")
            logging.critical(" Returning None")
            return
'''
Loading all known registered students 
'''
def load_known_faces():
    known_face_encodings = []
    known_face_usn = []
    known_faces_filenames = []
    path_=[]
    for(root, dirnames, filenames) in os.walk('images/', topdown=True):
        if filenames:
            path_.append(root)
            known_faces_filenames.extend(filenames)

    for root,filename in zip(path_,known_faces_filenames):

        face  = face_recognition.load_image_file(os.path.join(root, filename))
        known_face_usn.append(filename[:-4])
        known_face_encodings.append(face_recognition.face_encodings(face)[0])
    data = {"encodings": known_face_encodings, "usn": known_face_usn, "filenames": known_faces_filenames}
    logging.debug(f"USN recognized: {data['usn']}")
    return data
    
'''
Used for the live attendance
'''
def recognize(cam,known_face_encodings, known_face_usn):
    frame = cam.getRawFrames()
    process_this_frame = True
    if process_this_frame and frame is not None:
        
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        print(face_locations)

        if not face_locations:
            _, jpg = cv2.imencode(".jpg", frame)
            return jpg.tobytes(), frame
        
        else:
            face_usn = []

            json_to_export = {}
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding
                )
                usn = "Unknown"
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding
                )
                best_match_index = np.argmin(face_distances)

                _, jpg = cv2.imencode(".jpg", frame)

                if matches[best_match_index]:
                    usn = known_face_usn[best_match_index]
                    json_to_export["usn"] = usn
                    
                    json_to_export['date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
                    logging.info(f"{json_to_export['date']}")
                    r = requests.post(url='http://127.0.0.1:5000/attendance', json=json_to_export)
                    logging.info("Status: ", r.status_code)

                face_usn.append(usn)
                process_this_frame = not process_this_frame

                for (top, right, bottom, left), usn in zip(face_locations, face_usn):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(
                        frame, usn, (left + 6, bottom - 6), font, 1.0, (240, 126, 190), 1
                    )
                _, jpg = cv2.imencode(".jpg", frame)


                return jpg.tobytes(), frame


if __name__ == "__main__":
    data=load_known_faces()
    cam = camera()
    while True:
        _,f=recognize(cam,data['encodings'], data['usn'])
        cv2.imshow('f',f)
        cv2.waitKey(1)
else:
    ...