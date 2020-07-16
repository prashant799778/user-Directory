from flask import Flask, render_template,url_for, redirect, jsonify, request, session
from flask import Flask, send_from_directory, abort

from flask_pymongo import PyMongo
from flask import jsonify
import re
import json
import pytz 

from bson.objectid import ObjectId




from flask_pymongo import PyMongo

from pymongo import errors
from datetime import datetime
import os
import urllib.request
from bson.json_util import dumps


def profilePic(filename):

    path = "C:/Users/goyal/Desktop/"+filename
    return path




def CurrentDatetime():
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(tz=ist)
    ist_f_time = str(ist_time.strftime("%Y-%m-%d %H:%M:%S"))

    return ist_f_time	





app=Flask(__name__)
UPLOAD_FOLDER=  " C:\\Users\\goyal\\Desktop"
URL="http://127.0.0.1:5000/"
defaultPic="defaultpict.png"





app.config['MONGO_DBNAME']='pras'
app.config["MONGO_URI"] = "mongodb://localhost:27017/pras"
    

mongo = PyMongo(app)
app.secret_key = "secret key"



app.debug=True




@app.route("/C:/Users/goyal/Desktop/<image_name>")
def profilePicture(image_name):
    try:
        print(image_name,"wween")
        return send_from_directory('C:/Users/goyal/Desktop/', filename=image_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)	





@app.route('/index')
def Index():
    return render_template('index.html')


@app.route('/register', methods=['GET','POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template("index.html")
        if request.method == 'POST':
            name=str(request.form["name"])
            password = str(request.form["password"])
            email=str(request.form["email"])
            
            a=CurrentDatetime()
            if name and email and password:
                if not re.match(r'[A-Za-z0-9]+',name):
                    msg = 'Username must contain only characters and numbers!'
                    return render_template('index.html',msg=msg)

                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                    return render_template('index.html',msg=msg)

                elif not username or not password or not email:
                    msg = 'Please fill out the form!'
                    return render_template('index.html',msg=msg)

                else:            


                   
                    user = mongo.db.user.find_one({'email':email})
                    print(user)
                    users= mongo.db.user.find_one({'name':name})
                    print(users)
                    if users == None  or user == None:
                            id = mongo.db.user.insert({'name':name, 'email':email, 'password': password,'status':0,'dateCreate':a,'userType':1})
                            msg= 'User  Registered successfully!'
                           
                            return render_template('login.html',msg=msg)
                    else:
                            msg='User already exists'
                            
                            return render_template('index.html',msg=msg)


    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output  



@app.route('/userProfileView', methods=['POST'])
def userProfile():
    try:
        if request.method == 'POST':
            inputdata = request.get_data()
            print("===========================",inputdata)      
            inputdata = json.loads(inputdata.decode('utf-8'))
            Id=inputdata['id']
            user = mongo.db.user.find_one({'_id': ObjectId(Id)})
                
                
            if users != None  :
                    resp=dumps(user)
                    k=json.loads(t)
                    for i in k:
                        
                        if 'image' not in i:
                            i.update({'image':''})
                        image=i['image']
                        if image !='':
                            print("ww")
                            i['image']=URL +i['image']
                           
                        else:
                            print("jw")
                            i['image'] = URL +profilePic(defaultPic)
                        return jsonify(k)
                        
                    
            else:
                    resp=jsonify('User not exists')
                    resp.status_code = 200
                    return resp

    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output             
            
@app.route('/users',methods=['GET'])
def totalusers():
    users = mongo.db.user.find({'status':{'$ne':2},'userType':1})
    t=dumps(users)
    print(t,"list")
    k=json.loads(t)
    for i in k:
        if 'image' not in i:
            i.update({'image':''})
        image=i['image']
        if image !='':
            print("ww")
            i['image']=URL +i['image']
           
        else:
            print("jw")
            i['image'] = URL +profilePic(defaultPic)
    return {'users':k}


                

    	
    	

# Login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        print('ww')
          
        name=str(request.form["name"])
        password = str(request.form["password"])
        users= mongo.db.user.find_one({'name':name,"password":password})
        data1=dumps(users)
        print(data1)
        data2=json.loads(data1)
        print(data2,"hhs")
       
        if data2!=None:

           
            if data2['userType']== 1:
                
                
                if data2['status'] == 1:
                    if 'image' not in data2:
                        data2.update({'image':''})
                    image=data2['image']
                    if image !='':
                        print("ww")
                        data2['image']=URL +data2['image']
                       
                    else:
                        print("jw")
                        data2['image'] = URL +profilePic(defaultPic)
            

                    return render_template('account.html',account=data2)


                elif data2['status'] == 0:
                    msg="Your account has been DisApproved by admin"
                    return render_template('login.html',msg=msg)
                else:
                    msg='Your account has been Deleted by admin'
                    return render_template('login.html',msg=msg)
                 
            else:
               
                studen=totalusers()
                
                
                students=studen['users']

                return render_template('dashboard.html',students=students)


                
            
        else:
            users= mongo.db.user.find_one({'name':name})
            data1=dumps(users)
            print(data1)
            data2=json.loads(data1)
            print(data2,"hhs")
            if data2 != None:
                msg='wrong credentials'
                return render_template('login.html',msg=msg)
            else:
                msg='User does not Exists'
                return render_template('login.html',msg=msg)


#
@app.route('/logout')
def logout():
    return redirect(url_for('login'))
    



@app.route('/removeProfilePic', methods=['POST'])
def update():
    try:
        inputdata = request.form.get('data') 
        print("===========================",inputdata)      
        inputdata = json.loads(inputdata)
        
        name = inputdata['name']
        password= inputdata['password']
        email=inputdata['email']
        _id = inputdata['id']
       
        
       


       
        
        if name and email and password and request.method == 'POST':
            mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name':name, 'email':email, 'pwd': _hashed_password,'dateUpdate':CurrentDatetime(),'image':filename}})
            Data = {"status":"true","message":"data Updated Successfully","result":"data Updated Successfully"}                 
            return Data
           
                        
        
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output  



@app.route('/updateProfilePic', methods=['POST'])
def updateProfilePic():
    try:
        inputdata = request.form.get('data') 
        print("===========================",inputdata)      
        inputdata = json.loads(inputdata)
        _id = inputdata['id']
       
        filename=""
       


        if 'postImage' in request.files:  
            print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            file = request.files.get('postImage')        
            filename = file.filename or ''  
            print(filename,"jsj")
            filepath = 'C:/Users/goyal/Desktop/' + filename      

            file.save(filename)

        
        if  request.method == 'POST':
           
            mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'image':filepath}})
            Data = {"status":"true","message":"Profile Picture Updated Successfully","result":"Profile Picture Updated Successfully"}                  
            return Data
           
                        
        
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output                        


