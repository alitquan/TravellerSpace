import sqlite3
import re
import click
import sys
from flask import current_app, g
from flask.cli import with_appcontext
from flask_mysqldb import MySQL
import mysql.connector

def get_db(): 
    cnx = mysql.connector.connect(user='root', password='Farzana1972$',
                                  host='127.0.0.1',
                                  database='TravellerSpace')
    return cnx

def init_app(app):
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")

def init_db():
    database = get_db()
    try:
        with current_app.open_resource('schema.sql') as f:
            lines = f.readlines()
            for line in lines:
                print()
                print(line) 
            exec_sql_file(database,lines)
    except Exception:
        print ("\nError initializing database\n")
    finally:
        database.close() 

# inspired by @nonbeing https://stackoverflow.com/questions/4408714/execute-sql-file-with-python-mysqldb
def exec_sql_file (connection, lines):
    try:
        statement = ""
        cursor = connection.cursor()
        for line in lines:
            _line = line.decode('utf-8')
            _line = re.sub(r"[\n\t]*", "", _line).strip()
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
                    connection.commit()
                    # after each execution, close cursor and then reopen
                    cursor.close()
                    cursor = connection.cursor()
                except Exception as e:
                    print("\nError executing query\n")
                    print(e)
                    print()
                statement = ""
        cursor.close()
    except:
        print("\n problem executing schema \n")
    finally: 
        connection.close()

def exec_insert(query):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query)
        print("query executed")
        conn.commit()
        cursor.close()
    except Exception:
        print("\nInsert query exception; Please check query\n")
    finally:
        conn.close()

def exec_select(query):
    try:
        conn = get_db()
        cursor = conn.cursor()
        print("Query: %s " % query)
        cursor.execute(query)
        print("select query executed")
        result = cursor.fetchall()
        print("Results: %s \n" % result)
        cursor.close()
        return result
    except:
        print("\nSelect query exception; Please check query\n")
        raise 
    finally:
        conn.close()


'''
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
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.cli.add_command(init_db_command)


'''


