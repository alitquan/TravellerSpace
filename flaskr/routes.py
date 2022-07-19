from flask import (
        Blueprint, flash, jsonify, g, redirect, render_template, request, url_for)
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
        if (_password!=_confPassword):
            flash("Passwords do not match",category="error")
        if (not validatePassword(_password)):
            flash("Password needs at least one number and at least one special character",category="error")
        base="INSERT INTO Users(username,password,nickname,email,country)"
        values=" VALUES ({username},{password},{nickname},{email},{country});"
        values=values.format(username='"%s"'%_username,password='"%s"'%_password,nickname='"%s"'%_name,email='"%s"'%_email,country='"%s"'%_country)
        print(base+values)
        exec_insert(base+values)
        return redirect(url_for('index'))
    return render_template('auth/registration.html')



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
            return redirect(url_for('routes.loggedIn'))
        else:
            flash("Invalid combination of username or password")
    return render_template('main/first.html')

@bp.route('/user', methods=['POST','GET'])
def loggedIn():
    print("user has been logged in")
    return render_template("main/loggedIn.html" )

@bp.route('/viewProfile', methods=['POST','GET'])
def viewProfile():
    return render_template("main/userProfile.html")

@bp.route("/searchUsers", methods=['POST','GET'])
def userSearch():
    return render_template("main/navbar/searchBar.html")

@bp.route("/getUser", methods=["GET"])
def getUsers():
    if request.method == 'GET':
        query = "SELECT * FROM Users"
        ret = exec_select(query)
        return str(ret)
    return 'OK'

#auxilary methods 
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
