from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint ('routes',__name__)

@bp.route('/')
def index():
    print("hey")
    return render_template('main/first.html')

@bp.route('/register', methods=['POST','GET'])
def reg():
    if request.method == 'GET':
        _username=request.form.get('username')
        _password=request.form.get('password')
        _confPassword=request.form.get('confPassword')
        _name = request.form.get('name')
        _email = request.form.get('email')
        _country = request.form.get('country')
        print(_username, _password,_confPassword,_name,_email,_country)
    return render_template('auth/registration.html')
