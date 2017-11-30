from django.contrib import admin
from app01 import models

admin.site.register(models.CourseSubCategory)
admin.site.register(models.CourseChapter)
admin.site.register(models.PricePolicy)
admin.site.register(models.Course)
admin.site.register(models.CourseDetail)
admin.site.register(models.Teacher)
admin.site.register(models.Account)
admin.site.register(models.Coupon)
admin.site.register(models.CouponRecord)
admin.site.register(models.TransactionRecord)


