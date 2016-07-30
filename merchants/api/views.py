from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from merchants.models import Merchant
# from .permissions import IsOwnerAndAuth
from .serializers import MerchantSerializer

User = get_user_model()

class MerchantListAPIView(ListAPIView):
	model = Merchant
	queryset = Merchant.objects.all()
	serializer_class = MerchantSerializer