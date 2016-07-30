from django.conf.urls import patterns, include, url
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin

from .views import (
		UserCreateAPIView,
		UserLoginAPIView,
		UserLogoutAPIView,
		UserProfileChangeAPIView
	)

urlpatterns = [
    # url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^change/(?P<username>[\w ]+)/$', UserProfileChangeAPIView.as_view(), name='changeProfile'),
    url(r'^auth/token/', obtain_jwt_token),
]