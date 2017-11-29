#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Always"
# Date: 2017/11/26
from django.utils import deprecation

class CorsMiddleWare(deprecation.MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        response['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
        response['Access-Control-Allow-Headers'] = "Content-Type"
        return response