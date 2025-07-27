import pymysql
from flask import Blueprint, render_template, redirect, jsonify, request
from unicodedata import category

category_blue=Blueprint('category_blue','__name__')

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='hyy200539',
        database='zheng'
    )
    return connection

@category_blue.route('/all_categories')
def get_category():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(' select * from  category ')
    category = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('category.html',categories= category)


@category_blue.route('/delete/<int:id>',methods=['GET'])
def delete_category(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('delete from category where category_id=%s',(id))
    connection.commit()
    cursor.close()
    connection.close()
    return  redirect('/category/all_categories')


@category_blue.route('/level/<int:level>',methods=['POST'])
def category_level(level):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select *  from category where level=%s', (level))
    connection.commit()
    cursor.close()
    connection.close()
    category = cursor.fetchall()
    return jsonify(category)

@category_blue.route('/add',methods=['POST'])
def category_add():
    json = request.get_json()
    print(json)

    category_name= json['category_name']
    level = json['level']
    parent_id =json['parent_id']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('insert into category (category_name,level,parent_id) values (%s,%s,%s)',(category_name,level,parent_id))
    connection.commit()
    cursor.close()
    connection.close()
    return  jsonify({'status':'ok'})