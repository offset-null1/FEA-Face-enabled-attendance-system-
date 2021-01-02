#!/usr/bin/python3
from flask.helpers import flash
from backend.mysqlConnector import MysqlConnector
from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from backend.recognize import recognize, load_known_faces, camera
from backend.storage import Storage
import json
import base64
import logging
import numpy as np
import cv2
import sys
import os
import json
import face_recognition

# from vizApp import dashApp


fileName = sys.argv[0]

cwd = os.getcwd()

if fileName.startswith("."):
    PATH = cwd + fileName[1:]
elif fileName.startswith("/"):
    PATH = fileName
else:
    PATH = cwd + "/" + fileName

logging.info(f" PATH to executable {PATH}")

logging.getLogger("imported_module").setLevel(logging.WARNING)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


logging.basicConfig(
    filename=PATH + "-application.log",
    format="%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
mpl_logger = logging.getLogger("__init__")
mpl_logger.setLevel(logging.ERROR)
EMBED_PATH = os.path.join(cwd, "students_embedding")
app = Flask(__name__)
app.secret_key=os.urandom(24)
conn = MysqlConnector()
load_known_faces()


'''
    index
'''
@app.route("/")
def base():
    return render_template("base.html")

''' 
    For video feed
'''
def gen(cam):
    data=load_known_faces()
    # print(data)
    while True:
        # frame = cam.getRawFrame()
        raw_detect, _ = recognize(cam, data['encodings'], data['usn'])
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + raw_detect + b"\r\n"
        )


@app.route("/video")
def video():
    cam = camera()
    return Response(
        gen(cam), mimetype="multipart/x-mixed-replace; boundary=frame" 
    )


@app.route("/attendance", methods=['POST', 'GET'])
def attendance():
    
    if request.method == 'POST':
        conn = MysqlConnector()
        json_data = request.get_json()
        # print(json_data)
        usn_present_today = conn.select(columnName=['attendance.usn','students.fname'] , tableName=['attendance', 'students'], where=f" students.usn = '{json_data['usn']}' ")

        
        if usn_present_today:
            update_usn = conn.update(tableName='attendance', column={'logout': 'now()' }, where = f"usn = '{usn_present_today[0]}'")
        else:
            insert_usn = conn.insert(execute=True, tableName='attendance', column={'usn': f" '{json_data['usn']}' ", 'date': f" '{json_data['date']}' ", 'login': 'now()' })
        conn.closeConnection()
        
        #return details along
        return render_template("video_feed.html")
    else:    
        return render_template("video_feed.html")

''' 
To display last 5 attendees 
'''
@app.route("/get_5_last_entries", methods=['GET'])
def get_5_last_entries():
    answers_to_send = {}
    conn = MysqlConnector()
    cols = ['usn','name','login','logout']
    last_entries = conn.select(columnName = ['distinct(attendance.usn)','login' ,'logout','fname','sem'] , tableName = ['attendance','students'], where='attendance.usn=students.usn' ,orderBy = 'usn DESC LIMIT 5')
    #{0: {'usn': '', 'name': '', 'login': '', 'logout': ''}, 1: {'usn': '', 'name': '', 'login': '','logout': ''}, 2: {...}, ...}
    if last_entries:         
        for index,person in enumerate(last_entries):
                answers_to_send[index] = {}
                for i in person:
                    for j in cols:
                        answers_to_send[index][j] = str(i)
    else:
        answers_to_send = {'error': 'DB is not connected or empty'}
    if conn:
        conn.closeConnection()
    return jsonify(answers_to_send)
                
'''
To upload students details and academic records
'''
@app.route("/upload")
def upload():
    return render_template("upload/upload.html")

