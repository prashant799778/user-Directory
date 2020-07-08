from flask import Flask, render_template,url_for, redirect, jsonify, request, session
from flask import Flask, send_from_directory, abort

from flask_pymongo import PyMongo
from flask import jsonify

import json
import pytz 

from bson.objectid import ObjectId



from flask_pymongo import PyMongo

from pymongo import errors
from datetime import datetime
import os
import urllib.request
from werkzeug import generate_password_hash, check_password_hash
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
bcrypt = Bcrypt(app)





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


@app.route('/register', methods=['POST'])
def insert():
    try:
        if request.method == 'POST':
            inputdata = request.get_data()
            print("===========================",inputdata)      
            inputdata = json.loads(inputdata.decode('utf-8'))
            name = inputdata['name']
            password= inputdata['password']
            email=inputdata['email']
            
            a=CurrentDatetime()
            if name and email and password and request.method == 'POST':
                    _hashed_password = generate_password_hash(password)
                    user = mongo.db.user.find_one({'email':email})
                    print(user)
                    users= mongo.db.user.find_one({'name':name})
                    print(users)
                    if users == None  or user == None:
                            id = mongo.db.user.insert({'name':name, 'email':email, 'pwd': _hashed_password,'status':0,'dateCreate':a,'userType':1})
                            resp = jsonify('User added successfully!')
                            resp.status_code = 200
                            return resp
                    else:
                            resp=jsonify('User already exists')
                            resp.status_code = 200
                            return resp

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
        return render_template("login.html",title="User Login")
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
                a=[]
                
                if data2['status'] == 1:
                    a.append(data2)
                    data={'userProfile':a}
                    return data


                elif data2['status'] == 0:
                   return jsonify({'msg': f'user  DisApproved to login'})
                else:
                    return jsonify({'msg': f'user account Deleted'})
                 
            else:
               
                studen=totalusers()
                
                
                students=studen['users']

                return render_template('dashboard.html',students=students)


                
            
        else:
            return jsonify({'msg': f'user {name} not found'}), 404

# Logout
@app.route('/logout')
def logout():
    if 'name' in session:
        session.pop('name', default=None)
        return jsonify({'msg': 'successfully logged out'})
    else:
        return jsonify({'msg': 'no user logged in'})



@app.route('/updateProfile', methods=['POST'])
def update():
    try:
        inputdata = request.form.get('data') 
        print("===========================",inputdata)      
        inputdata = json.loads(inputdata)
        
        name = inputdata['name']
        password= inputdata['password']
        email=inputdata['email']
        _id = inputdata['id']
       
        filename,PicPath="",""
       


        if 'postImage' in request.files:  
            print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            file = request.files.get('postImage')        
            filename = file.filename or ''  
            print(filename,"jsj")
            filepath = 'C:/Users/goyal/Desktop/' + filename      

            file.save(filename)

        
        if name and email and password and request.method == 'POST':
        	_hashed_password = generate_password_hash(password)
        	mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name':name, 'email':email, 'pwd': _hashed_password,'dateUpdate':CurrentDatetime(),'image':filepath}})
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
                    mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'status':1}})
                    Data = {"status":"true","message":"Account Approved Successfully","result":"data Updated Successfully"}                  
                    return Data
                else:
                    mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'status':0}})
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
                mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'status':1}})
                Data = {"status":"true","message":"Account Deleted Successfully","result":"data Updated Successfully"}                  
                return Data

                        
        
                
            
                        
        
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output        

   

if __name__ == "__main__":
    app.run()
