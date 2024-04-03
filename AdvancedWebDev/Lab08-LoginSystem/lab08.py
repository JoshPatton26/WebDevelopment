from socket import MsgFlag
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql

app = Flask (__name__)
app.secret_key = "6ix9ine"

con = sql.connect("login.db")
cur = con.cursor()
#con.execute("CREATE TABLE persons (username TEXT, password TEXT)")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/log-in', methods = ["GET", "POST"])
def login():
    r = " "
    msg = " "
    if(request.method == "POST"):
        username = request.form["email"]
        password = request.form["psw"]
        conn = sql.connect("login.db")
        c = conn.cursor()
        c.execute("SELECT * FROM persons WHERE username = '"+username+"' and password = '"+password+"'")
        r = c.fetchall()
        for i in r:
            if(username == i[0] and password == i[1]):
                session["logedin"]  = True
                session["username"] = username
                return redirect(url_for("success"))
            else:
                msg = "Username or Password is invalid. Please try again."
    return render_template("login.html", msg = msg)

@app.route('/sign-up')
def signup():    
    return render_template("signup.html")

@app.route('/success')
def success():
    return render_template("secretpage.html")

@app.route('/thankyou', methods = ["GET", "POST"])
def thankyou():
    msg = None
    if(request.method == "POST"):
        if(request.form["email"] != "" and request.form["psw"] == request.form["conpsw"]):
            username = request.form["email"]
            password = request.form["psw"]
            conn = sql.connect("login.db")
            c = conn.cursor()
            c.execute("INSERT INTO persons VALUES('"+username+"', '"+password+"') ")           
            conn.commit()
            msg = "Account created successfully. Thank you for creating an account with us!"
            conn.close()
        else:
            msg = "Something went wrong. Please make sure your email is not blank, and both of your passwords match"
    return render_template("thankyou.html", msg = msg)

if __name__ =='__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)

# http://127.0.0.1:8080