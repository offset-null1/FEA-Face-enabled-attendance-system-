import numpy as np
import face_recognition

img1 = face_recognition.load_image_file("img/1.jpg")
img1_loc = face_recognition.face_locations(img1)
img1_encode = face_recognition.face_encodings(img1, img1_loc)


img2 = face_recognition.load_image_file("img/1.jpg")
img2_loc = face_recognition.face_locations(img2)
img2_encode = face_recognition.face_encodings(img2, img2_loc)



for face_encoding in img1_encode :
    name = "unknown"
    matches = face_recognition.compare_faces(img2_encode, face_encoding)
    face_distances = face_recognition.face_distance(img2_encode, face_encoding)
    best_match_index = np.argmin(face_distances)
    
    if matches[best_match_index]:
        name = "Dakshta"
        print(matches[best_match_index])
        
    print(name)