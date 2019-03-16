"""__author__ = 干友恒"""
from re import fullmatch

from flask import request, render_template, session, \
    Blueprint, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import db, User, Article, ArticleType, UserInform
from utils.function import is_login

# 生成蓝图对象
back_blue = Blueprint('back', __name__)


@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    db.create_all()
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 获取从注册页面传来的数据
        username = request.form.get('username')
        password = request.form.get('password')
        affirm_password = request.form.get('password2')

        if username and password and affirm_password:

            user = User.query.filter(User.username == username).first()

            if user:
                error = '该用户已存在，请重新输入用户名!'
                return render_template('back/register.html', error=error)

            if password != affirm_password:
                error = '两次密码不一致，请重新输入!'
                return render_template('back/register.html', error=error)

            user = User()
            user.username = username
            user.password = generate_password_hash(password)

            user.save()

            user_inform = UserInform()
            user_inform.name = 'QF' + username
            user_inform.user_id = user.id
            user_inform.save()

            return redirect(url_for('back.login'))
        else:
            error = '请填写完整的注册信息！'
            return render_template('back/register.html', error=error)


@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:

            user = User.query.filter(User.username == username).first()

            if not user:
                error = '该账号不存在，请注册!'
                return render_template('back/login.html', error=error)

            if not check_password_hash(user.password, password):
                error = '密码输入错误，请重新输入!'
                return render_template('back/login.html', error=error)

            session['user.id'] = user.id

            return redirect(url_for('back.index'))

        else:
            error = '请填写完整的登录信息！'
            return render_template('back/login.html', error=error)


@back_blue.route('/index/')
@is_login
def index():
    return render_template('back/index.html')


@back_blue.route('/logout/')
@is_login
def logout():
    del session['user.id']
    return redirect(url_for('back.login'))


@back_blue.route('/a_type/', methods=['GET', 'POST'])
def a_type():
    if request.method == 'GET':
        userid = session['user.id']
        types = ArticleType.query.filter(ArticleType.user_id == userid).all()
        return render_template('back/category_list.html', types=types)


@back_blue.route('/add_type/', methods=['GET', 'POST'])
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')

        if atype:
            art_type = ArticleType()
            art_type.art_name = atype
            art_type.user_id = session['user.id']

            art_type.save()

            return redirect(url_for('back.a_type'))
        else:
            error = '请填写分类信息'
            return render_template('back/category_add.html', error=error)


@back_blue.route('/del_type/<int:id>/', methods=['GET'])
def del_type(id):
    atype = ArticleType.query.get(id)

    atype.delete()
    return redirect(url_for('back.a_type'))


@back_blue.route('/article_list/', methods=['GET'])
def article_list():
    userid = session['user.id']
    articles = Article.query.filter(Article.user_id == userid).all()
    return render_template('back/article_list.html', articles=articles)


@back_blue.route('/article_add/', methods=['GET', 'POST'])
def article_add():
    if request.method == 'GET':
        userid = session['user.id']
        types = ArticleType.query.filter(ArticleType.user_id == userid).all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        userid = session['user.id']

        if title and desc and category and content:
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type_id = category
            art.user_id = userid

            art.save()

            return redirect(url_for('back.article_list'))

        else:
            error = '请填写完整的文章信息!'
            userid = session['user.id']
            types = ArticleType.query.filter(ArticleType.user_id == userid).all()
            return render_template('back/article_detail.html', types=types, error=error)


@back_blue.route('/del_article/<int:id>/', methods=['GET'])
def del_article(id):
    del_art = Article.query.get(id)

    del_art.delete()
    return redirect(url_for('back.article_list'))


