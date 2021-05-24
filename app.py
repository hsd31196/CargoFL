from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql


app = Flask(__name__)

try:
    print(f'Checking if database exists or not...')
    conn = sql.connect('database.db')
    print(f'Succesfully connected to database!')
    conn.execute('CREATE TABLE if not exists employee (first TEXT, middle TEXT, last TEXT, dob TEXT, gender TEXT, bg TEXT, marital TEXT, email TEXT, mobile TEXT, alternate TEXT)')
    print("Table created successfully")
    conn.close()
        
except sql.OperationalError as err:
        print('Database does not exist')
        print(err)

@app.route('/',methods = ['POST', 'GET'])
def add_emp():
    if request.method == 'POST':
            form_data=request.form
            fname=request.form['Employee First Name']
            mname=request.form['Employee Middle Name']
            lname=request.form['Employee Last Name']
            gender=request.form['Gender']
            dob=request.form['Date of Birth']
            mobile=request.form['Mobile Number']
            alternate=request.form['Alternate Mobile Number']
            email=request.form['Email ID']
            marital=request.form['Marital Status']
            bg=request.form['Blood Group']

            
            #add record to database
            try:
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute("INSERT INTO employee (first,middle,last,dob,gender,bg,marital,email,mobile,alternate) VALUES (?,?,?,?,?,?,?,?,?,?)"
                ,(fname,mname,lname,dob,gender,bg,marital,email,mobile,alternate) )

                con.commit()
                msg = "Record successfully added"
                print(msg)
            except:
                con.rollback()
                msg = "Error in insert operation"
                print(msg)
            finally:
                con.close()
                return render_template("/view_employee.html",form_data=form_data)
                
    return render_template("add_employee.html")
    


@app.route('/manage_emp')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from employee")
   print("Fetch.....")
   rows = cur.fetchall()
   return render_template("manage_employee.html",rows = rows)
  

if __name__ == '__main__':
    app.run(debug=True)