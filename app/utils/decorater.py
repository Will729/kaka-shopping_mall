# _*_ coding:utf-8 _*_
from functools import wraps

from flask import session, redirect, url_for, request


def user_login(f):
    '''登陆装饰器'''
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_func


def admin_login(f):
    '''登陆装饰器'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            # 将未知变量next添加到 URL 末尾作为查询参数
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function