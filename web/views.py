"""__author__ = 干友恒"""

from flask import Blueprint, render_template, session

from back.models import UserInform, Article, ArticleType

web_blue = Blueprint('web', __name__)


@web_blue.route('/index/')
def index():
    userid = session['user.id']
    inform = UserInform.query.filter(UserInform.user_id == userid).first()
    articles = Article.query.filter(Article.user_id == userid).all()
    return render_template('web/index.html', inform=inform, articles=articles)


@web_blue.route('/learn/<int:page>')
def learn(page):
    userid = session['user.id']
    inform = UserInform.query.filter(UserInform.user_id == userid).first()
    all_articles = Article.query.filter(Article.user_id == userid).all()
    if len(all_articles) % 8:
        pages = len(all_articles) // 8 + 1
    else:
        pages = len(all_articles) // 8
    articles = all_articles[(page-1)*8: page*8]
    types = ArticleType.query.filter(ArticleType.user_id == userid).all()
    return render_template('web/learn.html', inform=inform, articles=articles, types=types, pages=pages)


@web_blue.route('/about/')
def about():
    userid = session['user.id']
    inform = UserInform.query.filter(UserInform.user_id == userid).first()
    return render_template('web/about.html', inform=inform)


@web_blue.route('/content/<int:id>')
def content(id):
    userid = session['user.id']
    inform = UserInform.query.filter(UserInform.user_id == userid).first()
    article = Article.query.get(id)
    return render_template('web/content.html', inform=inform, article=article)


@web_blue.route('/type_find/<int:id>/<int:page>')
def type_find(id, page):
    userid = session['user.id']
    inform = UserInform.query.filter(UserInform.user_id == userid).first()
    all_type_articles = Article.query.filter(Article.type_id == id).all()
    if len(all_type_articles) % 8:
        pages = len(all_type_articles) // 8 + 1
    else:
        pages = len(all_type_articles) // 8
    type_articles = all_type_articles[(page - 1) * 8: page * 8]
    return render_template('web/type.html', inform=inform, type_articles=type_articles, id=id, pages=pages)


@web_blue.route('/gbook/')
def gbook():
    userid = session['user.id']
    inform = UserInform.query.filter(UserInform.user_id == userid).first()
    return render_template('web/gbook.html', inform=inform)

