#!/usr/bin/python3
from backend.mysqlConnector import MysqlConnector
from flask import Flask, render_template, Response,redirect, url_for,request
from backend.detect_faces import detector
from backend.embedding import kernel
from backend.alignment import align_faces
import base64
import logging
import numpy as np
import cv2
import sys
import os
import re

mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

model = kernel.load_model()


fileName = sys.argv[0]

cwd = os.getcwd()

if fileName.startswith('.'):
    PATH = cwd + fileName[1:]
elif fileName.startswith('/'):
    PATH = fileName
else:
    PATH = cwd + '/' + fileName

logging.info(f' PATH to executable {PATH}')

logging.getLogger("imported_module").setLevel(logging.WARNING)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)



logging.basicConfig(
    filename=PATH +'-application.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

EMBED_PATH = os.path.join(cwd,'students_embedding')


app = Flask(__name__)

conn = MysqlConnector()


@app.teardown_request
def close_conn(error=None):
    if error:
        conn.closeConnection()
        print('CALLED')
        logging.warning(f' Closing mysql conn')
        logging.critical(f' {str(error)}')
    


@app.route('/')
def base():
    return render_template('navbar.html')

def gen(detector_obj):
    
    while True:
        raw_detect,roi = detector_obj.detect()
        yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + raw_detect + b'\r\n')
   
@app.route('/video')
def video():
    return Response(gen(detector()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance/')
def attendance():
    return render_template("video_feed.html")


def decode(img_data=None):
    # img_data = re.sub('^data:image/png;base64,','',img_b64)
    
    byte_str = base64.b64decode(img_data)
    np_img = np.fromstring(byte_str,dtype=np.uint8)
    img = cv2.imdecode(np_img,cv2.IMREAD_UNCHANGED)
    if img.shape[-1]==4:
        np_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return np_img
    
@app.route('/form', methods=["POST","GET"])
def form():
    print("Running /form from",request.remote_addr)

    if request.method == 'POST':
        logging.info(' POST request')
        img_b64 = request.form.get("img")
        usn = request.form.get('usn')
        fname = request.form.get('fname')
        lname= request.form.get('lname')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        semester = request.form.get('semester')
        branch = request.form.get('branch')
              
        np_img = decode(img_data=img_b64)
        # print(np_img.shape)
        # cv2.imshow('img',np_img)
        # cv2.waitKey(0)
        embedding = get_embedding(np_img,model=model)
        
        # store = Storage(branch=semester,sem=branch)
        
        # file=store.write_bytes(data=,usn=usn)
        # conn.insert(tableName='teacher',values=(usn,fname,lname,email,phone_no,file,semester,branch))
        
        # res=conn.select(columnName="*",tableName='students')
        # conn.commit()
        # logging.info(f" Results after commit: {res}s")
        # logging.info(" Data received. Now redirecting ...")
       
        return redirect("/form.html")
    else:   
        return render_template("/form.html")
    



    


def get_embedding(image=None,model=None):
    if image.any():
        logging.info(' Aligning..')
        align_img=align_faces.aligner(image)
        cv2.imwrite('orig.png',image)
        cv2.imwrite('align.png',align_img)
        logging.info( f'Alignment successful shape : {align_img.shape}')
        logging.info(' Network init and calling')
        
        model = kernel.load_model()
        return kernel.embedding(align_img,model)     
    else:
        logging.critical(' Make sure image is captured and streamed in proper format')    



if __name__ == '__main__':
    app.run(debug=True)
   

