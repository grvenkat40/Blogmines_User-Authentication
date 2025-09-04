from flask import Flask,render_template,request,flash,redirect,url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app=Flask(__name__)
app.secret_key = 'aS3cr3t!Key#789@dev'

def db_connection_func():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='2040',
        database='users'
    )

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        userid=request.form.get('userid')
        password=request.form.get('password')

        db=db_connection_func()
        cursor=db.cursor()
        
        get_query="select * from user_info where userid=%s and password=%s"
        value=(userid,password)
        cursor.execute(get_query,value)
        user_there=cursor.fetchone()
        cursor.close()
        db.close()

        if user_there:
            flash("Login Success ✅")   
            return redirect(url_for('base'))
        else:
            flash("Invalid credentials! Please register or try again.🤨👇")
            return redirect(url_for('register'))

    return render_template('Login.html')

@app.route('/Register',methods=["GET","POST"])
def register():
    if request.method=='POST':
        userid=request.form.get('userid')
        password=request.form.get('password')

        db=db_connection_func()
        cursor=db.cursor()
        try:
            query="INSERT INTO user_info(userid,password) VALUES (%s,%s)"
            value=(userid,password)
            cursor.execute(query,value)
            db.commit()

            flash(f"User {userid} registered successfully!✅")

        except Exception as e:
            flash(f'Error Occured {e}')
        finally:
            cursor.close()
            db.close()
        
        # flash (message)

        return redirect(url_for('login'))

        
    return render_template('Register.html')

@app.route('/contact',methods=["GET","POST"])
def contact():
    if request.method == 'POST':
        message=""
        Name=request.form.get('name')
        E_mail=request.form.get('e_mail')
        Feedback=request.form.get('feedback')

        db=db_connection_func()
        cursor=db.cursor()
        try:
            table_query='CREATE TABLE IF NOT EXISTS contact_feedback (Id int AUTO_INCREMENT PRIMARY KEY ,Name VARCHAR(50),E_mail VARCHAR(50),Feedback VARCHAR(1000))'
            cursor.execute(table_query)

            insert_query='INSERT INTO contact_feedback(Name,E_mail,Feedback) VALUES (%s,%s,%s)'
            value=(Name,E_mail,Feedback)
            cursor.execute(insert_query,value)
            db.commit()
            flash(f'User {Name} your feedback is submitted successfully 📨✔️')

        except Exception as e:
            flash(f'Error {e}')
        finally:
            cursor.close()
            db.close()
        # flash(message)
        redirect(url_for('contact'))
        
    return render_template('contact.html')

@app.route('/base',methods=['GET','POST'] )
def base():
    if request.method=='POST':
        title=request.form.get('title')
        description=request.form.get('description')
        file=request.files.get('fileInput')


        db=db_connection_func()
        cursor=db.cursor()
        try:
            table_query='CREATE TABLE IF NOT EXISTS blog_submission(Id int AUTO_INCREMENT primary key,title varchar(100) NOT NULL ,description TEXT NOT NULL,file_path varchar(90),created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'

            cursor.execute(table_query)
            file_path=None
            # if file and file.filename != "":
            #     file_path=os.path.join(UPLOAD_FOLDER,file.filename)
            #     file.save(file_path)
            if file and file.filename != "":
                filename = secure_filename(file.filename)
    # Save to static/uploads
                file.save(os.path.join(UPLOAD_FOLDER, filename))
    # Save only "uploads/filename" to DB
                file_path = os.path.join('uploads', filename)
            else:
                file_path = None
            
            insert_query="INSERT INTO blog_submission(title,description,file_path)values (%s,%s,%s)"
            value=(title,description,file_path)
            cursor.execute(insert_query,value)
            db.commit()
            flash(f"{title} is uploaded ✅")
        except Exception as e:
            flash(f'Error {e}')
        finally:
            cursor.close()
            db.close()
        return redirect(url_for('base'))
    
    db=db_connection_func()
    cursor=db.cursor(dictionary=True)
    get_query="SELECT * FROM blog_submission order by created_at desc"
    cursor.execute(get_query)
    blogs=cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('Base.html',blogs=blogs)
            
@app.route('/menu')
def menu():
    return render_template('menu.html')



if __name__=='__main__':
    app.run(debug=True)