<<<<<<< HEAD:always/app01/admin.py
from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.PricePolicy)
admin.site.register(models.Course)
admin.site.register(models.CourseDetail)
admin.site.register(models.Teacher)
admin.site.register(models.Account)
admin.site.register(models.CourseSubCategory)
admin.site.register(models.CourseChapter)
=======
from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.PricePolicy)
admin.site.register(models.Course)
admin.site.register(models.CourseDetail)
admin.site.register(models.Teacher)
admin.site.register(models.Account)
admin.site.register(models.Coupon)
admin.site.register(models.CouponRecord)
admin.site.register(models.TransactionRecord)


>>>>>>> 32c973b3ee4fb07c7123d22dbf81d53507dabf96:always/app01/admin.py
