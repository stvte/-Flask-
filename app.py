from flask import Flask,render_template, request
from flask_ckeditor import CKEditor

import pymysql
from users.userblue import user_blue
from article.article_blue import article_blue
from upload.upload_blueprint import upload_blue
from article.category_blue import category_blue
from book.book_blue import book_blue
app=Flask('__name__')
ckeditor = CKEditor()
ckeditor.init_app(app)
app.register_blueprint(upload_blue, url_prefix='/upload', static_folder='static',template_folder='templates')
app.register_blueprint(user_blue, url_prefix='/users', static_folder='static',template_folder='templates')
app.register_blueprint(article_blue, url_prefix='/article', static_folder='static',template_folder='templates')
app.register_blueprint(category_blue, url_prefix='/category', static_folder='static',template_folder='templates')
app.register_blueprint(book_blue, url_prefix='/book', static_folder='static',template_folder='templates')

app.config['CKEDITOR_FILE_UPLOADER'] = 'upload_blue.upload'

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='hyy200539',
        database='zheng'
    )
    return connection

@app.route('/')
def hello_world():
    return render_template('book_index.html')


@app.route('/login')
def login():
    return render_template('login.html',title='title',name='john')


@app.route('/dologin',methods=['POST'])
def dologin():

    username=request.form.get('username')
    password=request.form.get('password')
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select * from  user where username=%s and password=%s ', (username, password))
    users = cursor.fetchall()
    
    if  len(users)>0:
        cursor.execute('select * from  user ')
        users=cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('base.html',users=users)
    else:
        return render_template('login.html',error='用户名密码错误')

if  __name__ =='__main__':
    app.run()
