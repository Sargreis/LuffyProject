import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from rest_framework.views import APIView
from app01 import models
from app01.utils.tools.tools import gen_token
from rest_framework.request import Request
from app01.utils.serializers import Serializers
from app01.utils.authentication import authentication
from django_redis import get_redis_connection

conn = get_redis_connection('default')


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
            request.user = user_obj
            response = JsonResponse({'code': 1002, 'username': username, 'tk': tk})
        else:
            # 验证失败，返会code：1001
            response = JsonResponse({'code': 1001})
        return response


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


class PaymentView(APIView):
    authentication_classes = [authentication.BaseAuthen, ]

    def get(self, request, *args, **kwargs):
        """
        用户结算时，用get获取数据，该函数将在redis中的"pay"的信息提取出来，并获取优惠券等信息后返回；
        用来渲染结算页面；
        :return: JsonResponse 结算页面需要的数据；
        """
        pay_dict = conn.hget('pay', request.user.id)
        if pay_dict:
            temp_dict = {}
            pay_dict = json.loads(pay_dict.decode("utf-8"))
            # 获取该用户的所有未使用的优惠券
            coupon_list = models.CouponRecord.objects.filter(account=request.user, status=0)

            # 循环每一个课程信息，重新整理格式并加入到 temp_dict 中
            for policy_id, pay_info in pay_dict.items():
                # 6 {'valid_period': 210, 'course': {'name': 'java', 'id': 2, 'img': '/static/java'}, 'price': 200.0}
                course_id = pay_info['course'].get('id')
                current_course_coupon_list = coupon_list.filter(coupon__object_id=course_id)
                # 序列化课程优惠券格式，并整理信息
                ser = Serializers.CustomCouponRecordSerializers(instance=current_course_coupon_list, many=True)

                course_info = pay_info.pop('course')
                policy_info = pay_info
                policy_info['id'] = policy_id
                coupon_info = ser.data
                temp_dict[course_id] = {"course_info": course_info, "policy_info": policy_info,
                                        "coupon_info": coupon_info}
            # 获取通用优惠券，并放入到temp_dict中，准备返回给前端
            gen_coupon_list = coupon_list.filter(coupon__object_id__isnull=True)
            ser = Serializers.CustomCouponRecordSerializers(instance=gen_coupon_list, many=True)
            data = ser.data
            code = 4002
            msg = "结算信息获取成功。。。"
        else:
            data = {}
            msg = "课程或课程信息已经发生变动，请重新提交数据！"
            code = 3001

        return JsonResponse({"data": {"gen_coupon": data, "course": temp_dict}, "code": code, "msg": msg})

    def post(self, request, *args, **kwargs):
        """
        用户点击立即结算时，用post提交数据，该函数将在redis中创建本次提交信息的记录；
        格式为： "pay": {用户id: "{优惠策略id:{k1: v1, k2: v2}, 优惠策略id:{k1: v1, k2: v2}}"}
        :return: 返回字典，code标识是否成功，msg标示提示信息；
        """
        create_list = request.data.get("create_list")
        create_list = eval(create_list) if create_list else []

        # try:
        temp_dict = {}
        try:
            for create_dict in create_list:
                course_id = create_dict.get('course_id')
                policy_id = create_dict.get('policy_id')
                policy_obj = models.PricePolicy.objects.get(id=policy_id, object_id=course_id)
                ser = Serializers.CustomPricePolicySerializers(instance=policy_obj, many=False)
                temp_dict[policy_id] = ser.data
            # 保存支付数据到redis中
            conn.hset('pay', request.user.id, json.dumps(temp_dict))
            msg = "成功！！！"
            code = 3002
        except ObjectDoesNotExist as e:
            msg = "课程或课程信息已经发生变动，请重新提交数据！"
            code = 3001

        return JsonResponse({'msg': msg, 'code': code})


class TestUser(APIView):
    authentication_classes = [authentication.BaseAuthen, ]

    def get(self, request, *args, **kwargs):
        return HttpResponse('111')

    def post(self, request, *args, **kwargs):
        print()
