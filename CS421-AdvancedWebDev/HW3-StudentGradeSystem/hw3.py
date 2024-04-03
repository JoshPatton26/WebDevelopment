from flask import Flask, render_template, request
from random import randint
import sqlite3 as sql
app = Flask (__name__)

con = sql.connect('database.db')
#con.execute("CREATE TABLE students (firstName TEXT, lastName TEXT, grade TEXT, id TEXT)")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            firstN = request.form['first']
            lastN = request.form['last']
            grade = request.form['grade']
            id = randint(10000, 99999)

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO students (firstName, lastName, grade, id) VALUES (?,?,?,?)", 
                (firstN, lastN, grade, id) )

                con.commit()
                msg = "Successful"
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally:
            return render_template("results.html", msg = msg)
    con.close()    

@app.route('/list')
def list():
    con = sql.connect('database.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("list.html", rows = rows)

if __name__ =='__main__':
    app.run(debug=True)