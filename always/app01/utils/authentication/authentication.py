#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "YGZBxia"
# Date: 2017/11/28

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from app01 import models

class BaseAuthen(BaseAuthentication):
    def authenticate(self, request):
        """
        http://127.0.0.1:8000/api/v1/testuser/?token=facaf748c3af07a5fe538ffc1377a9d48ee9cfaded4f78ac96b960f3
        如果需要使用认证来获取request.user的话
        无论post，和get都需要在？后面加上token=asdadsadadsasdds
        """
        val = request.query_params.get('token')
        tk_info=models.Token.objects.filter(value=val).first()
        if not tk_info:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (tk_info.user, tk_info)
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass