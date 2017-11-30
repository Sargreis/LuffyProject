#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Always"
# Date: 2017/11/25


def gen_token(username):
    """
    使用用户的用户名以及时间戳进行sha224加密，作为登录的标识
        下次访问可以直接携带这个参数过来就可以了
    """
    import time
    import hashlib
    sha1 = hashlib.sha224()
    sha1.update(username.encode('utf-8'))
    sha1.update(str(time.time()).encode('utf-8'))
    return sha1.hexdigest()