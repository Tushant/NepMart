from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import Http404

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from stores.models import Store, StoreCategory, Product
from .serializers import StoreSerializer, StoreCreateSerializer

class StoreListAPIView(ListAPIView):
	model = Store
	queryset = Store.objects.all()
	serializer_class = StoreSerializer


class SingleStoreAPIView(RetrieveAPIView):
	queryset = Store.objects.all()
	serializer_class = StoreSerializer
	# lookup_field = 'id'

class StoreCreateAPIView(CreateAPIView):
	queryset = Store.objects.all()
	serializer_class = StoreCreateSerializer
	parser_classes = (FormParser,MultiPartParser,)

	# def put(self, request, filename, format=None):
	# 	print('first put works')
	# 	file_obj = request.data['file']
	# 	print ('file_obj',file_obj)
	# 	return Response(status=204)

	# def perform_create(self, serializer):
	# 	print('then perform works')
	# 	serializer.save() 