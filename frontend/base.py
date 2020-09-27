#!/usr/bin/python3
from flask import Flask, render_template, Response,redirect, url_for
import sys
import cv2
import backend


app = Flask(__name__)

@app.route('/')
def base():
    return render_template('navbar.html')

def gen(detector_obj):
    # network = backend.embedding.kernel.load_model()
    while True:
        raw_detect,roi = detector_obj.detect()
        yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + raw_detect + b'\r\n')
   
@app.route('/video')
def video():
    return Response(gen(backend.detect_faces.detector()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance/')
def attendance():
    return render_template("video_feed.html")

@app.route('/form', methods=["GET","POST"])
def form():
    return render_template("user/form.html")

@app.route('/<string:page>')
def show(page):
    return redirect(url_for(page))

if __name__ == '__main__':
    app.run(debug=True)

