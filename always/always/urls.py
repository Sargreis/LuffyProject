"""always URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<version>\w+)/auth/$', views.AuthView.as_view(), name="auth"),  # 登录验证的路由
    url(r'^api/(?P<version>\w+)/courses/$', views.CoursesView.as_view(), name="course"),  # 显示课程信息的路由
    url(r'^api/(?P<version>\w+)/courses/(?P<id>\d+)/$', views.CoursesView.as_view(), name="detail"),  # 显示详细信息的路由
    url(r'^api/(?P<version>\w+)/payment/$', views.PaymentView.as_view(), name="payment"),  # 生成订单
    url(r'^api/(?P<version>\w+)/testuser/$', views.TestUser.as_view(), name="Test"),
    url(r'^api/(?P<version>\w+)/shopping_cart/', views.ShoppingCartView.as_view(), name="shopping_cart"),#显示购物车中要购买的所有课程信息
    url(r'^api/(?P<version>\w+)/shopping_cart/', views.ShoppingCartView.as_view(), name="shopping_cart"),#显示购物车中要购买的所有课程信息
    url(r'^api/(?P<version>\w+)/pay/$', views.pay, name="pay"),#跳转到支付页面
    url(r'^api/(?P<version>\w+)/page2/$', views.page2, name="pay"),#支付验证


    url(r'^api/(?P<version>\w+)/cart/$', views.CartView.as_view(), name="cart"),    # redis商品信息增删改查

]
