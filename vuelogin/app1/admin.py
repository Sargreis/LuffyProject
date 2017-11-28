from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Token)
admin.site.register(models.UserInfo)
admin.site.register(models.UserGroup)
admin.site.register(models.Teacher)
admin.site.register(models.Course)
admin.site.register(models.ContentType)
admin.site.register(models.CourseCategory)
admin.site.register(models.CourseDetail)
admin.site.register(models.PricePolicy)

