#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Always"
# Date: 2017/11/27
from app01 import models
from rest_framework import serializers


class CustomCourseSerializers(serializers.Serializer):
    '''
    自定义课程序列化

    '''
    id = serializers.IntegerField()
    name = serializers.CharField()
    brief = serializers.CharField()
    course_img = serializers.CharField()
    level = serializers.CharField(source='get_level_display')

class TeacherField(serializers.CharField):
    '''
    老师字段的信息的序列化
    '''
    def get_attribute(self, instance):
        return [obj.name for obj in instance.teachers.all()]

    def to_representation(self, value):
        return value

class PricePolicyField(serializers.CharField):
    '''
    价格策略的序列化提取
    '''
    def get_attribute(self, instance):
        return [{'price': obj.price, 'valid_period': obj.get_valid_period_display(), 'day': obj.valid_period} for obj in instance.course.price_policy.all()]

    def to_representation(self, value):
        return value

class CustomCourseDetailSerializers(serializers.ModelSerializer):
    '''
    课程详细信息的提取
    '''
    teachers = TeacherField()
    courses = serializers.CharField(source='course.name')
    pricePolicy = PricePolicyField(source='course.price_policy.all')
    class Meta:
        model = models.CourseDetail
        fields = ['hours', 'course_slogan', 'why_study', 'what_to_study_brief', 'career_improvement',
                  'prerequisite', 'teachers', 'courses', 'pricePolicy', 'video_brief_link']
