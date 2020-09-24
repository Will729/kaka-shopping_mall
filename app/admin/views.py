import os
import string
from decimal import Decimal
from functools import wraps
import random

from flask import session, redirect, url_for, request, flash, render_template, jsonify
from sqlalchemy import or_, func, desc

from app import db
from app.admin import admin
from app.admin.forms import LoginForm, GoodsForm
from app.models import Admin, Goods, SuperCat, SubCat, User, Orders, OrdersDetail
from app.utils.decorater import admin_login
from app.utils.urlforback import redirect_back


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    '''
    登陆功能
    :return:
    '''
    # 判断是否已经登陆
    if 'admin' in session:
        return redirect(url_for('admin.index'))
    form = LoginForm() # 实例化登陆表单
    if form.validate_on_submit():
        data = form.data # 接收数据
        admin  = Admin.query.filter_by(manager=data['manager']).first() # 查找Admin 表数据
        # 密码错误时， check_password, 则此时not check_password(data['pwd'])为真
        if not admin.check_password(data['password']):
            flash('密码错误！', 'err') # 闪存信息
            return redirect(url_for('admin.login'))
        # 如果是正确的，就要定义session的会话进行保存。
        session['admin'] = data['manager']
        session['admin_id'] = admin.id
        return redirect(url_for('admin.index')) # 返回后台主页
    return render_template('admin/login.html', form=form)

@admin.route('/logout/')
@admin_login
def logout():
    '''后台注销登陆'''
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))

@admin.route('/')
@admin_login
def index():
    page = request.args.get('page', 1, type=int)
    page_data = Goods.query.order_by(Goods.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/index.html', page_data=page_data)

@admin.route('/goods/add/', methods=['GET', 'POST'])
@admin_login
def goods_add():
    '''添加商品'''
    form = GoodsForm()  # 实例化form表单
    supercat_list = [(sup.id, sup.cat_name) for sup in SuperCat.query.all()] # 为大分类super_cat_id添加属性
    form.supercat_id.choices = supercat_list # 为大分类标签添加选项
    # print(supercat_list)
    form.subcat_id.choices = [(sub.id, sub.cat_name) for sub in SubCat.query.filter_by(super_cat_id=supercat_list[0][0]).all()] # 先默认选00 在通过前端get请求区分选了哪个小分类
    form.current_price.data = form.data['original_price'] # 为current_price 赋值 默认让现价等于原价
    if form.validate_on_submit(): # 验证通过 添加商品情况
        data = form.data
        # 实现图片上传并储存 入库
        # 生成随机字符串，防止图片名字重复
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        pic_file = request.files['pic_file']
        basedir = '/Users/mac/Desktop/MyPyPro/Pro/shopping_mall_pro/app'
        path = basedir + "/static/images/goods/"
        # 图片名称 给图片重命名 为了图片名称的唯一性
        pic_file_name = ran_str +'.'+ (pic_file.filename).split('.')[-1]
        #图片path和名称组成图片的保存路径
        file_path = path+pic_file_name
        # 保存图片
        pic_file.save(file_path)

        goods = Goods(
            name = data['name'],
            supercat_id = int(data['supercat_id']),
            subcat_id = int(data['subcat_id']),
            # 替换成新命名的图片名称
            picture=pic_file_name,
            original_price=Decimal(data['original_price']).quantize(Decimal('0.00')), # 转化为包含2位小数的形式
            current_price=Decimal(data['current_price']).quantize(Decimal('0.00')),
            is_new=int(data['is_new']),
            is_sale=int(data['is_sale']),
            introduction=data['introduction']
        )
        db.session.add(goods)
        db.session.commit()
        return redirect(url_for('admin.index'))
    return render_template('admin/goods_add.html', form=form) # get请求渲染模板

@admin.route('/goods/detail/', methods=['GET', 'POST'])
@admin_login
def goods_detail():
    '''商品详情'''
    goods_id = request.args.get('goods_id')
    goods = Goods.query.filter_by(id=goods_id).first_or_404()
    return render_template('admin/goods_detail.html', goods=goods)

@admin.route('/godds/edit/', methods=['GET', 'POST'])
@admin_login
def goods_edit():
    '''编辑商品'''
    id = request.args.get('id',type=int)
    page = request.args.get('page',type=int)
    # print('page',page)
    # print(request.args)
    # print('id',id)
    goods = Goods.query.get_or_404(id)
    form = GoodsForm() #实例化form表单
    form.supercat_id.choices = [(sup.id, sup.cat_name) for sup in SuperCat.query.all()] # 为super_cat_id 添加属性
    form.subcat_id.choices = [(sub.id, sub.cat_name) for sub in SubCat.query.filter_by(super_cat_id=goods.supercat_id).all()]

    if request.method == 'GET':
        form.name.data = goods.name
        form.picture.data = goods.picture
        form.current_price.data = goods.current_price
        form.original_price.data = goods.original_price
        form.supercat_id.data = goods.supercat_id
        form.subcat_id.data = goods.subcat_id
        form.is_new.data = goods.is_new
        form.is_sale.data = goods.is_sale
        form.introduction.data = goods.introduction
    elif form.validate_on_submit():
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        pic_file = request.files['pic_file']
        basedir = '/Users/mac/Desktop/MyPyPro/Pro/shopping_mall_pro/app'
        path = basedir + "/static/images/goods/"
        # 图片名称 给图片重命名 为了图片名称的唯一性
        pic_file_name = ran_str + '.' + (pic_file.filename).split('.')[-1]
        # 图片path和名称组成图片的保存路径
        file_path = path + pic_file_name
        # 保存图片
        pic_file.save(file_path)
        # 删除原来图片 ahVRnM8c4sAz9fXF
        old_file_path = path + goods.picture
        os.remove(old_file_path)

        goods.name = form.data['name']
        goods.supercat_id = int(form.data['supercat_id'])
        goods.subcat_id = int(form.data['subcat_id'])
        goods.picture = pic_file_name
        goods.original_price = Decimal(form.data['original_price']).quantize(Decimal('0.00'))
        goods.current_price = Decimal(form.data['current_price']).quantize(Decimal('0.00'))
        goods.is_new = int(form.data['is_new'])
        goods.is_sale = int(form.data['is_sale'])
        goods.introduction = form.data['introduction']
        db.session.add(goods)
        db.session.commit()
        return redirect(url_for('admin.index',page=page)) # 跳转页面  如果想跳转回原来页面，那么请求时候需要带着page 信息  然后此处回复携带 page 信息
    return render_template('admin/goods_edit.html', form=form)

@admin.route('/goods/select_sub_cat/', methods=['GET'])
@admin_login
def select_sub_cat():
    '''
    查找子分类
    '''
    super_id = request.args.get('super_id', '') #接受前端get请求传递过来的参数
    subcat = SubCat.query.filter_by(super_cat_id = super_id).all()
    result = {}
    if subcat:
        data = []
        for item in subcat:
            data.append({'id':item.id, 'cat_name':item.cat_name})
            # 前端把id 给value
        result['status'] = 1
        result['message'] = 'ok'
        result['data'] = data
    else:
        result['status'] = 0
        result['message'] = 'error'
    return jsonify(result) # 返回json数据

@admin.route('/goods/del_confirm/')
@admin_login
def goods_del_confirm():
    '''确认删除商品'''
    goods_id = request.args.get('goods_id')
    goods = Goods.query.filter_by(id=goods_id).first_or_404()
    return render_template('admin/goods_del_confirm.html', goods=goods)

@admin.route('/goods/del/<int:id>/', methods=['GET'])
@admin_login
def goods_del(id=None):
    '''
    删除商品
    :param id: 商品ID
    :return:
    '''
    goods = Goods.query.get_or_404(id)
    db.session.delete(goods)
    db.session.commit()
    return redirect(url_for('admin.index', page=1))

@admin.route('/user/list/')
@admin_login
def user_list():
    '''
    会员列表
    :return:
    '''
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '', type=str)
    print(keyword)
    if keyword:
        # # 根据姓名或邮箱查询
        # page_data = or_(User.username.like('%'+keyword+'%'), User.email.like('%'+keyword+'%')).order_by(User.addtime.desc()).paginate(page=page, per_page=5)
        #   模糊查找失败  暂停
        # # 可以精确查找
        # 根据姓名或者邮箱查询
        filters = or_(User.username == keyword, User.email == keyword)
        page_data = User.query.filter(filters).order_by(
            User.addtime.desc()
        ).paginate(page=page, per_page=5)
    else:
        page_data = User.query.order_by(User.addtime.desc()).paginate(page=page, per_page=5)

    return render_template('admin/user_list.html', page_data=page_data)

