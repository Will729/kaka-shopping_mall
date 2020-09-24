# _*_ codding:utf-8 _*_
from app import create_app, db
from app.models import *
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask import render_template

app = create_app('default')
# 后续由manager.run(app) 实现传参使用命令行参数
manager = Manager(app)
#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例 迁移数据库
migrate = Migrate(app, db=db)
# migrate = Migrate(app, db)

# make_shell_context() 函数注册了程序、数据库实例以及模型，因此这些对象能直接导入 shell
def make_shell_context():
    return dict(app=app, db = db)  #？？？

#为manager 创建了应用上下文  不然manager操作数据库的时候需要from XXX import db  然后在执行db.query.****
manager.add_command('shell', Shell(make_context=make_shell_context))

#manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令  然后到入到了 models文件中使用
manager.add_command('db', MigrateCommand)

#抛出错误
@app.errorhandler(404)
def page_not_found(error):
    '''
    404
    :param error:
    :return: home/404.html
    '''
    return render_template('home/404.html')

if __name__ == '__main__':
    manager.run()
