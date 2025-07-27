from flask import Blueprint, Flask,blueprints, render_template,request
import pymysql

user_blue = Blueprint('users','__name__')
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='hyy200539',
        database='zheng'
    )
    return connection


@user_blue.route('/query')
def user_query():
    connection =get_db_connection()
    cursor=connection.cursor()
    cursor.execute('select * from user')
    users = cursor.fetchall()

    return  render_template('user.html',users=users)


@user_blue.route('/base')
def user_base():
    return render_template('base.html')
