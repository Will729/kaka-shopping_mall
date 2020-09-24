# _*_ coding:utf-8 _*_
from io import BytesIO

from flask import make_response, session, redirect, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash

from app.utils.verifycode import get_verify_code
from . import user
from .forms import RegisterForm, LoginForm, PasswordForm
from .. import db
from ..models import User
from ..utils.decorater import user_login


@user.route('/register/', methods=['GET', 'POST'])
def register():
    '''
    注册功能
    '''
    if 'user_id' in session:
        return redirect(url_for('home.index'))
    form = RegisterForm()
    if form.validate_on_submit(): # ---> if post and dalidate
        data = form.data
        # 为User类属性赋值
        user = User(
            username = data['username'],
            email = data['email'],
            password = generate_password_hash(data['password']), # 对密码加密
            phone = data['phone']
        )
        db.session.add(user) # 添加数据
        db.session.commit() # 提交数据
        return redirect(url_for('user.register')) #登陆成功，跳转到登陆界面  之后变成 register
    return render_template('users/register.html', form=form) # 渲染模板

@user.route('/code')
def get_code():
    image, code = get_verify_code()
    #图片以而兼职形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把已经转换成而兼职的buf_str 作为response返回前端， 并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-type'] = 'image/gif'
    # 将验证码字符串储存在session 中 当提交用户登陆信息后，对比验证码是否合规
    session['image'] = code
    return response

@user.route('/login/', methods=['GET', 'POST'])
def login():
    '''
    登陆
    '''
    if 'user_id' in session:
        # session.pop("user_id", None)
        # session.pop("username", None)
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        # 判断验证码
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('验证码错误', 'err')
            return render_template('users/login.html', form=form) #验证码不对 返回登陆界面
        user = User.query.filter_by(username=data['username']).first() # 获取用户信息
        if not user:
            flash('用户名不存在！', 'err')
            return render_template('users/login.html') #返回登陆首页

        if not user.check_password(data['password']):
    # 调用check_password()方法，检测用户名密码是否匹配
            flash('密码错误！', 'err')
            return render_template('users/login.html')
        #如果以上都过了，证明登陆成功了
        session['user_id'] = user.id
        # user_id 写入session， 后面用户判断用户是否登陆
        session['username'] = user.username
        # 将username写入session, 后面做调用
        return redirect(url_for('home.index')) # 登陆成功，跳转到首页
        # return 'ok'
    return render_template('users/login.html', form=form) # form中信息校验不通过， 返回登陆界面


@user.route('/modify_password/', methods=['GET', 'POST'])
@user_login
def modify_password():
    '''修改密码'''
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=session['username']).first()
        from werkzeug.security import generate_password_hash
        user.password = generate_password_hash(data['password'])
        db.session.add(user)
        db.session.commit()
        return "<script>alert('密码修改成功');location.href='/';</script>" # 跳转回首页
    return render_template('users/modify_password.html', form=form)

@user.route('/logout/')
def logout():
    '''
    退出登陆
    '''
    # 从定向到 user 模块下的登陆
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('user.login'))





