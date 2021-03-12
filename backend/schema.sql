-- create table subjects (sub_id char(8) PRIMARY KEY,sub_name varchar(60));

create table students (
    usn varchar(20) PRIMARY KEY,
    fname VARCHAR(10),
    lname VARCHAR(10),
    email VARCHAR(20),
    phone_no CHAR(11),
    sem enum(1,2,3,4,5,6,7,8),
    branch VARCHAR(4),
    status_ bool ,
    constraint mail_ph unique(email,phone_no)
);

--independent

create table semesters (sem_id enum('1','2','3','4','5','6','7','8'),
                        sub_id char(8) PRIMARY KEY,
                        sub_name  varchar(60)
                        branch char(3),
                        branch_name varchar(30)
                        lab TINYINT(1),
                        proj TINYINT(1));

--independent
/* create table branches (branch char(3) primary key,
                       branch_name varchar(30)); */


-- create table in_sub_categories( sub_id CHAR(8),
--                                assignment_id varchar(10),
--                                project_id varchar(10),
--                                lab_id varchar(10),
--                                FOREIGN KEY(sub_id) REFERENCES semesters(sub_id),
--                                unique(assignment_id,project_id,lab_id));

-- create TABLE marks (usn varchar(20),
--                     assignment_id varchar(10),
--                     assignment_marks FLOAT,
--                     project_id varchar(10),
--                     project_marks FLOAT,
--                     lab_id varchar(10),
--                     lab_marks FLOAT,
--                     ia_no INT,
--                     ia_marks FLOAT,
--                     foreign key(usn) REFERENCES students(usn),
--                     foreign key(assignment_id, project_id,lab_id) REFERENCES in_sub_categories(assignment_id,project_id,lab_id));

create TABLE assignment_marks (usn varchar(20),
                    sub_id CHAR(8),
                    assignment_id varchar(10),
                    marks FLOAT,
                    foreign key(usn) REFERENCES students(usn) ON DELETE CASCADE,
                    foreign key(sub_id) REFERENCES semesters(sub_id) ON DELETE CASCADE);


create TABLE project_marks (usn varchar(20),
                    sub_id char(8),
                    marks FLOAT,
                    foreign key(usn) REFERENCES students(usn) ON DELETE CASCADE,
                    foreign key(sub_id) REFERENCES semesters(sub_id) ON DELETE CASCADE);


create TABLE lab_marks (usn varchar(20),
                    sub_id CHAR(8),
                    lab_id varchar(10),
                    marks FLOAT,
                    foreign key(usn) REFERENCES students(usn) on DELETE cascade,
                    foreign key(sub_id) REFERENCES semesters(sub_id) on DELETE cascade);


create TABLE ia_marks (usn varchar(20),
                    sub_id CHAR(8),
                    ia_no INT,
                    marks FLOAT,
                    foreign key(usn) REFERENCES students(usn) on delete cascade,
                    foreign key(sub_id) REFERENCES semesters(sub_id) ON DELETE cascade);




-- create view stud_sub as select sub_id,sub_name from semesters inner join students on semesters.sem_id =students.sem_id;

-- create view stud_marks as SELECT 
create table attendance (usn varchar(20),
                         login_ TIMESTAMP,
                         logout TIMESTAMP, 
                         date_ DATE,
                         sub_id char(8) ,
                         FOREIGN KEY(usn) REFERENCES students(usn) ON DELETE set null,
                         FOREIGN KEY(sub_id) REFERENCES semesters(sub_id) on delete  set null);

<<<<<<< HEAD

=======
create view usn_embed as SELECT usn, embedding FROM `students` order by usn;
>>>>>>> dev


---------------------------------------------------


<<<<<<< HEAD

=======
create TABLE teachers(
    t_id varchar(20) PRIMARY KEY,
    fname VARCHAR(10) NOT NULL,
    lname VARCHAR(10) NOT NULL,
    email VARCHAR(20) NOT NULL,
    phone_no char(11) NOT NULL,
     constraint mail_ph unique(email,phone_no)

);

create table teacher_allocation(
    t_id VARCHAR(20),
    sem enum('1','2','3','4','5','6','7','8') NOT NULL,
    sub_id char(8) NOT NULL,
    foreign key(t_id) references teachers(t_id)
);

--independent
create table t_time_table(
    sub_id char(8),
    class_day ENUM('SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'),
    class_time TIME
);
>>>>>>> dev

-- get_attendance_date_branch_wise 
select date_,count(distinct(attendance.usn)) from attendance,students where login_ is not null and students.branch=%s and sem=%s group by date_;