@back_blue.route('/ed_article/<int:id>', methods=['GET', 'POST'])
def ed_article(id):
    if request.method == 'GET':
        userid = session['user.id']
        ed_art = Article.query.filter(Article.user_id == userid, Article.id == id).first()
        types = ArticleType.query.filter(ArticleType.user_id == userid).all()
        return render_template('back/article_editor.html', ed_art=ed_art, types=types)
    if request.method == 'POST':
        userid = session['user.id']
        ed_art = Article.query.filter(Article.user_id == userid and Article.id == id).first()
        types = ArticleType.query.filter(ArticleType.user_id == userid).all()

        new_title = request.form.get('title')
        new_desc = request.form.get('desc')
        new_category = request.form.get('category')
        new_content = request.form.get('content')

        if new_title and new_desc and new_category and new_content:
            new_art = Article.query.filter(Article.user_id == userid, Article.id == id).first()
            new_art.title = new_title
            new_art.desc = new_desc
            new_art.content = new_content
            new_art.type_id = new_category

            new_art.save()

            return redirect(url_for('back.article_list'))

        else:
            error = '请填写完整的文章信息!'
            return render_template('back/article_editor.html', ed_art=ed_art, types=types, error=error)


@back_blue.route('/user_inform/', methods=['GET'])
def user_inform():
    if request.method == 'GET':
        userid = session['user.id']
        userinform = UserInform.query.filter(UserInform.user_id == userid).first()
        return render_template('back/user_inform.html', userinform=userinform)


@back_blue.route('/add_user_inform/', methods=['GET', 'POST'])
def user_inform_editor():
    if request.method == 'GET':
        userid = session['user.id']
        userinform = UserInform.query.filter(UserInform.user_id == userid).first()
        return render_template('back/user_inform_editor.html', userinform=userinform)
    if request.method == 'POST':
        userid = session['user.id']
        userinform = UserInform.query.filter(UserInform.user_id == userid).first()

        new_name = request.form.get('name')
        new_sex = request.form.get('sex')
        new_birth = request.form.get('birth')
        new_tel = request.form.get('tel')
        new_email = request.form.get('email')
        new_city = request.form.get('city')

        if not new_name:
            error = '请填写不为空的新用户名!'
            return render_template('back/user_inform_editor.html', userinform=userinform, error=error)
        existinform = UserInform.query.filter(UserInform.name == new_name).first()
        if not existinform:
            userinform.name = new_name
            if new_sex == '男':
                userinform.sex = 0
            else:
                userinform.sex = 1

            re_str = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])'
            if not fullmatch(re_str, new_birth):
                userinform.birth = new_birth
                userinform.tel = new_tel
                userinform.email = new_email
                userinform.city = new_city

                userinform.save()

                return redirect(url_for('back.user_inform'))
            error = '生日格式不对，请重新输入!'
            return render_template('back/user_inform_editor.html', userinform=userinform, error=error)

        userinform.name = new_name
        if new_sex == '男':
            userinform.sex = 0
        else:
            userinform.sex = 1

        re_str = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])'
        if not fullmatch(re_str, new_birth):
            userinform.birth = new_birth
            userinform.tel = new_tel
            userinform.email = new_email
            userinform.city = new_city

            userinform.save()

            return redirect(url_for('back.user_inform'))
        error = '生日格式不对，请重新输入!'
        return render_template('back/user_inform_editor.html', userinform=userinform, error=error)


@back_blue.route('/update_password/', methods=['GET', 'POST'])
def update_password():
    if request.method == 'GET':
        return render_template('back/update_password.html')
    if request.method == 'POST':
        userid = session['user.id']
        user = User.query.get(userid)

        oldpassword = request.form.get('old_password')
        newpassword = request.form.get('new_password')
        newpassword2 = request.form.get('new_password2')

        if oldpassword and newpassword and newpassword2:
            if not check_password_hash(user.password, oldpassword):
                error = '请输入正确的旧密码!'
                return render_template('back/update_password.html', error=error)
            if oldpassword == newpassword:
                error = '请输入新的密码!'
                return render_template('back/update_password.html', error=error)
            if newpassword != newpassword2:
                error = '请保持新密码和确认密码一致!'
                return render_template('back/update_password.html', error=error)
            user.password = generate_password_hash(newpassword)
            user.save()

            return redirect(url_for('back.index'))
        else:
            error = '请填写完整的信息!'
            return render_template('back/update_password.html', error=error)


