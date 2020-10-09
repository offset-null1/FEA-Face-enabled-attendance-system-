from operator import mod
from backend.embedding import kernel
import cv2
from backend.detect_faces import detector
from backend import embedding



if __name__=="__main__":
    same1=cv2.imread('1.png')
    model = kernel.load_model()
    e1=kernel.embedding(same1,model)
   
    d=detector()
    while True:
        byte_img,roi = d.detect()
        
        cv2.imshow('you',roi)
        
        if cv2.waitKey(1) == ord('q'):
            break
        roi_embed = kernel.embedding(roi,model)
        print(kernel.cosine_similarity(e1,roi_embed))
  
    # same2=cv2.imread('2.png')
    # diff=cv2.imread('3.png')
   
    # k2 = kernel(label='d',data_dict={'image':same1})
    # k3 = kernel(label='a',data_dict={'image':diff})
   
    
    # print(e1['embedding'].shape)
    # sim1=k2.similarity(e1['embedding'],model)
    # print('SAME:',sim1)
    # sim2=k3.similarity(e1['embedding'],model)
    # print('DIFF:',sim2)