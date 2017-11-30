from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import six
from rest_framework.views import APIView
from app01 import models
from app01.utils.tools.tools import gen_token
from rest_framework.request import Request
from app01.utils.serializers import Serializers


# pip install djangorestframework
class AuthView(APIView):
    """
    登录验证
    """

    def get(self, request, *args, **kwargs):
        """
        处理get请求的函数，暂时用不到
        """
        return HttpResponse("....")

    def post(self, request, *args, **kwargs):
        """
        处理post请求的函数，这里主要用来提交登录用户信息并验证返回token值
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = models.Account.objects.filter(username=username, password=password).first()

        if user_obj:
            # 如果验证成功，为该用户创建一个Token值，下次带过来，作为登录的标志
            tk = gen_token(username)
            # 如果有这条记录就跟新，如果没有这条记录就创建
            models.Token.objects.update_or_create(user=user_obj, defaults={'value': tk})
            # 验证成功，返会code：1002以及tk的值
            response = JsonResponse({'code': 1002, 'username': username, 'tk': tk})
        else:
            # 验证失败，返会code：1001
            response = JsonResponse({'code': 1001})
        return response

    def options(self, request, *args, **kwargs):
        """
        本次登录的功能是cors中的复杂请求，所以需要先通过option进行预检
        """
        # 本次预检返回的内容不重要
        return HttpResponse('')

# class CoursesView(APIView):
#     def get(self, request, *args, **kwargs):
#         course_id = kwargs.get('id')
#         print(course_id)
#         data = {'code': 2001, 'msg': '没有取到课程相关的数据。。。'}
#         return JsonResponse(data)






class CoursesView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            course_id = kwargs.get('id')
            if course_id:
                courseDetail_obj = models.CourseDetail.objects.get(course_id=course_id)
                courseChapter_obj = models.CourseChapter.objects.filter(course_id=course_id)
                ok = Serializers.CourseChapterSerializers(instance=courseChapter_obj,many=True)
                # print(courseChapter_obj)
                ser = Serializers.CustomCourseDetailSerializers(instance=courseDetail_obj, many=False)
                data = {'data':{'course':ser.data,'chapter':ok.data}}
            else:
                course_list_obj = models.Course.objects.exclude(course_type=2)
                ser = Serializers.CustomCourseSerializers(instance=course_list_obj, many=True)
                data = {'data': ser.data, 'code': 2002}
        except:
            data = {'code': 2001, 'msg': '没有取到课程相关的数据。。。'}
        return JsonResponse(data)





# ------redis---
from django_redis import get_redis_connection

conn = get_redis_connection("default")
import json

class Payment(APIView):
    def post(self,request,*args,**kwargs):
        print('pay')
        course_id = request.data.get('course_id')
        price_id = request.data.get('price_id')


        tk = request.query_params.get('token')
        course_info = models.Course.objects.filter(id=request.data.get('course_id')).first()
        tk_obj = models.Token.objects.filter(value=tk).first()
        policy_info = models.PricePolicy.objects.filter(id=price_id).first()

        course_dic = {'name': course_info.name,
                      'img': course_info.course_img,
                      'selected_policy_id': price_id,
                      'policy_list': [{'id': price_id, 'name': policy_info.valid_period, 'price': policy_info.price}]
                      }
        dic = {course_id:course_dic}
        # print(dic)
        # print(tk_obj.user.id)
        # print(dic,"new")
        old_info = eval(conn.hget('luffy_car', tk_obj.user.id).decode('utf-8'))

        old_info.update(dic)
        print(old_info, "++++", type(old_info))
        # print(dic,"-----")
        conn.hset('luffy_car', tk_obj.user.id, json.dumps(old_info).encode('utf-8'))

        v = conn.hget('luffy_car', tk_obj.user.id)
        print('------>',v)


        return JsonResponse(old_info)

    def get(self,request,*args,**kwargs):
        return JsonResponse({'ok':'ok'})






















