import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext
from flask_mysqldb import MySQL

def get_db():
    if 'db' not in g:
        g.db = MySQL (current_app)
    return g.db

def close_db(e = None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.connection.cursor()
    #with current_app.open_resource('schema.sql') as f:
    #    cursor.execute(f.read().decode('utf-8'))
    cursor.execute("insert into PERSONS(name,password) VALUES('sarah','johnson');")
    db.connection.commit()
    cursor.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    '''clear the existing data and create new tables '''
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.cli.add_command(init_db_command)