@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp    



@app.route('/AccountStatus', methods=['POST'])
def AccountStatus():
    try:
        inputdata = request.get_data()
        print("===========================",inputdata)      
        inputdata = json.loads(inputdata.decode('utf-8'))
        Id = inputdata['id']

        if Id and request.method == 'POST':
            user = mongo.db.user.find_one({'_id': ObjectId(Id)})
            for i in user:
                status=i['status']
                if status == 0 or status == '0':
                    mongo.db.user.update_one({'_id': ObjectId(Id['$oid']) if '$oid' in Id else ObjectId(Id)}, {'$set': {'status':1}})
                    Data = {"status":"true","message":"Account Approved Successfully","result":"data Updated Successfully"}                  
                    return Data
                else:
                    mongo.db.user.update_one({'_id': ObjectId(Id['$oid']) if '$oid' in Id else ObjectId(Id)}, {'$set': {'status':0}})
                    Data = {"status":"true","message":"Account DisApproved Successfully","result":"data Updated Successfully"}                  
                    return Data
                        
        
                
          
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output


@app.route('/deleteAccount', methods=['POST'])
def deleteAccount():
    try:
        inputdata = request.get_data()
        print("===========================",inputdata)      
        inputdata = json.loads(inputdata.decode('utf-8'))

        Id = inputdata['id']

        if Id and request.method == 'POST':
            user = mongo.db.user.find_one({'_id': ObjectId(Id)})
            if user:
                mongo.db.user.update_one({'_id': ObjectId(Id['$oid']) if '$oid' in Id else ObjectId(Id)}, {'$set': {'status':1}})
                Data = {"status":"true","message":"Account Deleted Successfully","result":"data Updated Successfully"}                  
                return Data

                        
        
                
            
                        
        
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output        

   

if __name__ == "__main__":
    app.run()
