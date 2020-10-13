from backend.embedding import kernel
import cv2
from backend.detect_faces import detector
import numpy as np



if __name__=="__main__":
    s1=cv2.imread('s.png')
    model = kernel.load_model()
    e1=kernel.embedding(s1,model)
    i=0
    d=detector()
    while True:
        byte_img,roi = d.detect()
        i+=1
        cv2.imshow('you',roi)
        roi+=roi
        img = np.divide(roi[:,:,2],224)
        roi = np.divide(roi/i)
        if cv2.waitKey(1) == ord('q'):
            break
        # else:
            # cv2.imwrite('5.png',roi)
        roi_embed = kernel.embedding(roi,model)
        print(kernel.cosine_similarity(e1,roi_embed))
  
    # s2=cv2.imread('2.png')
    # s3=cv2.imread('4.png')
    # s4=cv2.imread('5.png')
    # s = (s1+s2+s3+s4).astype('uint8')
    # img = np.divide(s[:,:,2],224)
    # img = np.divide(s,4)
    # cv2.imwrite('s.png',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # diff=cv2.imread('3.png')

    # k2 = kernel(label='d',data_dict={'image':same1})
    # k3 = kernel(label='a',data_dict={'image':diff})
   
    
    # print(e1['embedding'].shape)
    # sim1=k2.similarity(e1['embedding'],model)
    # print('SAME:',sim1)
    # sim2=k3.similarity(e1['embedding'],model)
    # print('DIFF:',sim2)