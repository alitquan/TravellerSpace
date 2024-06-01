from flask import (
        Blueprint, flash, session, jsonify, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flask import current_app
import re
from flask_mysqldb import MySQL
import mysql.connector
from flaskr.db import( exec_insert,exec_select,getMessages,getReviews,pushMessage, pushReview)
from datetime import datetime 
import json

bp = Blueprint ('routes',__name__)
cnx = mysql.connector.connect(user='root', password='Farzana1972$',
                              host='127.0.0.1',
                              database='TravellerSpace')


@bp.route('/')
def index():
    print("hey")
    return render_template('main/first.html')


@bp.route('/socket.io/')
def socketio_route():
    print("Received request:", request)
    return "This is the socket.io route"


@bp.route('/register', methods=['POST','GET'])
def reg():
    if request.method == 'POST':
        _username=request.form.get('username')
        _password=request.form.get('password')
        _confPassword=request.form.get('confPassword')
        _name = request.form.get('name')
        _email = request.form.get('email')
        _country = request.form.get('country')

#get current date time
        dateTime = datetime.now()
        _regdate  = dateTime.strftime('%Y-%m-%d %H:%M:%S')
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
        base="INSERT INTO Users(username,password,nickname,email,country,sign_up_date)"
        values=" VALUES ({username},{password},{nickname},{email},{country},{regdate});"
        values=values.format(
                username='"%s"'%_username,
                password='"%s"'%_password,
                nickname='"%s"'%_name,
                email='"%s"'%_email,
                country='"%s"'%_country,
                regdate='"%s"'%_regdate
        )
        print(base+values)
        exec_insert(base+values)


        createProfile(_username)
        return redirect(url_for('index'))
    return render_template('auth/registration.html')


@bp.route('/getUsername', methods=['GET'])
def getUsername():
    # print ("getUsername() -- called") 
    _id = request.args.get("id")
    query = "SELECT username from Users WHERE id = {};".format(_id)
    output = exec_select(query) 

    # exec_select always returns a 2D array
    # print (query)
    # print (output)
    name = output[0][0]
    return jsonify(name)


@bp.route('/lookupID', methods=['GET'])
def idToName():
    print ("idToName() -- called") 
    _id = request.args.get("userID")
    query = "SELECT username from Users WHERE id = {};".format(_id)
    print(query)
    output = exec_select(query) 

    # exec_select always returns a 2D array
    # print (query)
    # print (output)
    name = output[0][0]
    
    print ("idToName() output: ", name)
    return jsonify(name)


def createProfile(_username): 
    _username='\'%s\'' % _username 
    query = ("SELECT ID FROM Users"+
            " WHERE USERNAME =" + _username+";") 
    output = exec_select(query)
    print("created profile")
    # print(output) 
    id = output[0][0]
    
    query2 = "INSERT INTO Profiles(user_id) VALUES ({});".format(id)
    exec_insert(query2)
    print ("this is query" + query2)


@bp.route('/loginCall', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        cleanUp()
        _username=request.form.get('login-username',"")
        _username='\'%s\'' % _username
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

            # logging the login time
            dateTime = datetime.now()
            loginTime  = dateTime.strftime('%Y-%m-%d %H:%M:%S')

            query = "UPDATE Users SET last_login = \"{}\" WHERE id = {}".format(loginTime,id) 
            print(query)
            exec_insert(query)
            return redirect(url_for('routes.loggedIn',_id = id))
        else:
            flash("Invalid combination of username or password")
    return render_template('main/first.html')


@bp.route('/user', methods=['POST','GET'])
def loggedIn():
    print("user has been logged in")
    return render_template("main/loggedIn.html" )


@bp.route('/viewMyProfile',methods=['POST','GET']) 
def viewMyProfile():
    id = str(session.get('current_user'))
    return redirect(url_for('routes.viewProfile',user_id=id))


#clicking on the My Profile Button
@bp.route('/viewProfile<user_id>',methods=['POST','GET'])
def viewProfile(user_id):

    if user_id == str(session.get('current_user')):
        _myProfile = True
    else: 
        _myProfile = False

    print ("Looking for User ID: " + user_id )

    query = ("SELECT * FROM Users"+
             " WHERE ID =" + user_id )
    output = exec_select(query)
    print ("user table output: " + str(output))

    _username=output[0][1]
    _email=output[0][3]
    _country=output[0][5]
    _regdate=output[0][6]
    _lastlog=output[0][7]


    query2 = "SELECT * FROM Profiles WHERE user_id = {}".format(user_id)
    ret = exec_select (query2) 
    _bio= ret[0][1] 

    print("profiles table output: {}".format(str(ret))) 
    _user = {
            'username':_username,
            'email':_email,
            'country':_country,
            'bio':_bio,
            'reg_date': _regdate,
            'last_login':_lastlog
            
    }

    session.pop('viewing_profile', default=None)
    session['viewing_profile'] = user_id
    return render_template("main/userProfile.html",user=_user,myProfile=_myProfile)


@bp.route("/getViewedProfile", methods =['GET'])
def getViewedProfile():
    viewedProfile = str(session.get("viewing_profile"))
    print ("getViewedProfile() --> ", viewedProfile)
    return viewedProfile 


# function for rendering a user profile based on the username
@bp.route('/viewUserProfile/<_username>',methods=['POST','GET']) 
def viewUserProfile(_username=None):

    username = addQuotes(_username)
    query = ("SELECT id,username from Users" +
             " WHERE username = " + username) 
    output = exec_select(query) 
    print ("Function ---- viewUserProfile")
    print("Successfuly printed userinfo for: ", _username) 
    print (output) 
    _id=output[0][0]
    _username=output[0][1]
    session.pop('viewing_profile', default=None)
    session['viewing_profile'] = _id
    return redirect(url_for('routes.viewProfile',user_id=_id))


@bp.route("/searchUsers", methods=['POST','GET'])
def userSearch():
   return render_template("main/navbar/searchBar.html")


@bp.route("/chatroom", methods=['GET'])
def chatRoom(): 
    return render_template("main/navbar/chatRoom.html")


@bp.route('/postReview', methods=['POST'])
def submitReview(): 
    body = request.form['review-body']
    title = request.form['review-title']
    stars = request.form['num-stars']
    posterID = session.get('current_user')
    postedTo = session.get('viewing_profile')
    print ("submitReview()")
    print("Content-Type:", request.content_type) 
    pushReview(postedTo, posterID, stars, title, body)
    print(request) 
    print (body) 
    print (stars) 
    print (posterID)
    print (postedTo) 
    return 'WORKING' 



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


@bp.route("/getProfileInfo", methods=["GET"])
def getProfile(): 
    if request.method == 'GET':
        print()
        print("\ngetProfile()") 
        print(query)
        print(ret) 
        return str(ret)
    return '100'


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


@bp.route("/updateProfile", methods=["POST"])
def updateUserProfile():
    if request.method == 'POST':
        incoming = request.get_json()
        print("updateUserProfile()")
        print(incoming)
        bio = incoming ['bio']
        currentUser =session['current_user']
        query = "UPDATE Profiles SET bio = \"{}\" WHERE user_id = {}".format(bio,currentUser) 
        print(query)
        exec_insert(query)
    return '100'
   


@bp.route('/photo-upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        print ("upload_file()")
        file = request.files['file']
        
        # Process the file (e.g., save it, validate, etc.)
        # Your custom logic here
        return "File uploaded successfully!"
    else:
        print ("no file found")
        return "No file provided."

# chatroom
@bp.route("/getMessages", methods = ["GET"]) 
def getChatroomMessages(): 
    if request.method == 'GET':
        query = getMessages()            
        print()
        return query
    return '100'


@bp.route("/getReviews", methods = ['GET'])
def loadReviews():
    _id = request.args.get("userID")
    print ("loadReviews() arg: ", _id) 
    query = getReviews(_id) 
    print(query)
    return query


@bp.route("/submitChat", methods = ["POST"])
def submitChatMessage():
    if request.method == 'POST':
        incoming = request.get_json()
        print("submitChatMessages")
        print(incoming)
        usr_id = session['current_user']
        msg    = incoming ['msg']
        pushMessage (usr_id,msg)
    return '100'

#auxilary methods 

def cleanUp():
    session.clear()


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
