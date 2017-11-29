from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import six
from rest_framework.views import APIView
from app01 import models
from app01.utils.tools.tools import gen_token
from rest_framework.request import Request
from app01.utils.serializers import Serializers
from app01.utils.authentication import authentication
from rest_framework.response import Response
import time
import json
import datetime
# pip install djangorestframework
class AuthView(APIView):
    """
    登录验证
    在全局加了认证机制
    每次返回都需要带tk
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
            request.user=user_obj
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


class CoursesView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            course_id = kwargs.get('id')
            if course_id:
                courseDetail_obj = models.CourseDetail.objects.get(course_id=course_id)
                ser = Serializers.CustomCourseDetailSerializers(instance=courseDetail_obj, many=False)
            else:
                course_list_obj = models.Course.objects.exclude(course_type=2)
                ser = Serializers.CustomCourseSerializers(instance=course_list_obj, many=True)
            data = {'data': ser.data, 'code': 2002}
        except:
            data = {'code': 2001, 'msg': '没有取到课程相关的数据。。。'}
        return JsonResponse(data)

from django.core.exceptions import ObjectDoesNotExist
class CreateView(APIView):
    def post(self, request, *args, **kwargs):

        # models.Course.objects.filter(id=course_id).first()
        #     p = models.PricePolicy.objects.get(id=policy_id, object_id=6)
        # print(p)

        # try:
        #     policy_obj = models.PricePolicy.objects.get(id=policy_id, object_id=course_id)

        # except ObjectDoesNotExist as e:
        #     msg = "课程或课程信息变动，请重新提交数据！"
        username = 'admin'
        ridies_dict = {}
        create_list = [{'course_id': '1', 'policy_id': '2'}]
        temp_dict = {}
        for create_dict in create_list:
            course_id = create_dict.get('course_id')
            policy_id = create_dict.get('policy_id')
            policy_obj = models.PricePolicy.objects.get(id=policy_id, object_id=course_id)
            ser = Serializers.CustomPricePolicySerializers(instance=policy_obj, many=False)
            temp_dict[policy_id] = ser.data
        ridies_dict[username] = temp_dict
        return JsonResponse(ridies_dict)
        # return HttpResponse("...")

    def options(self, request, *args, **kwargs):
        return HttpResponse('')
class TestUser(APIView):
    info={'code':1000,'msg':'无信息','data':''}

    authentication_classes = [authentication.BaseAuthen, ]
    def get(self,request,*args,**kwargs):
        print(request.user)
        return HttpResponse('111')
    def post(self,request,*args,**kwargs):
        # print(request._request.COOKIES)
        if not request.user:
            self.info['code']=404
            self.info['msg']='用户登陆'
            return Response(self.info)
        nowtime=datetime.datetime.now()#当前时间
        user_obj=request.user#当前用户
        ###########用户发送过来的数据
        pricepolicy_lists=request.data.get('pricepolicy')#用户发来的价格策略id
        all_coupons_list=request.data.get('all_coupons')#用户当前发来的使用的优惠券的id
        class_coupons_list=request.data.get('class_coupons')#用户发来的课程优惠券id 列表
        public_coupons_list=request.data.get('public_coupons')#公共优惠券
        ###########服务器得到的数据
        for pricepolicy_list in pricepolicy_lists:
            pricepolicy_obj=models.PricePolicy.objects.filter(id=pricepolicy_list).first()#价格策略
            course_obj=pricepolicy_obj.content_object #课程id
        user_coupons_class_lists=user_obj.couponrecord_set.filter(status=0,)#所有的优惠券对象
        user_coupons_class_id=[x[0] for x in list(user_coupons_class_lists.values_list('coupon__pk'))]#数据库可用的优惠券id
        for i in all_coupons_list:
            if i not in user_coupons_class_id:
                self.info['code'] = 100
                self.info['msg'] = '非法操作'
                return Response(self.info)

        beelin=int(user_obj.balance)#当前用户的贝里剩余




        return HttpResponse('post')
