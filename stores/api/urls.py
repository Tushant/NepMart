from django.conf.urls import patterns, include, url
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin

from .views import (
		StoreListAPIView,
		SingleStoreAPIView,
		StoreCreateAPIView
	)

urlpatterns = [
    url(r'^list/$', StoreListAPIView.as_view(), name='store'),
    url(r'^(?P<pk>\d+)/$', SingleStoreAPIView.as_view(), name='single-store'),
    url(r'^create/$', StoreCreateAPIView.as_view(), name="store-create"),
]