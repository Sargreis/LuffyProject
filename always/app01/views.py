import json

from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from rest_framework.views import APIView
from app01 import models
from app01.utils.tools.tools import gen_token
from rest_framework.request import Request
from app01.utils.serializers import Serializers
from app01.utils.authentication import authentication

from rest_framework.response import Response
import json

from django_redis import get_redis_connection

conn = get_redis_connection('default')




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
                # 获取用户贝里数额
                balance = request.user.balance

                course_info = pay_info.pop('course')
                policy_info = pay_info
                policy_info['id'] = policy_id
                coupon_info = ser.data
                temp_dict[course_id] = {"course_info": course_info,
                                        "policy_info": policy_info,
                                        "coupon_info": coupon_info,}
            # 获取通用优惠券，并放入到temp_dict中，准备返回给前端
            gen_coupon_list = coupon_list.filter(coupon__object_id__isnull=True)
            ser = Serializers.CustomCouponRecordSerializers(instance=gen_coupon_list, many=True)
            data = ser.data
            code = 4002
            msg = "结算信息获取成功。。。"
        else:
            balance = 0
            data = {}
            msg = "课程或课程信息已经发生变动，请重新提交数据！"
            code = 3001

        return JsonResponse({"data": {"gen_coupon": data, "course": temp_dict}, "code": code, "msg": msg, "balance": balance})

    def post(self, request, *args, **kwargs):
        """
        用户点击立即结算时，用post提交数据，该函数将在redis中创建本次提交信息的记录；
        格式为： "pay": {用户id: "{优惠策略id:{k1: v1, k2: v2}, 优惠策略id:{k1: v1, k2: v2}}"}
        :return: 返回字典，code标识是否成功，msg标示提示信息；
        """
        create_list = request.data.get("create_list")
        create_list = eval(create_list) if create_list else []


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

from django_redis import get_redis_connection
conn = get_redis_connection("default")
class ShoppingCartView(authentication.BaseAuthen,APIView):
    def get(self,request,*args,**kwargs):
        """
        点击页面上的购物车小图标，触发此函数
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_cart_dict = conn.hget("luffy_car",request.user.id)
        print(user_cart_dict)
        if user_cart_dict:
            user_cart_dict = eval(user_cart_dict.decode("utf-8"))
        return Response(user_cart_dict)



    def put(self,request,*args,**kwargs):
        """
        前端绑定onchange事件，一旦选中的价格策略发生变化，则触发此函数
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        course_id = request.data.get("course_id")
        to_change_policy_id = request.data.get("to_change_policy_id")
        user_courses_dict = conn.hget("luffy_car", request.user.id)

        if user_courses_dict:
            user_courses_dict = eval(user_courses_dict.decode("utf-8"))
            course_detail_dict = user_courses_dict.get(course_id)
            selected_policy_id = course_detail_dict.get("selected_policy_id")
            course_detail_dict["selected_policy_id"] = to_change_policy_id
            price_policy_list = course_detail_dict["policy_list"]
            date = models.PricePolicy.objects.get(id=selected_policy_id).valid_period
            price = models.PricePolicy.objects.get(id=selected_policy_id).price
            to_change_policy ={"id":selected_policy_id,"name":date,"price":price}
            for item in price_policy_list:
                if item.get("id") == selected_policy_id:
                    price_policy_list.remove(item)
                else:
                    price_policy_list.append(to_change_policy)
        return Response(user_courses_dict)
    def delete(self,request,*args,**kwargs):
        """
        删除某个课程，点击删除按钮触发此函数
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        course_id = request.data.get("course_id")
        user_courses_dict = conn.hget("luffy_car",request.user.id)
        if user_courses_dict:
            user_courses_dict = eval(user_courses_dict.decode("utf-8"))
            user_courses_dict.pop(course_id)
        return Response(user_courses_dict)


    def post(self, request, *args, **kwargs):
        conn.hset("luffy_car",request.user.id,"{'name':'21天学会Python','img':'xxxxxx.ong','selected_policy_id':2,'policy_list':[{'id':1,'name':'120天','price':99.99}]}")
        return HttpResponse("post...")

##############################支付相关##########################
from app01.utils.pay.pay import AliPay
import time
def ali():
    app_id = "2016082500309412"
    #post请求
    notify_url = "http://127.0.0.1:8008/api/v1/page2/"
    #get请求
    return_url = "http://127.0.0.1:8008/api/v1/pay/"
    merchant_private_key_path = "app01/utils/keys/pri"
    alipay_public_key_path = "app01/utils/keys/pub"

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,#支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,#默认是False
    )
    return alipay
def pay(request):
    if request.method == "POST":

        money = float(request.POST.get("money"))
        goods = request.POST.get("goods")
        alipay = ali()
        #生成支付的URL
        query_params = alipay.direct_pay(
            subject=goods,#商品简单描述
            out_trade_no="x2"+str(time.time()),#商户订单号
            total_amount=money,#交易金额（单位：元 保留两位小数）
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        return redirect(pay_url)

def page2(request):
    alipay = ali()
    if request.method == "POST":
        #检测是否支付成功
        #去请求体中获取所有反悔的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode("utf-8")
        post_data = parse_qs(body_str)
        post_dict = {}
        for k,v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop('sign',None)
        status = alipay.verify(post_dict,sign)
        if status:
            print(post_dict['stade_status'])
            print(post_dict['out_trade_no'])
        return HttpResponse("POST返回")
    else:
        params = request.GET.dict()
        sign = params.pop('sign',None)
        status = alipay.verify(params,sign)
        print('GET验证',status)
        return HttpResponse("支付成功")