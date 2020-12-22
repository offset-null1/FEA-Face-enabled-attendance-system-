from backend.detect_faces import detector
import face_recognition


d = detector()
while True:
    binary, frame = d.detect()
    if process_this_frame:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = frame_reci