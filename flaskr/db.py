import sqlite3
import re
import click
import sys
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
    conn = db.connection
    with current_app.open_resource('schema.sql') as f:
        lines = f.readlines()
        for line in lines:
            print()
            print(line) 
        exec_sql_file(conn, lines) 
    #cursor.execute("insert into PERSONS(name,password) VALUES('sarah','johnson');")
    conn.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    '''clear the existing data and create new tables '''
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.cli.add_command(init_db_command)

def exec_query(query):
    db = get_db()
    cursor = db.connection.cursor()
    cursor.execute(query)
    cursor.close()

# inspired by @nonbeing https://stackoverflow.com/questions/4408714/execute-sql-file-with-python-mysqldb
def exec_sql_file (connection, lines):
    statement = ""
    cursor = connection.cursor()
    for line in lines:
        _line = line.decode('utf-8')
        _line = re.sub(r"[\n\t]*", "", _line)
        print("\n"+ "After decoding: ")
        print(_line)
        print()
        if re.match(r'--', _line):  # ignore sql comment lines
            continue
        if not re.search(r';$', _line):  # keep appending lines that don't end in ';'
            statement = statement + str(_line)
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + str(_line)
            try:
                cursor.execute(statement)
                # after each execution, close cursor and then reopen
                cursor.close()
                cursor = connection.cursor()
            except Exception as e:
                print()
                print(e)
                print()
            statement = ""
    cursor.close()




def exec_sql_file2(cursor, sql_file):
    print ("\n[INFO] Executing SQL script file: '%s'" % (sql_file))
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r';$', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                cursor.execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print ("\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args)))

            statement = ""

