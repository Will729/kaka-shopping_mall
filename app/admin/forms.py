from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, RadioField, TextAreaField, \
    FileField
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin


class LoginForm(FlaskForm):
    '''
    管理员登陆表单
    '''
    manager = StringField(
        label='管理员名',
        validators=[
            DataRequired('管理员名不能为空！')
        ],
        description='管理员名',
        render_kw={
            'class':'manager',
            'placeholder':'输入管理员名',
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('密码不能为空'),
        ],
        description='密码',
        render_kw={
            'class':'password',
            'placeholder':'请输入密码',
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': 'login_ok',
        }
    )

    # 验证账号，命名规则：validate_ + 字段名。如果要验证密码，则可以创建函数validate_pwd
    def validate_manager(self, field):
        account = field.data
        admin = Admin.query.filter_by(manager=account).count()
        if admin == 0:
            raise ValidationError('账号不存在！')

# 商品录入表单
class GoodsForm(FlaskForm):
    name = StringField(
        label='商品名称',
        validators=[
            DataRequired('商品名称不能为空！'),
        ],
        description='商品名称',
        render_kw={
            'class': 'Style_text',
            'placeholder': '请输入商品名称！',
            'size': '50'
        }
    )
    # 表名 + 字段
    supercat_id = SelectField(
        label='大分类',
        validators=[
            DataRequired('请选择大分类！')
        ],
        coerce=int,
        description='大分类',
        render_kw={
            'class':'form-control'
        }
    )
    subcat_id = SelectField(
        label='小分类',
        validators=[
            DataRequired('请选择小分类！'),
        ],
        coerce=int,
        description='小分类',
        render_kw={
            'class': 'form-control',
        }
    )
    picture = StringField(
        label='图片名称',
        validators=[
            DataRequired('图片名称不能为空！')
        ],
        description='图片名称',
        render_kw={
            'class': 'Style_upload',
            'placeholder':'请输入图片名称！'
        }
    )
    pic_file = FileField(
        label='图片文件',
        validators=[
            DataRequired('图片不能为空！')
        ],
        description='图片文件',
        render_kw={
            'class': 'Style_upload',
            'placeholder': '请选择上传文件！',
        }
    )
    original_price = DecimalField(
        label='商品价格',
        validators=[
            DataRequired('请输入正确的价格类型')
        ],
        description='商品价格',
        render_kw={
            'class': 'Style_text',
            'placeholder': '请输入商品价格！'
        }
    )
    current_price = DecimalField(
        label='商品现价',
        validators=[
            DataRequired('商品现价不能为空！')
        ],
        description='商品现价',
        render_kw={
            'class': 'Style_text',
            'palceholder': '请输入商品现价！'
        }
    )
    is_new = RadioField(
        label = '是否新品',
        description = '是否新品',
        coerce = int,
        choices=[(0, '否'), (1, '是')],
        default=0,
        render_kw={
            'class': 'is_radio'
        }
    )
    is_sale = RadioField(
        label = '是否特价',
        description = '是否特价',
        coerce = int,
        choices = [(0, '否'), (1, '是')],
        default = 0,
        render_kw={
            'class': 'is_radio'
        }
    )
    introduction = TextAreaField(
        label='商品简介',
        validators=[
            DataRequired('商品简介不能为空！')
        ],
        description='商品简介',
        render_kw={
            'class':'textarea',
            'rows': 5
        }
    )
    submit = SubmitField(
        '保存',
        render_kw={
            'class':'btn_bg_short'
        }
    )

