# FEA (Face Enabled Attendance System) 
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  ![Maintaner](https://img.shields.io/badge/maintainer-offset-null1) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

Face recognition database application (for students in university,schools etc) which allows the user to take *automatic attendance* without manual interference.

It supports *HTML forms* to enter the data and update the database. Also facilitating *registration* of new comers along with their pic to allow automatic facial attendance. 

It allows *visualization* of student scores and attendance to pinpoint the information pictorially without reading the table (though it shows the table along with the graphs).

### *Preview*
Home page:
![Home page](/Preview/fea_ss1.png)

Attendance (table show last few logins and logouts):
![Attendance page](/Preview/fea_ss2.png)

Registration page (pic uploading part):
![Registration page](/Preview/fea_ss4.png)

Registration cont. (details uploading part):
![Home page](/Preview/fea_ss6.png)

Visualization:
![Home page](/Preview/fea_ss13.png)

### *Dependencies*
* Python: 3.6 and above
* Flask : 1.1.2
* Werkzeug: 1.0.1
* OS: Ubuntu 18.04 LTS
* Face Recognition (python module)

### *Setup*
```bash
export PYTHONPATH=path_to_FEA/
export MYSQL_USER=your_username
export MYSQL_PASSWORD=your_password
export MYSQL_DB=database_you_want_to_use
```
**Note:** Make sure you execute FEA/backend/schema.sql for setting up the database. 

### *Special Thanks/Resources*:
* [Bootstrap (creative Tim)](https://www.creative-tim.com/product/blk-design-system)

* [Face Recognition python (Dev.to)](https://dev.to/graphtylove/how-to-automate-attendance-record-with-face-recognition-python-and-react-4413) 
