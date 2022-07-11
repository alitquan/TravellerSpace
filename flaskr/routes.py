from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from flask import current_app
import re
from flask_mysqldb import MySQL

bp = Blueprint ('routes',__name__)

def exec_query(query):
    db = get_db()
    cursor = db.connection.cursor()
    cursor.execute(query)
    print("query executed")
    db.connection.commit()
    cursor.close()

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
        exec_query(base+values)
    return render_template('auth/registration.html')


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
