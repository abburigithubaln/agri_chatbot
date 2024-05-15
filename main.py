from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
import mysql.connector

import gensim
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
from gensim.parsing.porter import PorterStemmer

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="agri_chatbot"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""

    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cc_customer where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        print(myresult)
        if myresult>0:
            session['username'] = username1
            ff=open("user.txt",'w')
            ff.write(username1)
            ff.close()
            result=" Your Logged in sucessfully**"
            return redirect(url_for('userhome')) 
        else:
            msg="Invalid Username or Password!"
            result="You are logged in fail!!!"
        

    return render_template('index.html',msg=msg,act=act)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login_admin.html',msg=msg,act=act)

@app.route('/login',methods=['POST','GET'])
def login():
    cnt=0
    act=""
    msg=""

    
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ag_user where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('bot')) 
        else:
            msg="Invalid Username or Password!"
            result="You are logged in fail!!!"
        

    return render_template('login.html',msg=msg,act=act)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        

        mycursor.execute("SELECT count(*) FROM ag_user where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM ag_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO ag_user(id,name,address,mobile,email,uname,pass,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,address,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='Already Exist'
            
    
    return render_template('register.html', msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get("act")
    
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        query=request.form['query']
        answer=request.form['answer']
        
        mycursor.execute("SELECT max(id)+1 FROM ag_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ag_data(id,query,answer,voice_note) VALUES (%s,%s,%s,%s)"
        val = (maxid,query,answer,'')
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        return redirect(url_for('admin',act='1'))
            
      
    
    return render_template('admin.html',msg=msg,act=act)

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ag_data")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ag_data where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_data'))
    
    return render_template('view_data.html',msg=msg,act=act,data=data)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    msg=""
    act=request.args.get("act")
    did=request.args.get("did")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ag_data where id=%s",(did,))
    data = mycursor.fetchone()

    if request.method=='POST':
        query=request.form['query']
        answer=request.form['answer']
        
        mycursor.execute("update ag_data set query=%s,answer=%s where id=%s",(query,answer,did))
        mydb.commit()
        
        print(mycursor.rowcount, "Registered Success")
        return redirect(url_for('view_data'))
            
      
    
    return render_template('edit.html',msg=msg,act=act,data=data)

@app.route('/voice', methods=['GET', 'POST'])
def voice():
    msg=""
    act=request.args.get("act")
    did=request.args.get("did")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ag_data where id=%s",(did,))
    data = mycursor.fetchone()

    if request.method=='POST':
        file=request.files['file']
        fname = file.filename
        f1="A"+did+fname
        filename = secure_filename(f1)
        file.save(os.path.join("static/upload/", filename))
        
        mycursor.execute("update ag_data set voice_note=%s where id=%s",(filename,did))
        mydb.commit()
        
        print(mycursor.rowcount, "Registered Success")
        return redirect(url_for('view_data'))
            
      
    
    return render_template('voice.html',msg=msg,act=act,data=data)


@app.route('/bot', methods=['GET', 'POST'])
def bot():
    msg=""
    output=""
    uname=""
    mm=""
    s=""
    xn=0
    if 'username' in session:
        uname = session['username']

    cnt=0
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      charset="utf8",
      database="agri_chatbot"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ag_data order by rand() limit 0,10")
    data=mycursor.fetchall()
            
    if request.method=='POST':
        msg_input=request.form['msg_input']
        

        ##
        
        nlp=STOPWORDS
        def remove_stopwords(text):
            clean_text=' '.join([word for word in text.split() if word not in nlp])
            return clean_text
        ##
        txt=remove_stopwords(msg_input)
        ##
        mm='%'+msg_input+'%'
        
        mycursor.execute("SELECT count(*) FROM ag_data where query like %s || answer like %s",(mm,mm))
        cnt=mycursor.fetchone()[0]
        if cnt>0:
            
            mycursor.execute("SELECT * FROM ag_data where query like %s || answer like %s",(mm,mm))
            dd=mycursor.fetchone()
            
            if dd[3]=="":
                s=""
            else:
                #s='<embed src=static/upload/'+dd[3]+' autostart="false" width="10" height="10"></embed>'
                s='<a href=static/upload/'+dd[3]+' target="_blank">Voice</a>'
                
            output=dd[2]+" - "+s

        else:
            if msg_input=="":
                output="How can i help you?"
            else:
                output="Sorry, No Results Found!"

        return json.dumps(output)


    return render_template('bot.html', msg=msg,output=output,uname=uname,data=data)   




@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
