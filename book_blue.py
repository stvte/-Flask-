import datetime
from pathlib import Path

import pymysql
from flask import Blueprint, request, redirect, render_template, url_for

book_blue = Blueprint('book_blue',__name__)
PROJECT_ROOT = Path(__file__).parent.parent
UPLOAD_DIR = PROJECT_ROOT / "static/uploaded"

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='hyy200539',
        database='zheng'
    )
    return connection


@book_blue.route('/add',methods=['POST'])
def book_add():
    book_name = request.form['book_name']
    book_author = request.form['book_author']
    book_publisher = request.form['book_publisher']

    files = request.files.getlist('file')
    img =[]
    for f in files:
        extension = f.filename.split('.')[1].lower()

        now = datetime.datetime.now()

        milliseconds = now.microsecond // 1000

        formatted_time = now.strftime("%Y%m%d%H%M%S") + f"{milliseconds:03d}"
        filename = formatted_time + '.' + extension
        save_path = UPLOAD_DIR / filename
        save_path = UPLOAD_DIR / filename
        f.save(str(save_path))
        url = url_for('upload_blue.uploaded_files', filename=filename)
        img.append(url)
    print(img)
    book_abstract = request.form['book_abstract']
    book_price = request.form['book_price']
    book_publish_date = request.form['book_publish_date']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''insert into book(book_name, book_author, book_publisher,book_img,
                                              book_abstract,book_price,book_publish_date,
                                               book_img1,book_img2,book_img3,book_img4) 
                                               values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                (book_name,book_author,book_publisher,img[0],
                                                       book_abstract,book_price,book_publish_date,
                                                        img[1],img[2],img[3],img[4]))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect('/book/all_books')

@book_blue.route('/all_books')
def book_all():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select * from book')
    book = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('allbook.html',books=book)

@book_blue.route('/delete/<int:id>')
def book_delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('delete from book where book_id=%s',(id))
    connection.commit()
    cursor.close()
    connection.close()
    return  redirect('/book/all_books')

@book_blue.route('/addbook')
def book_page():
    return render_template('addbook.html')

@book_blue.route('/book_detail/<int:id>')
def book_detail(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select * from book  where  book_id=%s',(id))
    book = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('book_detail.html',book=book[0])