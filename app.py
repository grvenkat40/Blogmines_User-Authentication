from flask import Flask,render_template,request,flash,redirect,url_for
import mysql.connector

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
            return render_template('Base.html')
        else:
            flash("Invalid credentials! Please register or try again.")
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

            message=f"User {userid} registered successfully!"
        except Exception as e:
            message=f'Error Occured {e}'
        finally:
            cursor.close()
            db.close()
        
        # flash (message)

        return redirect(url_for('login'))

        
    return render_template('Register.html')

if __name__=='__main__':
    app.run(debug=True)