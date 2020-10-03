#!/usr/bin/python3
from backend.mysqlConnector import MysqlConnector
from flask import Flask, render_template, Response,redirect, url_for,request
from backend.detect_faces import detector
from backend.embedding import kernel
from backend.alignment import align_faces
from flask_socketio import SocketIO,emit
from flask_cors import CORS,cross_origin
import base64
import logging
import numpy as np
import cv2
import sys
import os

fileName = sys.argv[0]

cwd = os.getcwd()

if fileName.startswith('.'):
    PATH = cwd + fileName[1:]
elif fileName.startswith('/'):
    PATH = fileName
else:
    PATH = cwd + '/' + fileName

logging.info(f' PATH to executable {PATH}')

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
cors = CORS(app)
app.config['SECRET_KEY']='blaaaaahblahblahbalhhh'
socket = SocketIO(app,cors_allowed_origins="*")


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
    # network = kernel.load_model()
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

    
@app.route('/form', methods=["POST","GET"])
def form(embedding_file):

    if request.method == 'POST':
        logging.info(' POST request')
        usn = request.form.get('usn')
        fname = request.form.get('fname')
        lname= request.form.get('lname')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        semester = int(request.form.get('semester'))
        
        
        
        conn.insert(tableName='teacher',values=(usn,fname,lname,email,phone_no,embedding_file,semester))
        res=conn.select(columnName="*",tableName='students')
        conn.commit()
        logging.info(f" Results after commit: {res}")
        logging.info(" Data received. Now redirecting ...")
        
        return redirect(url_for('live_train'))
    else:   
        return render_template("user/form.html")
    


def get_embedding(image=None,label=None):
    if image.any() and label:
        logging.info(' Aligning..')
        align_img=align_faces.aligner(image)
        logging.info( 'Alignment successful')
        logging.info(' Network init and calling')
        k = kernel(label= label, data_dict={'image':align_img})
        network = kernel.load_model()
        return k.embedding(network)     
    else:
        logging.critical(' Make sure image is captured and streamed in proper format')
    
@app.route('/register')
@cross_origin()
def live_train():
    logging.info(" On Live train")
    return render_template('live_train.html')       

@socket.on('connect')
def connect():
    logging.info(" Client connected")
    socket.emit('connect response')
    
    
@socket.on('image')
def image(data):
    decoded_data = base64.b64decode(data)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    logging.info(f' Image received of shape: {img.shape}')
    embedding_dict = get_embedding(img)
    return redirect(url_for('form',embedding_dict=embedding_dict))
    
@socket.on('disconnect')
def disconnect():
    logging.info('Client DISCONNECTED, Bye!')


if __name__ == '__main__':
    # app.run(debug=True)
    socket.run(app,debug=True)

