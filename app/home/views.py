# _*_ coding:utf-8 _*_
from urllib.parse import urlparse, urljoin

from flask import render_template, request, session, redirect, url_for

from app import db
from app.home import home
from app.models import Goods, Cart, Orders, OrdersDetail
from app.utils.decorater import user_login
from app.utils.urlforback import redirect_back


@home.route('/')
def index():
    '''首页'''
    #获得两个热门商品
    hot_goods = Goods.query.order_by(Goods.views_count.desc()).limit(2).all()  #过滤条件后查询新结果后全部取出
    # 获得12个新品
    new_goods = Goods.query.filter_by(is_new=1).order_by(Goods.addtime.desc()).limit(12).all()
    # 获得12个打折商品
    sale_goods = Goods.query.filter_by(is_sale=1).order_by(Goods.addtime.desc()).limit(12).all()
    return render_template('home/index.html', hot_goods=hot_goods, new_goods=new_goods, sale_goods=sale_goods)

@home.route('/goods_list/<int:supercat_id>')
def goods_list(supercat_id=None):
    '''
    商品页
    :param supercat_id: 为大商品分类ID
    :return:
    '''
    page = request.args.get('page', 1, type=int)  #获取page参数值  设置page参数
    page_data = Goods.query.filter_by(supercat_id=supercat_id).paginate(page=page, per_page=12)
    # 左侧边栏热门商品
    hot_goods = Goods.query.filter_by(supercat_id=supercat_id).order_by(Goods.views_count.desc()).limit(7).all()
    return render_template('home/goods_list.html', page_data=page_data, hot_goods=hot_goods, supercat_id=supercat_id)

@home.route('/goods_detail/<int:id>/')
def goods_detail(id=None):
    '''
    详情页
    :param id: 商品ID
    :return:
    '''
    user_id = session.get('user_id', 0)  # 获取用户名ID， 判断用户名是否登陆
    # print('------->', id)
    goods = Goods.query.get_or_404(id) # 根据商品id获取商品数据，如果不存在就返回404 ---> manage.py 中定义的404
    #如果找到， 浏览量+1
    goods.views_count += 1
    db.session.add(goods)  # 添加数据
    db.session.commit() # 提交数据
    #左侧当前小分类热门商品
    hot_goods = Goods.query.filter_by(subcat_id=goods.subcat_id).order_by(Goods.views_count.desc()).limit(5).all()
    # 底部相关小分类热门商品
    similar_goods = Goods.query.filter_by(subcat_id=goods.subcat_id).order_by(Goods.addtime.desc()).limit(5).all()
    return render_template('home/goods_detail.html', goods = goods, hot_goods=hot_goods, similar_goods=similar_goods, user_id=user_id)

@home.route('/search/')
def goods_search():
    '''搜索功能'''
    page = request.args.get('page', 1, type=int) # 获取page参数值 设置参数
    keywords = request.args.get('keywords','',type=str) #获取get请求携带参数 搜索关键字
    if keywords:
        # 使用like实现模糊查询
        page_data = Goods.query.filter(Goods.name.like('%'+keywords+'%')).order_by(Goods.addtime.desc()).paginate(page=page, per_page=12) #有就显示最新12条
    else:
        page_data = Goods.query.order_by(Goods.addtime.desc()).paginate(page=page, per_page=12)

    hot_goods = Goods.query.order_by(Goods.views_count.desc()).limit(7).all()
    return render_template('home/goods_search.html', page_data=page_data, keywords=keywords, hot_goods=hot_goods)

@home.route('/cart_add/')
@user_login
def cart_add():
    '''
    添加商品到购物车 这里需要判断是否登陆了
    :return:
    '''
    cart = Cart(
        goods_id = request.args.get('goods_id'),
        number = request.args.get('number'),
        user_id = session.get('user_id', 0) # 获取用户ID,判断用户是否登录
    )
    db.session.add(cart) # 添加数据
    db.session.commit() # 提交数据
    return redirect_back()
    # return redirect(url_for(next=request.url))

@home.route('/cart_clear/')
@user_login
def cart_clear():
    ''' 清空购物车
    '''
    user_id = session.get('user_id', 0)
    Cart.query.filter_by(user_id=user_id).update({'user_id':0})
    db.session.commit()
    return redirect(url_for('home.shopping_cart'))

@home.route('/shopping_cart/')
@user_login
def shopping_cart():
    user_id = session.get('user_id', 0)
    cart = Cart.query.filter_by(user_id=user_id).order_by(Cart.addtime.desc()).all()
    if cart:
        return render_template('home/shopping_cart.html', cart=cart)
    else:
        return render_template('home/empty_cart.html')



@home.route('/cart_order/', methods=['GET', 'POST'])
@user_login
def cart_order():
    if request.method == 'POST':
        user_id = session.get('user_id', 0)
        # 添加订单
        orders = Orders(
            user_id = user_id,
            recevie_name = request.form.get('recevie_name'),
            recevie_tel = request.form.get('recevie_tel'),
            recevie_address = request.form.get('recevie_address'),
            remark = request.form.get('remark')
        )
        db.session.add(orders)
        db.session.commit()
        # 添加订单详情
        cart = Cart.query.filter_by(user_id=user_id).all()
        object = []
        for item in cart:
            object.append(
                OrdersDetail(
                    order_id = orders.id,
                    goods_id = item.goods_id,
                    number = item.number,
                )
            )
        db.session.add_all(object)
        # 修改购物车状态
        Cart.query.filter_by(user_id=user_id).update({'user_id':0})
        db.session.commit()
    return redirect(url_for('home.index'))