'''
Uploading marks
'''
@app.route("/marks", methods=["POST", "GET"])
def marks():
    if request.method == "POST":
        logging.info(" POST request")
        usn = request.form.get("usn")
        assign_id = request.form.get("assign_id")
        assign_marks = request.form.get("assign_marks")
        ia_no = request.form.get("ia_no")
        ia_marks = request.form.get("ia_marks")
        project_id = request.form.get("project_id")
        project_marks = request.form.get("project_marks")
        lab_id = request.form.get("lab_id")
        lab_marks = request.form.get("lab_marks")
        where = f'trim(usn)="{usn}"'
        
        res=conn.select(tableName='students',columnName='usn',where=where)
        print(res)
        
        if res is not None:
       
            conn.insert(
                execute=True,
                tableName="marks",
                column={
                    "usn": usn,
                    "assign_id": assign_id,
                    "assign_marks": assign_marks,
                    "ia_no": ia_no,
                    "ia_marks": ia_marks,
                    "project_id": project_id,
                    "project_marks": project_marks,
                    "lab_id": lab_id,
                    "lab_marks": lab_marks,
                },
            )
            
            res = conn.select(columnName="*", tableName="students")
            conn.closeConnection()
            print("Connection after calling close connection:",conn)
            logging.info(f" Results after commit: {res}")
            logging.info(" Data received. Now redirecting ...")
            flash('Upload successful!','success')
            return redirect(url_for('marks'))
        else:
            logging.critical("Aborting upload as primary key (usn) doesn't exist in tables student ")
            flash('Upload failed!! student is not registered, make sure student register first!','danger')
            return redirect(url_for('marks'))
    else:
        return render_template("upload/marks.html")

