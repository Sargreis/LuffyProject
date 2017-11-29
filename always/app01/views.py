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
    authentication_classes = [authentication.BaseAuthen, ]

    def get(self, request, *args, **kwargs):
        print(request.user)
        return HttpResponse('111')

    def post(self, request, *args, **kwargs):
        print()


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






