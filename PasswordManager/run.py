import random
import string
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql
from myEncrypt import a28, z82, PASSLEN

Sign_IN = False

# Flask initialization stuff.
app = Flask (__name__)
app.secret_key = "6ix9ine"

# Connecting to the database.
con = sql.connect("3. Hard\PasswordManager\jpm.db")
cur = con.cursor()

# ========== ONLY USE TO RESTART DATABASE ========== 

# cur.execute("DROP TABLE accounts")
# cur.execute("DROP TABLE sites")
# cur.execute("CREATE TABLE accounts (firstname TEXT, lastname TEXT, email TEXT, password TEXT)")
# cur.execute("CREATE TABLE sites (name TEXT, username TEXT, password BLOB)")
# cur.execute("CREATE TABLE sites (name TEXT, username TEXT, password TEXT)")

# ==================================================

@app.route('/')
def home():
    global Sign_IN
    Sign_IN = False

    return render_template("main.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/thankyou', methods = ["GET", "POST"])
def thankyou():
    msg = None
    if(request.method == "POST"):
        if(request.form["email"] != "" and request.form["psw"] == request.form["conpsw"]):
            firstname = request.form["fName"]
            lastname = request.form["lName"]
            email = request.form["email"]
            password = request.form["psw"]
            conn = sql.connect("3. Hard\PasswordManager\jpm.db")
            c = conn.cursor()
            c.execute("INSERT INTO accounts VALUES('"+firstname+"', '"+lastname+"', '"+email+"', '"+password+"') ")           
            conn.commit()
            msg = "Account created successfully. Thank you for creating an account with us!"
            conn.close()
        else:
            msg = "Something went wrong. Please make sure your email is not blank, and both of your passwords match"
    return render_template("thankyou.html", msg = msg)


@app.route('/log-in', methods = ["GET", "POST"])
def login():
    msg = None
    global Sign_IN
    if(request.method == "POST"):
        email = request.form["email"]
        password = request.form["psw"]
        con = sql.connect("3. Hard\PasswordManager\jpm.db")
        c = con.cursor()
        c.execute("SELECT * FROM accounts WHERE email = '"+email+"' and password = '"+password+"'")
        rows = c.fetchall()
        for i in rows:
            if(email == i[2] and password == i[3]):
                session["logedin"]  = True
                session["email"] = email
                Sign_IN = True
                if Sign_IN == True:
                    return redirect(url_for("userhome"))
            else:
                msg = "Email or Password is invalid. Please try again."

            con.commit()
            con.close()
    return render_template("login.html", msg = msg)


@app.route('/userhome', methods = ["GET", "POST"])
def userhome():
    global Sign_IN
    if Sign_IN == False:
                return redirect(url_for("login"))
    
    con = sql.connect("3. Hard\PasswordManager\jpm.db")
    c = con.cursor()
    c.execute("SELECT * FROM accounts")

    con.commit()
    con.close()
    return render_template("userhome.html")


@app.route('/generate', methods = ["GET", "POST"])
def generate():
    if Sign_IN == False:
                return redirect(url_for("login"))
    
    spli = ['!', '?', '+', '][', '*', '&', '^', '%', '$', '#', '@']
    
    val = ''.join(random.choices(string.ascii_letters +
                            string.digits + random.choice(spli), k=PASSLEN))
    
    # a, b, c = a28(val)
    
    if(request.method == "POST"):
        site = request.form["stnme"]
        user = request.form["usrnme"]
        con = sql.connect("3. Hard\PasswordManager\jpm.db")
        cur = con.cursor()
        cur.execute("INSERT INTO sites (name, username, password) VALUES (?,?,?)",
        (site, user, val))
        con.commit()
        con.close()
        return redirect(url_for("userhome"))
    else:
        print("\nSomething went wrong, Try Again.")

    return render_template("generate.html", genpswd=val)


@app.route('/manage', methods = ["GET", "POST"])
def manage():
    if Sign_IN == False:
                return redirect(url_for("login"))

    return render_template("manage.html")

@app.route('/results', methods = ["GET", "POST"])
def results():
    if Sign_IN == False:
                return redirect(url_for("login"))

    if(request.method == "POST"):
        site = request.form["site"]
        
        con = sql.connect("3. Hard\PasswordManager\jpm.db")
        con.row_factory = sql.Row
        c = con.cursor()
        c.execute("SELECT * FROM sites WHERE name = '"+site+"' ")
        rows = c.fetchall()
        print(rows)
    else:
        print("\nSomething went wrong, Try Again.")

    con.commit()
    con.close()
    return render_template("results.html", rows=rows)


if __name__ == "__main__":
     app.run(host="127.0.0.1", port=8080, debug=True)