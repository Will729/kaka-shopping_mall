# _*_ coding:utf-8 _*_
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class SuggetionForm(FlaskForm):
    '''
    意见和建议
    '''
    name = StringField(
        label = '邮箱',
        validators=[
            DataRequired('邮箱不能为空！')
        ],
        description='邮箱',
        render_kw={
            'type':'email',
            'placeholder':'请输入邮箱',
            'class':'form-control'
        }
    )
    content = TextAreaField(
        label='意见建议',
        validators=[
            DataRequired('内容不能为空!')
        ],
        description='意见建议',
        render_kw={
            'class':'form-control',
            'placeholder':'请输入内容！',
            'rows':7
        }
    )
    submit = SubmitField(
        '发送消息',
        render_kw={
            'class':'btn-default btn-cf-submit',
        }
    )