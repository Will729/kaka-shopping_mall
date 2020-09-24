# _*_ coding:utf-8 _*_
# 跳转回上一个页面
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for


# default 可以指定一个url
def redirect_back(default='', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
    # return "<script>alert('密码修改成功');location.href='%s';</script>" % (default,)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc