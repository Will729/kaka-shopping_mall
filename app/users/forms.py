# _*_ coding:utf-8 _*_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp, EqualTo, ValidationError, Length, Email, email_validator
from app.models import User
import email_validator

class RegisterForm(FlaskForm):
    """
    用户注册表单
    """
    username = StringField(
        label='账户：',
        validators=[
            DataRequired('用户名不能为空！'),
            Length(min=3, max=50, message='用户名长度必须在3-10位之间')
        ],
        # css 渲染
        description='用户名',
        render_kw={
            'type':'text',
            'placeholder':'请输入用户名',
            'class':'validate-username',
            'size':38
        }
    )
    phone = StringField(
        label='联系电话：',
        validators=[
            DataRequired('手机号不能为空！'),
            Regexp('1[2345678][0-9]{9}',message='手机号码格式不正确')
        ],
        description='手机号',
        render_kw={
            'type':'text',
            'placeholder':'请输入联系电话',
            'size':38
        }
    )
    email = StringField(
        label="邮箱 ：",
        validators=[
            DataRequired("邮箱不能为空！"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "type": "email",
            "placeholder": "请输入邮箱！",
            "size": 38,
        }
    )
    password = PasswordField(
        label='密码：',
        validators=[
            DataRequired('密码不能为空！')
        ],
        description='密码',
        render_kw={
            'placeholder':'请输入密码！',
            'size':38
        }
    )
    repassword = PasswordField(
        label='确认密码：',
        validators=[
            DataRequired('请输入密码！'),
            EqualTo('password', message='两次密码不一致！')
        ],
        description='确认密码',
        render_kw={
            'placeholder':'请输入确认密码！',
            'size':38
        }
    )
    submit = SubmitField(
        '同一协议定注册',
        render_kw={
            'class':'btn btn-primary login',
        }
    )

    #wtfform 没有到数据库查重邮箱和电话的配置，只有用户名的，所以使用自定义校验规则 vilidate_变量名
    def vilidate_email(self, field):
        '''
        检测注册邮箱是否已经存在
        :param field: 字段名
        '''
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError('邮箱已经存在！') #抛出异常

    def vilidate_phone(self, field):
        '''
        检测注册手机是否已经存在
        :param field: 字段名
        '''
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError('手机号已经存在！')

class LoginForm(FlaskForm):
    '''
    登陆功能
    '''
    username = StringField(
        validators=[
            DataRequired('用户名不能为空！'),
            Length(min=3, max=50, message='用户名长度必须在3-10位之间')
        ],
        description='用户名',
        render_kw={
            'type':'text',
            'placeholder':'请输入用户名',
            'class':'validate-username',
            'size':'38',
            'maxlength':99
        }
    )
    password = PasswordField(
        validators=[
            DataRequired('密码不能为空！'),
            Length(min=3,message='密码长度不少于6位')
        ],
        description='密码',
        render_kw={
            'type':'password',
            'placeholder':'请输入密码！',
            'size':38,
            'maxlength':99
        }
    )
    verify_code = StringField(
        'VerifyCode',
        validators=[DataRequired()],
        render_kw={
            'class':'validate-code',  # flask里边封装了可以验证的函数
            'size':18,
            'maxlength':4,
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': 'btn btn-primary login'
        }
    )

class PasswordForm(FlaskForm):
    '''
    修改密码表单
    '''
    old_password = PasswordField(
        label='原始密码：',
        validators=[
            DataRequired('原始密码不能为空!')
        ],
        description='原始密码',
        render_kw={
            'placeholder':'请输入原始密码',
            'size':38
        }
    )
    password = PasswordField(
        label='新密码：',
        validators=[
            DataRequired('新密码不能为空!')
        ],
        description='新密码',
        render_kw={
            'placeholder':'请输入新密码',
            'size':38,
        }
    )
    repassword = PasswordField(
        label='确认密码：',
        validators=[
            DataRequired('请输入确认密码'),
            EqualTo('password', message='两次密码不一致!')
        ],
        description='确认密码',
        render_kw={
            'placeholder':'请输入确认密码！',
            'size':38
        }
    )
    submit = SubmitField(
        '确认修改',
        render_kw={
            "class": "btn btn-primary login",
        }
    )
    # 自定义校验
    # 提交按钮后  自动触发旧密码校验如果通过才返回True
    def validate_old_password(self, field):
        from flask import session
        old_password = field.data
        user_id = session['user_id']
        user = User.query.get(int(user_id)) # 拿到user_id这条数据
        if not user.check_password(old_password):
            raise ValidationError('原始密码错误！')



