#!/usr/bin/python3
from flask.helpers import flash
from mysql.connector.connection import MySQLConnection
from requests.api import get
from werkzeug.datastructures import RequestCacheControl
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
import requests
import pprint

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
        entries={}
        json_data = request.get_json()
        print(json_data)
        usn_present_today = conn.select(columnName=['attendance.usn','students.fname'] , tableName=['attendance', 'students'], where=f" students.usn = '{json_data['usn']}' AND attendance.date_ = '{json_data['date']}' ")

        if usn_present_today:
            update_usn = conn.update(execute=True, tableName='attendance', column={'logout': 'now()' }, where = f"usn = '{json_data['usn']}'")
        else:
            insert_usn = conn.insert(execute=True, tableName='attendance', column={'usn': f" '{json_data['usn']}' ", 'date_': f" '{json_data['date']}' ", 'login_': 'now()' })
            
        logging.debug(entries)
        conn.closeConnection()
    entries = get_5_last_entries()
    print(entries)
        #return details along
    return render_template("video_feed.html", entry=entries)
    # else:    
    # return render_template("video_feed.html")

''' 
To display last 5 attendees 
'''

def get_5_last_entries():
    answers_to_send = {}
    conn = MysqlConnector()
    cols = ['usn','name','login','logout', 'sem']
    last_entries = conn.select(columnName = ['distinct(attendance.usn)','fname', 'login_' ,'logout','sem'] , tableName = ['attendance','students'], where='attendance.usn=students.usn' ,orderBy = 'usn DESC LIMIT 5')
    
    #{0: {'usn': '', 'name': '', 'login': '', 'logout': ''}, 1: {'usn': '', 'name': '', 'login': '','logout': ''}, 2: {...}, ...}
    if last_entries:         
        for index,person in enumerate(last_entries):
                answers_to_send[index] = {}
                for i,j in zip(cols,person):
                    answers_to_send[index][i] = str(j)
    else:
        answers_to_send = {'error': 'DB is not connected or empty'}
    if conn:
        conn.closeConnection()
    return answers_to_send
    
                
'''
To upload students details and academic records

@app.route("/upload")
def upload():
    return render_template("upload/upload.html")
'''

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
        sub_id = request.form.get("sub_id")
        project_marks = request.form.get("project_marks")
        lab_id = request.form.get("lab_id")
        lab_marks = request.form.get("lab_marks")
        where = f'trim(usn)="{usn}"'
        
        res=conn.select(tableName='students',columnName='usn',where=where)
        print(res)
        
        if res is not None:
       
            conn.insert(
                execute=True,
                tableName="ia_marks",
                column={
                    "usn": usn,
                    "ia_no": ia_no,
                    "marks": ia_marks,
                    "sub_id":sub_id
                }
            )
            
            conn.insert(
                execute=True,
                tableName="assignment_marks",
                column={
                    "usn": usn,
                    "assignment_id": assign_id,
                    "marks": assign_marks,
                    "sub_id":sub_id
                }
            )
            
            conn.insert(
                execute=True,
                tableName="lab_marks",
                column={
                    "usn": usn,
                    "marks": lab_marks,
                    "sub_id":sub_id
                }
            )
            
            conn.insert(
                execute=True,
                tableName="project_marks",
                column={
                    "usn": usn,
                    "marks": project_marks,
                    "sub_id":sub_id
                }
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
        sub_id = request.form.get("sub_id")
        assign_marks = request.form.get("assign_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
        
        if res:
            conn.insert(
                execute=True,
                tableName="assignment_marks",
                column={
                    "usn": usn,
                    "assignment_id": assign_id,
                    "marks": assign_marks,
                    "sub_id":sub_id
                }
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
        sub_id = request.form.get("sub_id")
        ia_no = request.form.get("ia_no")
        ia_marks = request.form.get("ia_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
       
        if res:
            conn.insert(
                execute=True,
                tableName="ia_marks",
                column={
                    "usn": usn,
                    "ia_no": ia_no,
                    "marks": ia_marks,
                    "sub_id":sub_id
                }
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
        sub_id = request.form.get("sub_id")
        project_marks = request.form.get("project_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
        if res:
            conn.insert(
                execute=True,
                tableName="project_marks",
                column={
                    "usn": usn,
                    "marks": project_marks,
                    "sub_id":sub_id
                }
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
        sub_id = request.form.get("sub_id")
        lab_marks = request.form.get("lab_marks")
        where = f'usn = {usn}'
        conn = MysqlConnector()
        res=conn.select(tableName='students',columnName='usn',where=where)
        if res:
            conn.insert(
                execute=True,
                tableName="lab_marks",
                column={
                    "usn": usn,
                    "marks": lab_marks,
                    "sub_id":sub_id
                }
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

            return redirect("form1.html")
        else:
            logging.critical(f' Loaded json is: {type(json_str_img_list)}, storage skipped')
    else:
        return render_template("form1.html")

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
    
@app.route('/viz_attendance', methods=["POST", "GET"])
def viz_attendance():
    if request.method == 'POST':
        branch = request.form.get("branch")
        sem = request.form.get("semester") 
        spec_date = request.form.get("date")
        usn = request.form.get("usn")
        
        conn = MysqlConnector()
        
        res = conn.select(columnName=['date_','count(distinct(attendance.usn))'], tableName=['attendance','students'], where=f"login_ is not null and branch='{branch.split(' ')[0]}' and sem='{sem}' ", groupBy='date_')
        
        date=[]
        count=[]
        for i in res:
            date.append(i[0])
            count.append(i[1])
       
        # json_data = json.dumps(
        #     {
        #         "date" : date.__str__(),
        #         "count" : count
        #     }
        # )
        if spec_date and usn:
            
            entries = conn.select(columnName='*', tableName='attendance', where= f"date_ = '{spec_date}' and usn='{usn}'") 
            d={}   
            usn=[]
            login=[]
            logout=[]
            date=[]
            sub_id=[]
            for i in entries:
                usn.append(i[0])
                login.append(i[1])
                logout.append(i[2])
                date.append(i[3])
                sub_id.append(i[4])
            
            d={
                'usn':usn,
                'login':login,
                'logout':logout,
                'date':date,
                'sub_id':sub_id
            }    
            return render_template('viz/attendance.html',values=count,labels=date,spec_date=spec_date,entries=d) 
            
        elif spec_date:    
            
            d={}
            entries = conn.select(columnName='*', tableName='attendance', where= f"date_ = '{spec_date}'")    
            usn=[]
            login=[]
            logout=[]
            date=[]
            sub_id=[]
            for i in entries:
                usn.append(i[0])
                login.append(i[1])
                logout.append(i[2])
                date.append(i[3])
                sub_id.append(i[4])
            
            d={
                'usn':usn,
                'login':login,
                'logout':logout,
                'date':date,
                'sub_id':sub_id
            } 
            conn.closeConnection()
            return render_template('viz/attendance.html',values=count,labels=date,spec_date=spec_date,entries=d) 
        
            
        return render_template('viz/attendance.html',values=count,labels=date,spec_date=spec_date) 
        
            
    # jsonify({'payload':json_data})
    return render_template('viz/attendance.html')
   
@app.route('/viz_marks',methods=['GET','POST'])
def viz_marks():
    if request.method == 'POST':
        conn = MysqlConnector()
        usn = request.form.get('usn')
        ia = request.form.get('ia')
        assign = request.form.get('assign')
        sub = request.form.get('sub')
        sub_name = conn.select(columnName='sub_name', tableName='semesters', where=f"sub_id='{sub}' ")
        print(sub_name)
        marks=[]
        labels=['Assignment','Internal Assessment','Lab','Project']
        if usn and ia and assign and sub:
            res = conn.select(columnName='marks',tableName='assignment_marks',where=f" sub_id='{sub}' and usn='{usn}' and assignment_id='{assign}'")
            if res:
                marks.append(res[0][0])
            res1 = conn.select(columnName='distinct(marks)',tableName='ia_marks',where=f"sub_id='{sub}' and usn='{usn}' and ia_no='{ia}' ")
            if res1:
                marks.append(res1[0][0])
            res2 = conn.select(columnName='marks',tableName='lab_marks',where=f"sub_id='{sub}' and usn='{usn}'")
            if res2:
               marks.append(res2[0][0])
            res3 = conn.select(columnName='marks',tableName='project_marks',where=f"sub_id='{sub}' and usn='{usn}'")
            if res3:
               marks.append(res3[0][0])
            conn.closeConnection()
            return render_template('viz/marks.html',values=marks, labels=labels,sub_name=sub_name)
    return render_template('viz/marks.html')

# @app.route('/viz_student',methods=['GET','POST'])
# def viz_student():
#     if request.method=="POST":
#         usn=request.form.get('usn')
#         sub_id=request.form.get('sub')
#         ia_no=request.form.get('ia')
#         assign_id=request.form.get('assign')
        
        
#         conn = MysqlConnector()
#         d={}
#         l=['usn','fname','lname','email','phone_no','sem','branch','usn','login','logout','date','sub_id','usn','sub_id','assign_no','assign_marks','usn','sub_id','ia_no','ia_marks','usn','sub_id','lab_marks','usn','sub_id','project_marks']
#         attend_count = conn.select(columnName='count(*)',tableName='attendance',where= f"'usn={usn}'")
#         res=conn.select(columnName='*', tableName='students', inner_join=f"attendance on students.usn=attendance.usn inner join assignment_marks on students.usn=assignment_marks.usn inner join ia_marks on students.usn=ia_marks.usn inner join lab_marks on students.usn=lab_marks.usn inner join project_marks on students.usn=project_marks.usn where students.usn='{usn}' and sub_id'{sub_id}' ia_no={ia_no} assignment_id={assign_id}")
#         for i,j in enumerate(res):
#             dd={}
#             for label,data in zip(l,j):
#                 dd[label]=data
#             d[i]=dd
#         return render_template('viz/student_details.html',d=d, attend_count=attend_count)
#     return render_template('viz/student_details.html')
if __name__ == "__main__":
    app.run(debug=True)
