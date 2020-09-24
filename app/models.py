from datetime import datetime

from . import db

# 定义模型Role
# 会员数据模型

class User(db.Model):
    #定义表名
    __tablename__ = 'user'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True) #序号
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    consumption = db.Column(db.DECIMAL(10,2),default=0) #消费额
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) #注册时间 创建索引 优化搜索
    orders = db.relationship('Orders', backref='user') #订单外键关系关联

    # repr()方法显示一个可读字符串，
    def __repr__(self):
        return f'<User {self.name}>' # 或username


    def check_password(self, password):
        '''
        check_password方法接受一个参数(即密码)，将其传给 Werkzeug 提供的 check_ password_hash() 函数，与存储在 User 模型中的密码散列值进行比对。如果这个方法返回 True，表明密码是正确的。
        :param password: 密码
        :return: 返回布尔值
        '''
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    manager = db.Column(db.String(100), unique=True) #管理员账号设置成唯一，由于admin没有注册功能，所以录入数据库要检查
    password = db.Column(db.String(100))

    def __repr__(self):
        return f'<Admin {self.manager}>'

    def check_password(self,password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

#商品大品类分类
class SuperCat(db.Model):
    __tablename__ = 'supercat'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100)) # 大分类名称
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) #添加时间
    subcat = db.relationship('SubCat', backref='supercat') #外键关联
    goods = db.relationship('Goods', backref='supercat') #外键关系关联

    def __repr__(self):
        return f'<SuperCat {self.cat_name}>'

# 商品小类别
class SubCat(db.Model):
    __tablename__ = 'subcat'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    super_cat_id = db.Column(db.Integer, db.ForeignKey('supercat.id')) #所属大分类
    goods = db.relationship('Goods', backref='subcat')

    def __repr__(self):
        return f'<SubCat {self.cat_name}>'

# 商品列表
class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True) #编号
    name = db.Column(db.String(255))
    original_price = db.Column(db.DECIMAL(10,2)) #商品原价
    current_price = db.Column(db.DECIMAL(10,2)) # 商品现在价格
    picture = db.Column(db.String(255)) #图片
    introduction = db.Column(db.Text) #商品简介
    views_count = db.Column(db.Integer, default=0) #浏览次数
    is_sale = db.Column(db.Boolean(),default=0) #是否特价
    is_new = db.Column(db.Boolean(), default=0) #是否新品

    # 设置外键
    supercat_id = db.Column(db.Integer, db.ForeignKey('supercat.id')) #所属大类别
    subcat_id = db.Column(db.Integer, db.ForeignKey('subcat.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) #添加时间
    cart = db.relationship('Cart', backref='goods') #购物车外键关系关联 在Cart类中创建了一个goods属性，帮助确认外键
    orders_detail = db.relationship('OrdersDetail', backref='goods') #订单外键关系关联

    def __repr__(self):
        return f'<Goods {self.name}>'

#购物车
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True) #编号
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id')) #创建外键 与 Goods中的 backref呼应
    user_id = db.Column(db.Integer) #所属用户
    number = db.Column(db.Integer, default=0) # 购买数量
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return f'<Cart {self.id}>'


#订单
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True) # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #所属用户
    recevie_name = db.Column(db.String(255)) #收款人姓名
    recevie_address = db.Column(db.String(255)) #收款人地址
    recevie_tel = db.Column(db.String(255)) #收款人电话
    remark = db.Column(db.DateTime, index=True, default=datetime.now)
    orders_deteil = db.relationship('OrdersDetail', backref='orders')
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) # 添加时间

    def __repr__(self):
        return f'<Orders {self.id}>'

class OrdersDetail(db.Model):
    __tablename__ = 'orders_detail'
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id')) #所属商品
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id')) #所属订单
    number = db.Column(db.Integer, default=0) # 购买数量
