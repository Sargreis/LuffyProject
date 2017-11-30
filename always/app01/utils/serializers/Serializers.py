<<<<<<< HEAD
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Always"
# Date: 2017/11/27
from app01 import models
from rest_framework import serializers


class CustomCourseSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    brief = serializers.CharField()
    course_img = serializers.CharField()
    level = serializers.CharField(source='get_level_display')


class TeacherField(serializers.CharField):
    def get_attribute(self, instance):
        return [obj.name for obj in instance.teachers.all()]

    def to_representation(self, value):
        return value

class PricePolicyField(serializers.CharField):
    def get_attribute(self, instance):
        return [{'id':obj.id,'price': obj.price, 'valid_period': obj.get_valid_period_display(), 'day': obj.valid_period} for obj in instance.course.price_policy.all()]

    def to_representation(self, value):
        return value

class CustomCourseDetailSerializers(serializers.ModelSerializer):
    teachers = TeacherField()
    courses = serializers.CharField(source='course.name')
    brief = serializers.CharField(source='course.brief')
    pricePolicy = PricePolicyField(source='course.price_policy.all')

    class Meta:
        model = models.CourseDetail
        fields = ['id','brief','hours', 'course_slogan', 'why_study', 'what_to_study_brief', 'career_improvement',
                  'prerequisite', 'teachers', 'courses', 'pricePolicy', 'video_brief_link']


class CourseChapterSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.CourseChapter
        fields = ['name','summary']


class CustomPricePolicySerializers(serializers.ModelSerializer):
    """
    定义一个关于价格策略方面的序列化类
    主要用来序列化数据后提供给缓存中，用来结算时使用
    """
    course = serializers.SerializerMethodField()
    class Meta:
        model = models.PricePolicy
        fields = ['price', 'valid_period', 'course']

    def get_course(self, obj):
        return {'id': obj.content_object.id, 'name': obj.content_object.name, 'img': obj.content_object.course_img}


class CustomCouponRecordSerializers(serializers.ModelSerializer):
    """
    定义一个优惠券发放相关的序列化类
    主要用来将相关数据封装后返回给前端结算页面
    """
    couponrecord_id = serializers.IntegerField(source="id")
    coupon_id = serializers.IntegerField(source="coupon.id")
    coupon_brief = serializers.CharField(source="coupon.brief")
    coupon_type = serializers.CharField(source="coupon.coupon_type")
    money_equivalent_value = serializers.IntegerField(source="coupon.money_equivalent_value")
    off_percent = serializers.IntegerField(source="coupon.off_percent")
    minimum_consume = serializers.IntegerField(source="coupon.minimum_consume")
    class Meta:
        model = models.CouponRecord
        fields = ["couponrecord_id", "coupon_id", "coupon_brief", "coupon_type",
                  'money_equivalent_value', 'off_percent', 'minimum_consume']
=======
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Always"
# Date: 2017/11/27
from app01 import models
from rest_framework import serializers


class CustomCourseSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    brief = serializers.CharField()
    course_img = serializers.CharField()
    level = serializers.CharField(source='get_level_display')


class TeacherField(serializers.CharField):
    def get_attribute(self, instance):
        return [obj.name for obj in instance.teachers.all()]

    def to_representation(self, value):
        return value

class PricePolicyField(serializers.CharField):
    def get_attribute(self, instance):
        return [{'id':obj.id,'price': obj.price, 'valid_period': obj.get_valid_period_display(), 'day': obj.valid_period} for obj in instance.course.price_policy.all()]

    def to_representation(self, value):
        return value

class CustomCourseDetailSerializers(serializers.ModelSerializer):
    teachers = TeacherField()
    courses = serializers.CharField(source='course.name')
    brief = serializers.CharField(source='course.brief')
    pricePolicy = PricePolicyField(source='course.price_policy.all')

    class Meta:
        model = models.CourseDetail
        fields = ['id','brief','hours', 'course_slogan', 'why_study', 'what_to_study_brief', 'career_improvement',
                  'prerequisite', 'teachers', 'courses', 'pricePolicy', 'video_brief_link']


class CourseChapterSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.CourseChapter
        fields = ['name','summary']


class CustomPricePolicySerializers(serializers.ModelSerializer):
    """
    定义一个关于价格策略方面的序列化类
    主要用来序列化数据后提供给缓存中，用来结算时使用
    """
    course = serializers.SerializerMethodField()
    class Meta:
        model = models.PricePolicy
        fields = ['price', 'valid_period', 'course']

    def get_course(self, obj):
        return {'id': obj.content_object.id, 'name': obj.content_object.name, 'img': obj.content_object.course_img}


class CustomCouponRecordSerializers(serializers.ModelSerializer):
    """
    定义一个优惠券发放相关的序列化类
    主要用来将相关数据封装后返回给前端结算页面
    """
    couponrecord_id = serializers.IntegerField(source="id")
    coupon_id = serializers.IntegerField(source="coupon.id")
    coupon_brief = serializers.CharField(source="coupon.brief")
    coupon_type = serializers.CharField(source="coupon.coupon_type")
    money_equivalent_value = serializers.IntegerField(source="coupon.money_equivalent_value")
    off_percent = serializers.IntegerField(source="coupon.off_percent")
    minimum_consume = serializers.IntegerField(source="coupon.minimum_consume")
    class Meta:
        model = models.CouponRecord
        fields = ["couponrecord_id", "coupon_id", "coupon_brief", "coupon_type",
                  'money_equivalent_value', 'off_percent', 'minimum_consume']
>>>>>>> b86017405bce821dbac8a6c4984a0189e3dc0bce
