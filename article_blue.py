import pymysql
from flask import render_template, Blueprint, request, redirect

article_blue=Blueprint('article_blue','__name__')

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='hyy200539',
        database='zheng'
    )
    return connection

@article_blue.route('/add')
def add():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(' select * from  category ')
    category = cursor.fetchall()
    return render_template('article.html',categories= category)

@article_blue.route('/save',methods=['POST'])
def save():
    editor = request.form.get('ckeditor')
    title = request.form.get('title')
    category = request.form.get('category')
    abstract = request.form.get('abstract')
    print(editor)
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('insert into article(article_title,article_content,article_category,article_abstract) values(%s,%s,%s,%s)',(title,editor,category,abstract))
    cursor.execute(' SELECT @@IDENTITY ')
    id = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return  redirect('/article/blog_detail/' + str(id[0]))

@article_blue.route('/blog_detail/<int:id>',methods=['GET'])
def blog_detail(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select  *  from  article  where  article_id=%s',(id))
    article = cursor.fetchone()


    return render_template('blog.html',article=article)


@article_blue.route('/all_articles')
def all_articles():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select  *  from  article a, category c where a.article_category=c.category_id ')
    articles = cursor.fetchall()
    return render_template('all_articles.html',articles=articles)

@article_blue.route('/delete/<int:id>',methods=['GET'])
def  delete_article(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('delete from article where article_id=%s',(id))
    connection.commit()
    cursor.close()
    connection.close()
    return  redirect('/article/all_articles')

@article_blue.route('/blog_home')
def blog_home():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select  *  from  article a limit 5 ')
    five_articles = cursor.fetchall()
    cursor.execute('select  *  from  category c  limit 10')
    categories = cursor.fetchall()

    cursor.execute('select  *  from  article c  order by article_id  desc limit 1')
    top_articles = cursor.fetchall()

    cursor.execute('select  *  from  article c  order by article_id  desc limit 2 ')
    two_articles = cursor.fetchall()
    return render_template('blog_home.html',
                           five_articles=five_articles,
                           categories=categories,
                           top_articles=top_articles,
                           two_articles=two_articles)
