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
from django.utils import timezone
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
        try :
            pricepolicy_lists=request.data.get('pricepolicy')#用户发来的价格策略id
            all_coupons_list=request.data.get('all_coupons')#用户当前发来的使用的优惠券的id
            class_coupons_list=request.data.get('class_coupons')[0]#用户发来的课程优惠券id 列表
            public_coupons_list=request.data.get('public_coupons')#公共优惠券
            use_beili = request.data.get('beili')
        except Exception as e:
            self.info['code'] = 404
            self.info['msg'] = '''
            
            {"pricepolicy": [1],  -----这里的要求是传入选中的价格策略
            "all_coupons": [1, 2],  ----这里是返回所有用到的优惠券
            "class_coupons": [      ----这里是返回所有用到的课程优惠券 key：价格策略的id；value代表使用的优惠券id
                    {"1": 1}
                            ], 
            "public_coupons": 2, ----这里代表公共优惠券的id
                "beili": false  ----这里代表用不用贝里
            }
            链接地址：
            http://127.0.0.1:8000/api/v1/testuser/?token=5e7f904dfd9032ce96abafcc9a9fe9c74f2bc39d4e88c454f4d74c34
            '''
            return Response(self.info)
        ###########服务器得到的数据
        class_lists_obj=[]
        for pricepolicy_list in pricepolicy_lists:
            pricepolicy_obj=models.PricePolicy.objects.filter(id=pricepolicy_list).first()#价格策略
            course_obj=pricepolicy_obj.content_object #课程id
            class_lists_obj.append(course_obj)#[<Course: python入门(付费)>, <Course: python入门(付费)>]
        user_coupons_class_lists=user_obj.couponrecord_set.filter(status=0,)#所有的优惠券对象
        user_coupons_class_id=[x[0] for x in list(user_coupons_class_lists.values_list('coupon__pk'))]#数据库可用的优惠券id

        #######到这里为止 个人优惠券算法到此开始
        for i in all_coupons_list:
            if i not in user_coupons_class_id:
                self.info['code'] = 100
                self.info['msg'] = '非法操作,使用了不属于你的优惠券'
                return Response(self.info)
        class_price=0

        course_old_price=[]
        try:
            for i in pricepolicy_lists:
                price=models.PricePolicy.objects.filter(id=i).first()
                day=models.PricePolicy.objects.filter(id=i).first().valid_period
                many=price.price

                class_coupons=models.Coupon.objects.filter(id=class_coupons_list.get(str(price.id))).first().money_equivalent_value
                c=many-class_coupons
                course_old_price.append({'original_price':many,'price':class_coupons,'valid_period':day})
                if many<class_coupons :
                    self.info['code'] = 100
                    self.info['msg'] = '优惠券优惠价格超出了物品价值无法使用'
                    return Response(self.info)
                class_price+=c
        except Exception as e:
            self.info['code'] = 100
            self.info['msg'] = '别瞎几把传，贱人'
            print(e)
            return Response(self.info)

        #######################个人优惠券算法到此结束
        print(class_price,"这是在结算的结尾了额")

        print(public_coupons_list)
        if public_coupons_list:
            price = models.PricePolicy.objects.filter(id=public_coupons_list).first()
            many = price.valid_period
            oter_public=class_price-many
            if oter_public<0:
                self.info['code'] = 100
                self.info['msg'] = '公共优惠券优惠价格超出了物品价值无法使用'
                return Response(self.info)
        ######################公共优惠券算法结束

        ############路飞币开始
        beelin=int(user_obj.balance)

        if use_beili:
            #当前用户的贝里剩余
            if oter_public-(beelin/10) <= 0:
                order_obj=models.Order.objects.create(payment_type=3,
                                            order_number=gen_token(user_obj.username),
                                            account=user_obj,
                                            actual_amount=0,
                                            status=0,
                                            pay_time=nowtime
                                            )
                for i in range(len(class_lists_obj)):
                    models.OrderDetail.objects.create(
                        order=order_obj,
                        content_object=class_lists_obj[i],
                        original_price=course_old_price[i]['original_price'],
                        price=course_old_price[i]['price'],
                        valid_period=course_old_price[i]['valid_period']
                    )
                models.TransactionRecord.objects.create(account=user_obj,
                                                        amount=oter_public,
                                                        balance=oter_public-(beelin/10),
                                                        transaction_type=2,
                                                        transaction_number=gen_token(user_obj.username)
                                                        )

                #调用订单直接进行创建订单并且返回成功购买
                self.info['code'] = 200
                self.info['msg'] = '购买成功啦'
                return Response(self.info)
            else:
                oter_public= oter_public - (beelin/10)

        print(oter_public,'跳过路飞金币')

        ############路飞币结束

        ########常规订单开始
        order_obj = models.Order.objects.create(payment_type=1,
                                                order_number=gen_token(user_obj.username),
                                                account=user_obj,
                                                actual_amount=oter_public,
                                                status=1,
                                                pay_time=nowtime
                                                )
        for i in range(len(class_lists_obj)):
            models.OrderDetail.objects.create(
                order=order_obj,
                content_object=class_lists_obj[i],
                original_price=course_old_price[i]['original_price'],
                price=course_old_price[i]['price'],
                valid_period=course_old_price[i]['valid_period']
            )
        models.TransactionRecord.objects.create(account=user_obj,
                                                amount=oter_public,
                                                balance=(beelin / 10),
                                                transaction_type=2,
                                                transaction_number=gen_token(user_obj.username)
                                               )
        print('到这里了么？说明下一步就是要返回给他别人一个价格了',oter_public)
        return HttpResponse('post请求')