@admin.route('/supercat/list/', methods=['GET'])
@admin_login
def supercat_list():
    '''大分类列表 大分类信息管理'''
    #以添加时间为分组依据查询所有大分类
    data = SuperCat.query.order_by(SuperCat.addtime.desc()).all()
    return render_template('admin/supercat.html',data=data) #数据返回前端 渲染页面

@admin.route('/supercat/add/', methods=['GET', 'POST'])
@admin_login
def supercat_add():
    '''添加大分类'''
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        supercat = SuperCat.query.filter_by(cat_name=cat_name).count()
        if supercat:
            flash('大分类已存在', 'err')
            return redirect(url_for('admin.supercat_add'))
        data = SuperCat(
            cat_name = cat_name
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('admin.super_list'))
    return render_template('admin/supercat_add.html')

@admin.route('/supercat/del/', methods=['POST'])
@admin_login
def supercat_del():
    '''删除大分类'''
    if request.method == 'POST':
        cat_ids = request.form.getlist('delid') # cat_ids 是一个列表
        # 判断是否有子类 如果有子类因为是外键关联，需要先删除子类
        for id in cat_ids:
            count = SubCat.query.filter_by(super_cat_id=id).count()
            if count:
                return "<script>alert('大分类下有小分类，请先删除小分类');history.go(-1);</script>"
                # return '大分类下有小分类，请先删除先分类'
            # 使用in_ 方式批量删除，需要设置synchronize_session为False,而 in 操作估计还不支持
            # 解决办法就是删除时不进行同步，然后再让 session 里的所有实体都过期
            db.session.query(SuperCat).filter(SuperCat.id.in_(cat_ids)).delete(synchronize_session=False)
            db.session.commit()
            return redirect(url_for('admin.supercat_list'))

@admin.route('/subcat/list/', methods=['GET'])
@admin_login
def subcat_list():
    '''小分类列表'''
    data = SubCat.query.order_by(SubCat.addtime.desc()).all()
    return render_template('admin/subcat.html', data=data)

@admin.route('/subcat/add/', methods=['GET', 'POST'])
@admin_login
def subcat_add():
    ''' 添加小分类 '''
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        super_cat_id = request.form['super_cat_id']
        #检测名称是否存在
        subcat = SubCat.query.filter_by(cat_name=cat_name).count()
        if subcat:
            return "<script>alert('该小分类已经存在');history.go(-1);</script>"

        #不重名 数据就录入
        data = SubCat(
            super_cat_id = super_cat_id,
            cat_name = cat_name,
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('admin.subcat_list'))


@admin.route('/subcat/del/', methods=['POST'])
@admin_login
def subcat_del():
    '''删除小分类'''
    if request.method == 'POST':
        cat_ids = request.form.getlist('delid') # cat_ids 是一个列表
        for id in cat_ids:
            count = Goods.query.filter_by(cat_id=id).count()
            if count:
                return "<script>alert('该分类下有商品，请先删除分类下的商品');history.go(-1);</script>"

        # 使用in_ 方式批量删除，需要设置synchronize_session为False,而 in 操作估计还不支持
        # 解决办法就是删除时不进行同步，然后再让 session 里的所有实体都过期
        db.session.query(SubCat).filter(SubCat.id.in_(cat_ids)).delete(synchronize=False)
        db.session.commit()
        return redirect(url_for('admin.subcat_list'))

@admin.route('/orders/list/')
@admin_login
def orders_list():
    ''' 订单列表页面 '''
    keywords = request.args.get('keywords', '', type=str)
    page = request.args.get('page', 1, type=int) # 获得page参数
    if keywords:
        page_data = Orders.query.filter_by(id=keywords).order_by(Orders.addtime.desc()).paginate(page=page, per_page=10)
    else:
        page_data = Orders.query.order_by(Orders.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/orders_list.html', page_data=page_data)

@admin.route('/orders/detail')
def orders_detail():
    '''订单详情'''
    order_id = request.args.get('order_id')
    orders = OrdersDetail.query.join(Orders).filter(OrdersDetail.order_id==order_id).all()
    return render_template('admin/orders_detail.html', data=orders)

@admin.route('/topgoods/')
@admin_login
def topgoods():
    '''销量排行榜（前十位）'''

    orders = OrdersDetail.query.join(Goods, OrdersDetail.goods_id == Goods.id).with_entities(Goods.name, func.sum(OrdersDetail.number).label('s')).group_by(OrdersDetail.goods_id).order_by(desc('s')).limit(10).all()

    return render_template("admin/topgoods.html", data=orders)


