#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, render_template, url_for, flash, redirect, request, abort, g
import sqlite3
from sqlalchemy.sql import text


app=Flask(__name__)
app.secret_key = 'whatever'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        uname = request.form['username']
        pw = request.form['password']
        role = request.form['role'] # student/instructor
        if role == 'instructor':
            uname_check = """SELECT * from instructor_account where username = '{}'""".format(uname);
            uname_check_result = db.engine.execute(text(uname_check)).fetchall() # empty: []
            # print(usernam_check_result[0]) # ('student1', 'student1', 'student1@mail.utoronto.ca', 1)
            # print(usernam_check_result[0][0]) # 'student1'
            pw_check = """SELECT * from instructor_account where password = '{}'""".format(pw);
            pw_check_result = db.engine.execute(text(pw_check)).fetchall() # empty: []
            if uname_check_result != [] and pw_check_result != []:
                user_id = uname_check_result[0][2]
                session['id'] = user_id
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password.')
                return redirect(url_for('login'))
        elif role == 'student':
            uname_check = """SELECT * from student_account where username = '{}'""".format(uname);
            uname_check_result = db.engine.execute(text(uname_check)).fetchall() # empty: []
            # print(usernam_check_result[0]) # ('student1', 'student1', 'student1@mail.utoronto.ca', 1)
            # print(usernam_check_result[0][0]) # 'student1'
            pw_check = """SELECT * from student_account where password = '{}'""".format(pw);
            pw_check_result = db.engine.execute(text(pw_check)).fetchall() # empty: []
            if uname_check_result != [] and pw_check_result != []:
                user_id = uname_check_result[0][2]
                session['id'] = user_id
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password.')
                return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        new_account_id = request.form['new_account_id']
        uname = request.form['username']
        pw = request.form['password']
        role = request.form['role'] # student/instructor
        if role == 'instructor':
            id_exist = """SELECT * from valid_instructor where i_id = '{}'""".format(new_account_id)
            id_exist_result = db.engine.execute(text(id_exist)).fetchall()

            id_occupied = """SELECT * from instructor_account where i_id = '{}'""".format(new_account_id)
            id_occupied_result = db.engine.execute(text(id_occupied)).fetchall()

            uname_exist = """SELECT * from instructor_account where username = '{}'""".format(uname)
            uname_exist_result = db.engine.execute(text(uname_exist)).fetchall()

            if id_exist_result == []:
                flash('Sorry you are not in the course team.')
                return redirect(url_for('register'))
            else:
                if id_occupied_result != []:
                    flash('This instructor already has an account.')
                    return redirect(url_for(('login')))
                else:
                    if uname_exist_result != []:
                        flash('Username already taken.')
                        return redirect(url_for('register'))
                    else:
                        add_account = """INSERT INTO instructor_account (username, password, i_id) VALUES ('{}', '{}', '{}')""".format(uname, pw, new_account_id)
                        db.engine.execute(text(add_account))
                        return redirect(url_for('login'))
        elif role == 'student':
            id_exist = """SELECT * from valid_student where s_id = '{}'""".format(new_account_id)
            id_exist_result = db.engine.execute(text(id_exist)).fetchall()

            id_occupied = """SELECT * from student_account where s_id = '{}'""".format(new_account_id)
            id_occupied_result = db.engine.execute(text(id_occupied)).fetchall()

            uname_exist = """SELECT * from student_account where username = '{}'""".format(uname)
            uname_exist_result = db.engine.execute(text(uname_exist)).fetchall()

            if id_exist_result == []:
                flash('Student not enrolled in this course.')
                return redirect(url_for('register'))
            else:
                if id_occupied_result != []:
                    flash('This student already has an account.')
                    return redirect(url_for('login'))
                else:
                    if uname_exist_result != []:
                        flash('Username already taken.')
                        return redirect(url_for('register'))
                    else:
                        add_account = """INSERT INTO student_account (username, password, s_id) VALUES ('{}', '{}', '{}')""".format(uname, pw, new_account_id)
                        db.engine.execute(text(add_account))
                        return redirect(url_for('login'))

@app.route("/home")
def home():
    if 'id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route("/syllabus")
def syllabus():
    return render_template('syllabus.html')

@app.route("/assignment")
def assignment():
    if 'id' in session:
        return render_template('assignment.html')
    return redirect(url_for('login'))


@app.route("/labs")
def labs():
    if 'id' in session:
        return render_template('labs.html')
    return redirect(url_for('login'))

@app.route("/courseteam")
def courseteam():
    if 'id' in session:
        return render_template('courseteam.html')
    return redirect(url_for('login'))

@app.route("/mark")
def mark():
    if 'id' in session:
        u_id = session['id']
        # print(u_id)
        if u_id in range(1, 11): # students
            # print(usernam_check_result[0]) # ('student1', 'student1', 'student1@mail.utoronto.ca', 1)
            student_marks = """SELECT * from grades where s_id = '{}'""".format(u_id)
            student_marks_result = db.engine.execute(text(student_marks)).fetchall()

            remark_history = """SELECT * from request_remark where s_id = '{}'""".format(u_id)
            remark_history_result = db.engine.execute(text( remark_history)).fetchall()
            return render_template('mark.html', student_marks_result=student_marks_result, remark_history_result=remark_history_result)
        elif u_id in range(100, 105): # instructors
            instructor_marks = """SELECT * from grades where i_id = '{}'""".format(u_id)
            instructor_marks_result = db.engine.execute(text(instructor_marks)).fetchall()

            new_remark_requests = """SELECT * from request_remark where i_id = '{}' and read = 0""".format(u_id)
            new_remark_requests_result = db.engine.execute(text(new_remark_requests)).fetchall()


            num = len(new_remark_requests_result)

            all_remark_requests = """SELECT * from request_remark where i_id = '{}'""".format(u_id)
            all_remark_requests_result = db.engine.execute(text(all_remark_requests)).fetchall()

            return render_template('mark.html', num=num, instructor_marks_result=instructor_marks_result, new_remark_requests_result=new_remark_requests_result, all_remark_requests_result=all_remark_requests_result)
    return redirect(url_for('login'))