'''
Uploading assignment marks
'''
@app.route("/assign", methods=["POST", "GET"])
def assign():
    if request.method == "POST":
        logging.info(" POST request")
        usn = request.form.get("usn")
        assign_id = request.form.get("assign_id")
        assign_marks = request.form.get("assign_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
        
        if res:
            res=conn.insert(
                execute=True,
                tableName="marks",
                column={"usn": usn, "assign_id": assign_id, "assign_marks": assign_marks},
            )
            res = conn.select(columnName="*", tableName="students")
            conn.closeConnection()
            logging.info(f" Results after commit: {res}")
            logging.info(" Data received. Now redirecting ...")
            flash('Upload successful!','success')
            return redirect(url_for('assign'))
        else:
            logging.critical("Aborting upload as primary key (usn) doesn't exist in tables student ")
            flash('Upload failed! This usn is not registered, make sure student register first.','danger')
            return redirect(url_for('assign'))
    else:
        return render_template("upload/assign.html")

'''
Uploading internal assessment marks
'''
@app.route("/ia", methods=["POST", "GET"])
def ia():
    if request.method == "POST":
        logging.info(" POST request")
        usn = request.form.get("usn")
        ia_no = request.form.get("ia_no")
        ia_marks = request.form.get("ia_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
       
        if res:
            res=conn.insert(
                execute=True,
                tableName="marks",
                column={"usn": usn, "ia_no": ia_no, "ia_marks": ia_marks},
            )
            res = conn.select(columnName="*", tableName="students")
            conn.closeConnection()
            logging.info(f" Results after commit: {res}")
            logging.info(" Data received. Now redirecting ...")
            flash('Upload successful!','success')
            return redirect(url_for('ia'))
        else:
            logging.critical("Aborting upload as primary key (usn) doesn't exist in tables student ")
            flash('Upload failed! This usn is not registered, make sure student register first.','danger')
            return redirect(url_for('ia'))
    else:
        return render_template("upload/ia.html")

'''
Uploading project marks
'''
@app.route("/project", methods=["POST", "GET"])
def project():
    if request.method == "POST":
        logging.info(" POST request")
        usn = request.form.get("usn")
        project_id = request.form.get("project_id")
        project_marks = request.form.get("project_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
        if res:
            res=conn.insert(
                execute=True,
                tableName="marks",
                column={
                    "usn": usn,
                    "project_id": project_id,
                    "project_marks": project_marks,
                },
            )
            res = conn.select(columnName="*", tableName="students")
            conn.closeConnection()
            logging.info(f" Results after commit: {res}")
            logging.info(" Data received. Now redirecting ...")
            flash('Upload successful!','success')
            return redirect(url_for('project'))
        else:
            logging.critical("Aborting upload as primary key (usn) doesn't exist in tables student ")
            flash('Upload failed! This usn is not registered, make sure student register first.','danger')
            return redirect(url_for('project'))
    else:
        return render_template("upload/project.html")

'''
Lab marks
'''
@app.route("/lab", methods=["POST", "GET"])
def lab():
    if request.method == "POST":
        logging.info(" POST request")
        usn = request.form.get("usn")
        lab_id = request.form.get("lab_id")
        lab_marks = request.form.get("lab_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
        if res:
            conn.insert(
                execute=True,
                tableName="marks",
                column={"usn": usn, "lab_id": lab_id, "lab_marks": lab_marks},
            )
            res = conn.select(columnName="*", tableName="students")
            conn.closeConnection()
            logging.info(f" Results after commit: {res}")
            logging.info(" Data received. Now redirecting ...")
            flash('Upload successful!','success')
            return redirect(url_for('lab'))
        else:
            logging.critical("Aborting upload as primary key (usn) doesn't exist in tables student ")
            flash('Upload failed! This usn is not registered, make sure student register first.','danger')
            return redirect(url_for('lab'))
    else:
        return render_template("upload/lab.html")

'''
For student registration
'''
@app.route("/form", methods=["POST", "GET"])
def form():
    print("Running /form from", request.remote_addr)

    if request.method == "POST":
        logging.info(" POST request")
        json_str_img_list = request.form.get("img")
        usn = request.form.get("usn")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        phone_no = request.form.get("phone_no")
        semester = request.form.get("semester")
        branch = request.form.get("branch")
        
        if json_str_img_list is not None:
            img_b64_list = json.loads(json_str_img_list)
            logging.info(f' Received image set length: {len(img_b64_list)}')

            embeddings=[]
            for img in img_b64_list:
                np_img = decode(img_data=img)
                # cv2.imshow('img',np_img)
                # cv2.waitKey(0)
                face_picture = face_recognition.load_image_file(np_img)
                face_locations = face_recognition.face_locations(face_picture)
                face_encodings = face_recognition.face_encodings(face_picture,face_locations)
                embeddings.append(face_encodings)
        
            b = branch.split(" ")[0]
            print(b)
            store = Storage(branch=branch.split(" ")[0], sem=semester)
            file = store.write_bytes(data=embeddings, usn=usn)


            conn=MysqlConnector()
            res=conn.insert(
                execute=True,
                tableName="students",
                column={
                    "usn": usn,
                    "fname": fname,
                    "lname": lname,
                    "email": email,
                    "phone_no": phone_no,
                    "semester": semester,
                    "branch": branch,
                    "embedding": file,
                },
            )
            res = conn.select(columnName="*", tableName="students")
            conn.closeConnection()
            logging.info(f" Results after commit: {res}")
            logging.info(" Data received. Now redirecting ...")

            return redirect("form.html")
        else:
            logging.critical(f' Loaded json is: {type(json_str_img_list)}, storage skipped')
    else:
        return render_template("form.html")

'''
Used by form to decode received student image via post method
'''
def decode(img_data=None):
    # img_data = re.sub('^data:image/png;base64,','',img_b64)
    byte_str = base64.b64decode(img_data)
    np_img = np.fromstring(byte_str, dtype=np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)
    if img.shape[-1] == 4:
        np_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return np_img

'''
To list out students who are present for the given subject
'''
@app.route('/get_attendees', methods=['GET', 'POST'])
def get_attendees():
    
    if request.method == "POST":
        subject = request.get("subject")
        conn = MysqlConnector()
        attendees = conn.select(columnName = ['usn','fname'], tableName="attendance", where=f"sub_id = {subject}")
        return jsonify(attendees)
    
# app.route("/viz", methods=["POST", "GET"])
# def viz():
    
#     if request.method == "POST":
#         logging.info(" POST request")
#         usn = request.form.get("usn")
#         project_id = request.form.get("project_id")
#         project_marks = request.form.get("project_marks")
#         where = f'usn = {usn}'
#         conn = MysqlConnector()
#         res=conn.select(tableName='students',columnName='usn',where=where)
        
    
    # return render_template("viz.html")


if __name__ == "__main__":
    app.run(debug=True)
