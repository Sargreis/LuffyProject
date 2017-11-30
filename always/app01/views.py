<<<<<<< HEAD
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






















=======
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from rest_framework.views import APIView
from app01 import models
from app01.utils.tools.tools import gen_token
from app01.utils.serializers import Serializers
from app01.utils.authentication import authentication
from rest_framework.response import Response


from django_redis import get_redis_connection

conn = get_redis_connection('default')
from rest_framework.response import Response
from django.utils import timezone
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
        for create_dict in create_list:
            course_id = create_dict.get('course_id')
            policy_id = create_dict.get('policy_id')
            policy_obj = models.PricePolicy.objects.get(id=policy_id, object_id=course_id)
            ser = Serializers.CustomPricePolicySerializers(instance=policy_obj, many=False)
            temp_dict[policy_id] = ser.data
        # ridies_dict[username] = temp_dict
        # return JsonResponse(ridies_dict)
        return HttpResponse("...")

    def options(self, request, *args, **kwargs):
        return HttpResponse('')


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






# ####################redis购物信息存储#######################


from django_redis import get_redis_connection

conn = get_redis_connection('default')


class CartView(APIView):
    '''
    根据用户选择的课程和价格策略，存到redis的购物车信息表
    '''
    authentication_classes = [authentication.BaseAuthen, ]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        # 拿到该用户购买的所有课程（字典）
        course_list = eval(conn.hget('luffy_car', user_id).decode('utf-8'))
        print(course_list, type(course_list))
        return Response('get...')

    def post(self, request, *args, **kwargs):
        '''
        获取前端发送的数据格式：
        {'course_id':'xxx','policy_id':'xxxx'}
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        from django.core.exceptions import ObjectDoesNotExist
        import json

        # 获取前端发送的数据
        user_id = request.user.id
        # print(user_id, type(user_id))
        data = request.data  # <QueryDict:{'course_id':'xxx','policy_id':'xxxx'}>
        course_id = data.get('course_id')
        policy_id = data.get('policy_id')

        # 验证前端发送的课程ID和价格策略ID是否合法
        course_obj = models.Course.objects.filter(id=int(course_id)).first()
        if not course_obj:
            raise ObjectDoesNotExist('课程不存在')

        policy_id_list = [obj.id for obj in course_obj.price_policy.all()]
        if int(policy_id) not in policy_id_list:
            raise ObjectDoesNotExist('用户所选的价格策略不存在')

        # 查找选择的课程的所有价格策略
        ret = []
        policy_list = course_obj.price_policy.all()
        for obj in policy_list:
            ret.append({'id': obj.id, 'name': obj.get_valid_period_display(), 'price': obj.price})

        # 从redis中读取数据
        course_dict = eval(conn.hget('luffy_car', user_id).decode('utf-8'))
        # 生成课程数据
        course_dict[course_id] = {
            'name': course_obj.name,
            'img': course_obj.course_img,
            'selected_policy_id': policy_id,
            'policy_list': ret
        }

        # 向redis的购物车信息表存一条用户的购物记录
        conn.hset('luffy_car', user_id, json.dumps(course_dict))

        return Response('post...')

    def put(self, request, *args, **kwargs):
        return Response('put...')

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        course_id = request.data.get('course_id')
        course_dict = eval(conn.hget('luffy_car', user_id).decode('utf-8'))
        if course_id in list(course_dict.keys()):
            course_dict.pop(course_id)
        print(course_dict)
        conn.hset('luffy_car', user_id, course_dict)
        return Response('delete...')

class TestUser(APIView):
    info={'code':1000,'msg':'无信息','data':''}

    authentication_classes = [authentication.BaseAuthen, ]

    def get(self, request, *args, **kwargs):
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
>>>>>>> 32c973b3ee4fb07c7123d22dbf81d53507dabf96