@app.route("/request_remark", methods=['GET', 'POST'])
def request_remark():
    if 'id' in session:
        u_id = session['id']
        which = request.form['which']
        reason = request.form['reason']
        num = """SELECT * from request_remark""".format()
        num = db.engine.execute(text(num)).fetchall()
        num = len(num)
        ins_id = """SELECT * from relationship where s_id = '{}'""".format(u_id)
        ins_id = db.engine.execute(text(ins_id)).fetchall()
        ins_id = ins_id[0][1]
        read = 0
        add_request = """INSERT INTO request_remark (rank, s_id, i_id, which, reason, read) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(num, u_id, ins_id, which, reason, read)
        db.engine.execute(text(add_request))
        return redirect(url_for('mark'))
    else:     
        return redirect(url_for('login'))



@app.route("/change_mark", methods=['GET', 'POST'])
def change_mark():
    if 'id' in session:
        u_id = session['id']
        which = request.form['which']
        new_score = request.form['new_score']
        student_id = request.form['student_id']
        identifier = request.form['identifier']

        modify_grade = """UPDATE grades SET '{}'='{}' WHERE s_id='{}'""".format(which, new_score, student_id)
        db.engine.execute(text(modify_grade))
        
        modify_history = """UPDATE request_remark SET read=1 WHERE rank='{}'""".format(identifier)
        db.engine.execute(text(modify_history))
        return redirect(url_for('mark'))
    else:     
        return redirect(url_for('login'))


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if 'id' in session:
        u_id = session['id']
        if u_id in range(1, 11):
            role = 'student'
            if request.method == 'GET':
                available_instructor = '''select name, X.i_id from valid_instructor as X
                join
                (select i_id from instructor_account where exists
                (select i_id from valid_instructor)) Y
                on x.i_id = Y.i_id;'''
                available_instructor = db.engine.execute(text(available_instructor)).fetchall()

                my_feedback = """select name, Y.msg from valid_instructor as X 
                join
                (SELECT i_id, msg from feedback where s_id='{}') as Y
                on X.i_id = Y.i_id""".format(u_id)
                my_feedback = db.engine.execute(text(my_feedback)).fetchall()

                # replied_me = """SELECT * from feedback where s_id = '{}' and reply != -1""".format(u_id)
                replied_me = """select name, reply, rank from valid_instructor natural join
                (select * from feedback where s_id = '{}' and reply != -1 and receive = 0)""".format(u_id)
                replied_me = db.engine.execute(text(replied_me)).fetchall()
                number = len(replied_me)
                return render_template('feedback.html', available_instructor=available_instructor, my_feedback=my_feedback, role=role, number=number, replied_me=replied_me)
            else:
                which = request.form['which']
                msg = request.form['feedback']
                num = """SELECT * from feedback""".format()
                num = db.engine.execute(text(num)).fetchall()
                num = len(num)
                read = 0
                reply = -1
                receive = 0
                write_feedback = """INSERT INTO feedback (i_id, s_id, msg, read, rank, reply, receive) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(which, u_id, msg, read, num, reply, receive)
                db.engine.execute(text(write_feedback))
                return redirect(url_for('feedback'))
        else:
            if request.method == 'GET':
                u_id = session['id']
                new_feedback = """SELECT * from feedback where i_id = '{}' and read = 0""".format(u_id)
                new_feedback = db.engine.execute(text(new_feedback)).fetchall()
                num = len(new_feedback)


                all_feedback = """SELECT * from feedback where i_id = '{}'""".format(u_id)
                all_feedback = db.engine.execute(text(all_feedback)).fetchall()
                num_all = len(all_feedback)
                
                return render_template('feedback.html', num=num, new_feedback=new_feedback, num_all=num_all, all_feedback=all_feedback)
            else:
                identifier = request.form['identifier']
                reply = request.form['reply']
                read = 1
                send_reply = """UPDATE feedback SET read='{}', reply='{}' WHERE rank='{}'""".format(read, reply, identifier)
                db.engine.execute(text(send_reply))
                return redirect(url_for('feedback'))
    else:
        return redirect(url_for('login'))


@app.route("/mark_read", methods=['GET', 'POST'])
def mark_read():
    if 'id' in session:
        u_id = session['id']

        # which_form = request.form['delete_mark']
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', which_form)
        if 'delete_remark' in request.form:
            identifier = request.form['delete_remark']
            identifier = identifier[6:]
            read = 1
            delete_remark = """UPDATE request_remark SET read='{}' WHERE rank='{}'""".format(read, identifier)
            db.engine.execute(text(delete_remark))
            return redirect(url_for('mark'))
        elif 'delete_reply' in request.form:
            identifier = request.form['delete_reply']
            identifier = identifier[6:]
            receive = 1
            delete_reply = """UPDATE feedback SET receive='{}' WHERE rank='{}'""".format(receive, identifier)
            db.engine.execute(text(delete_reply))
            return redirect(url_for('feedback'))

        elif 'delete_feedback' in request.form:
            identifier = request.form['delete_feedback']
            identifier = identifier[6:]
            read = 1
            delete_feedback = """UPDATE feedback SET read='{}' WHERE rank='{}'""".format(read, identifier)
            db.engine.execute(text(delete_feedback))
            return redirect(url_for('feedback'))
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run(debug=False, host='0.0.0.0', port=5000)
    #app.run(debug=True, port=5000)
