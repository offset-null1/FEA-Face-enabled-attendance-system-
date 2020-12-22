import face_recognition
import numpy as np
import time
import logging
import cv2
import os
import re
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class camera:
    def __init__(self, source=None):
        try:
            self.cap = cv2.VideoCapture(source)
            logger.debug(f"Camera obj:{self.cap}")
        except:
            logger.critical(
                "Video capture failed, please check the given video source is valid"
            )
            logger.critical("Returning...")
            return

    def __del__(self):
        self.cap.release()
        logger.info(" VideoCapture source released")

    def getRawFrames(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            logger.warning(" VideoCapture source is not opened.")
            logger.critical(" Returning None")
            return

def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    known_faces_filenames = []

    for(dirpath, dirnames, filenames) in os.walk('../images'):
        known_faces_filenames.extend(filenames)
        break

    for filename in known_faces_filenames:
        face  = face_recognition.load_image_file('../images' + filename)
        known_face_names.append(re.sub("[0-9]",'',filename[:-4]))
        known_face_encodings.append(face_recognition.face_encodings(face)[0])

    return known_face_encodings,known_face_names,known_faces_filenames
    
def recognize(cam, known_face_encodings, known_face_names):
    frame = cam.getRawFrames()
    process_this_frame = True
    if process_this_frame and frame:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []

        json_to_export = {}

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            name = "Unknown"
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            
            _, jpg = cv2.imencode(".png", frame)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                json_to_export["name"] = name
                json_to_export[
                    "hour"
                ] = f"{time.localtime().tm_hour}:{time.localtime().tm_min}"
                json_to_export[
                    "date"
                ] = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}"
                                
                json_to_export["picture_array"] = jpg
                
                r = requests.post(url='http://127.0.0.1:5000/attendance', json=json_to_export)
                logger.info("Status: ", r.status_code)

            face_names.append(name)
            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    frame, name, (left + 6, bottom - 6), font, 1.0, (240, 126, 190), 1
                )

            # _, jpeg_frame = cv2.imencode(".png", frame)
            return jpg.tobytes(), frame
