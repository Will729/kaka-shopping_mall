# _*_ coding:utf-8 _*_

from flask import Blueprint

user = Blueprint('user', __name__)

import app.users.views