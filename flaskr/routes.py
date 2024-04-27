from flask import (
        Blueprint, flash, session, jsonify, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flask import current_app
import re
from flask_mysqldb import MySQL
import mysql.connector
from flaskr.db import exec_insert,exec_select


bp = Blueprint ('routes',__name__)
cnx = mysql.connector.connect(user='root', password='Farzana1972$',
                              host='127.0.0.1',
                              database='TravellerSpace')


@bp.route('/')
def index():
    print("hey")
    return render_template('main/first.html')

@bp.route('/register', methods=['POST','GET'])
def reg():
    if request.method == 'POST':
        _username=request.form.get('username')
        _password=request.form.get('password')
        _confPassword=request.form.get('confPassword')
        _name = request.form.get('name')
        _email = request.form.get('email')
        _country = request.form.get('country')
        print()
        if (isUsernameTaken(_username)):
            flash("Username was already taken") 
            return render_template('auth/registration.html') 
        if (_password!=_confPassword):
            flash("Passwords did not match")
            return render_template('auth/registration.html') 
        if (not validatePassword(_password)):
            flash("Password did not meet requirements") 
            return render_template('auth/registration.html') 
        base="INSERT INTO Users(username,password,nickname,email,country)"
        values=" VALUES ({username},{password},{nickname},{email},{country});"
        values=values.format(username='"%s"'%_username,password='"%s"'%_password,nickname='"%s"'%_name,email='"%s"'%_email,country='"%s"'%_country)
        print(base+values)
        exec_insert(base+values)


        createProfile(_username)
        return redirect(url_for('index'))
    return render_template('auth/registration.html')


def createProfile(_username): 
    _username='\'%s\'' % _username 
    query = ("SELECT ID FROM Users"+
            " WHERE USERNAME =" + _username+";") 
    output = exec_select(query)
    print("created profile")
    print(output) 
    id = output[0][0]
    
    query2 = "INSERT INTO Profiles(user_id) VALUES ({});".format(id)
    exec_insert(query2)
    print ("this is query" + query2)



@bp.route('/loginCall', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        _username=request.form.get('login-username',"")
        _username='\'%s\'' % _username
        print (_username)
        _password=request.form.get('login-password',"")
        _password='\'%s\'' % _password

        query = ("SELECT ID FROM Users"+
                 " WHERE USERNAME =" + _username +
                 " AND PASSWORD="+_password+";")
        output = exec_select(query)
        if (output):
            print("routes.py output ---> %s" % output)
            id = output[0][0]
            print ("number: "+str(id))
            session['current_user']= id
            print ("Test: " + str(session.get('current_user')))
            return redirect(url_for('routes.loggedIn',_id = id))
        else:
            flash("Invalid combination of username or password")
    return render_template('main/first.html')


@bp.route('/user', methods=['POST','GET'])
def loggedIn():
    print("user has been logged in")
    return render_template("main/loggedIn.html" )

#clicking on the My Profile Button
@bp.route('/myProfile',methods=['POST','GET'])
def viewMyProfile():
    _id = str(session.get('current_user'))
    print ("My Profile: " + _id )

    query = ("SELECT username,email,country FROM Users"+
             " WHERE ID =" + _id )
    output = exec_select(query)
    print ("my profile query output: " + str(output))

    _username=output[0][0]
    _email=output[0][1]
    _country=output[0][2]
    user = {'username':_username,'email':_email,'country':_country}
    return render_template("main/userProfile.html",user=user)

# function for rendering a user profile based on the username
@bp.route('/viewUserProfile/<_username>',methods=['POST','GET']) 
def viewUserProfile(_username=None):
    username = addQuotes(_username)
    query = ("SELECT username,email,country from Users" +
             " WHERE username = " + username) 
    output = exec_select(query) 
    print (output) 
    print ("Function ---- viewUserProfile")
    print("Sucessfuly printed username " + _username) 
    _username=output[0][0]
    _email=output[0][1]
    _country=output[0][2]
    user = {'username':_username,'email':_email,'country':_country}
    return render_template("main/userProfile.html",user=user)


@bp.route("/searchUsers", methods=['POST','GET'])
def userSearch():
    return render_template("main/navbar/searchBar.html")

'''
clicking on username in searchbar
'''
@bp.route("/storeRenderQuery",methods=["POST"])
def storeUserSearchQuery(): 
    if request.method == 'POST':
        incoming = request.get_json()
        queryName = incoming['render_query']
        print (queryName)
        print("storeUserSearchQuery")
        username = addQuotes(queryName)
        query = ("SELECT username,email,country from Users" +
                 " WHERE username = " + username) 
        output = exec_select(query) 
        print (output) 
        print ("Function ---- viewUserProfile")
        print("Sucessfuly printed username " + username) 
        return jsonify(output)
    print("storeUserSearchQuery -- done")
    return render_template("main/loggedIn.html")


#testing redirection called by JS functiuon
@bp.route("/return",methods=["GET","POST"])
def testingRedirection(): 
    if request.method == 'POST':
        incoming = request.get_json()
        queryName = incoming['searchedUser']
        print(queryName)
        profileName = queryName[0][0]
        print("testingRedirection")
        print (profileName)
        print("testing redirection") 
        return redirect(url_for('routes.viewUserProfile',_username=profileName))
    return 'OK'


# clicking on link from navbar will call this 
@bp.route("/getUser", methods=["GET"])
def getUsers():
    if request.method == 'GET':
        query = "SELECT * FROM Users"
        ret = exec_select(query)
        return str(ret)
    return 'OK'


@bp.route("/getSearchTerm", methods=["POST"])
def getSearch():
    if request.method == 'POST':
        incoming = request.get_json()
        query    = incoming['query']
        ret      = exec_select(query)
        _ret     = re.findall(r"'([^']*)'",str( ret ) )
        _ret     = str( _ret ).replace("'","\"").replace(" ","")
        print("INCOMING")
        print(incoming)
        print(ret)
        print(_ret)
        return str(_ret)
    return '100'



#auxilary methods 

def addQuotes(word):
    return "\"" + word + "\""

def isUsernameTaken (value):
    query = "SELECT USERNAME FROM Users WHERE USERNAME = '%s';" % value
    output = exec_select(query)
    print ("isUsernameTaken: " + str(output)+ "\n")
    if (output):
        return True
    else:
        return False 

def validatePassword(value):
    numbers=False
    special=False
    special_characters = "!@#$%^&*()-+?_=,<>/"
    for character in value:
        if character.isdigit():
            numbers=True
            print ("Numbers detected")
        if (character in special_characters):
            special=True
            print("yes")
    if (special == True and numbers == True):
        return True
    else:
        return False
