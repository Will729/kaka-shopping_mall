# _*_ Coding:utf-8 _*_

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()

def create_app(config_name):
    # config_name ---> default
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name] --- > DevelopmentConfig  继承了 Config
    config[config_name].init_app(app)
    # Config.init_app(app)
    db.init_app(app)
    # db.init_app() db 类中定义的方法，用来初始化和那些类有关的配置。和 Config 类中的 init_app()不是一个函数。
    # 相当于 db = SQLAlchemy(app)

    #后续蓝图注册  这里顺序不能变 因为代码是按照顺序执行的，当你从其他模块导入蓝图的时候就需要 db 了，但是这个时候db 还没有生成，所以会报出错误 提示不可以从当中导入相应的模块
    from app.users import user as user_blueprint
    from app.home import home as home_blueprint
    from app.admin import admin as admin_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')


    return app