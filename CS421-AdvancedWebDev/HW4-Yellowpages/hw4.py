from flask import Flask, render_template, request
from random import randint
import sqlite3 as sql
app = Flask (__name__)

#con = sql.connect('users.db')
#con.execute("CREATE TABLE companies (name TEXT, email TEXT, phone TEXT, address TEXT)")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/list')
def list():
    
    con = sql.connect('users.db')
    con.row_factory = sql.Row

    cur = con.cursor()

    cur.execute("select * from companies")
        
    rows = cur.fetchall()
    con.commit()

    return render_template("list.html", rows = rows)

@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            cName = request.form['name']
            cEmail = request.form['email']
            cPhone = request.form['phone']
            cAddress = request.form['address']

            with sql.connect("users.db") as con:
                cur = con.cursor()
                

                cur.execute("INSERT INTO companies (name, email, phone, address) VALUES (?,?,?,?)", 
                (cName, cEmail, cPhone, cAddress) )
                con.commit()

                con.row_factory = sql.Row
                cur.execute("select * from companies")
                rows = cur.fetchall()

                msg = "Successfully inserted new record."
        except:
            con.rollback()
            msg = "Error in insert operation."
        finally:
            return render_template("results.html", rows = rows, msg = msg)
    con.close()    

@app.route('/delete', methods = ['POST', 'GET'])
def delete():
    msg = " "

    if request.method == 'POST':
        try:
            phone = request.form['phone']

            with sql.connect("users.db") as con:
                cur = con.cursor()

                cur.execute("delete from companies where phone = '"+phone+"'")
                con.commit()

                con.row_factory = sql.Row
                cur.execute("select * from companies")
                rows = cur.fetchall()

                msg = "Successfully deleted record(s)."
        except:
            con.rollback()
            msg = "Error in delete operation."
        finally:
            return render_template("results.html", rows = rows, msg = msg)

@app.route('/modify', methods = ['POST', 'GET'])
def modify():
    if request.method == 'POST':
        try:
            cName = request.form['name']
            cEmail = request.form['email']
            cPhone = request.form['phone']
            cAddress = request.form['address']

            with sql.connect("users.db") as con:
                cur = con.cursor()

                cur.execute("update companies set email = '"+cEmail+"', phone = '"+cPhone+"', address = '"+cAddress+"' where name = '"+cName+"'")
                con.commit()

                con.row_factory = sql.Row
                cur.execute("select * from companies")
                rows = cur.fetchall()

                msg = "Successfully modified record(s)."
        except:
            con.rollback()
            msg = "Error in modify operation."
        finally:
            return render_template("results.html", rows = rows, msg = msg)
    con.close()

if __name__ =='__main__':
    app.run(debug=True)