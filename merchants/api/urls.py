from django.conf.urls import patterns, include, url
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin

from .views import (
		MerchantListAPIView,
	)

urlpatterns = [
    # url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^list/$', MerchantListAPIView.as_view(), name='merchant'),
]