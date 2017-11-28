from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from . import models
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
# Create your views here.
import json
def test(request):

    return JsonResponse({'test':'Successful'})


def gen_token(username):
    import hashlib
    import time
    ctime = str(time.time())
    md5 = hashlib.md5(username.encode('utf-8'))
    md5.update(ctime.encode('utf-8'))
    return md5.hexdigest()


class lo_gin(views.APIView):
    def options(self,request,*args,**kwargs):

        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST'  # 允许的复杂请求方式为 PUT 请求;如果多个，用逗号分隔, "PUT, DELETE"
        response['Access-Control-Allow-Headers'] = "Content-Type"  # 复杂请求还有一种情况就是定制请求头，这种情况下，我们在返回的相应中应该设置该响应头，代表允许发送请求头的key是什么，如果多个，逗号分隔 "k1, k2"
        return response
    def post(self,request,*args,**kwargs):
        # request.body是字符串
        # request.data是字典

        userinfo = json.loads(request.body.decode('utf-8'))

        username = models.UserInfo.objects.filter(user=userinfo.get('username'),pwd=userinfo.get('password')).first()
        if username:
            print(username.user)
            tk = gen_token(username.user)
            models.Token.objects.update_or_create(user=username, defaults={'token': tk})
            user_obj = models.Token.objects.filter(user=username).first()
            print(user_obj.token)
            print('ok')
            response = JsonResponse({'token':user_obj.token,'username':username.user,'code':200})


        else:
            response = JsonResponse({'msg':'用户名或密码错误','code':False})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST'  # 允许的复杂请求方式为 PUT 请求;如果多个，用逗号分隔, "PUT, DELETE"
        response['Access-Control-Allow-Headers'] = "Content-Type"
        return response


class CourseSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    class Meta:
        model = models.Course
        fields = ['name','level_name','brief','id']


class Courses(views.APIView):
    def options(self,request,*args,**kwargs):

        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET'  # 允许的复杂请求方式为 PUT 请求;如果多个，用逗号分隔, "PUT, DELETE"
        response['Access-Control-Allow-Headers'] = "Content-Type"  # 复杂请求还有一种情况就是定制请求头，这种情况下，我们在返回的相应中应该设置该响应头，代表允许发送请求头的key是什么，如果多个，逗号分隔 "k1, k2"
        return response
    def get(self,request,*args,**kwargs):
        course_obj = models.Course.objects.all()
        course_list = CourseSerializer(instance=course_obj, many=True)
        # print(type(course_list.data))
        response = JsonResponse({'data':course_list.data})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET'
        response['Access-Control-Allow-Headers'] = "Content-Type"
        return response


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseDetail
        fields = ['why_study','what_to_study_brief','career_improvement','prerequisite']


class CourseDetail(views.APIView):
    def get(self,request,*args,**kwargs):

        course_detail = models.CourseDetail.objects.filter(course_id=kwargs.get('course_id')).first()
        # print(course_list)
        course_info = CourseDetailSerializer(instance=course_detail,many=False)
        print(course_info.data)
        response = JsonResponse(course_info.data)
        # print(kwargs.get('course_id'))
        return response

# def lo_gin(request):
#     import json
#
#     if request.method == 'POST':
#         # request.body是字符串
#         # request.data是字典
#         userinfo = json.loads(request.body.decode('utf-8'))
#
#         username = models.UserInfo.objects.filter(user=userinfo.get('username'),pwd=userinfo.get('password')).first()
#         if username:
#             print(username.user)
#             tk = gen_token(username.user)
#             models.Token.objects.update_or_create(user=username, defaults={'token': tk})
#             user_obj = models.Token.objects.filter(user=username).first()
#             print(user_obj.token)
#             print('ok')
#             return JsonResponse({'token':user_obj.token,'username':username.user})
#         else:
#             return JsonResponse({'100':'用户名或密码错误'})
#
#     #     print(userinfo.get('username'))
#     #     if userinfo.get('username') == 'alex' and userinfo.get('password') == '123':
#     #         print('登录成功')
#     #         return JsonResponse({200:'登录成功'})
#     #     else:
#     #         print('用户名或密码错误')
#     #         return JsonResponse({100:'登录失败'})
#     return JsonResponse({'login':'login'})

