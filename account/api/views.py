from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404 
from django.contrib.auth import login, logout, authenticate

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView


from rest_framework import permissions

# from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

User = get_user_model()

from .serializers import (
    UserProfileChangeSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    )



class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        print('data',data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            # new_data = serializer.data
            print('request.data', request.data)
            print('serializer.data',serializer.data)
            print('***********************')
            print('data.get',data.get('remember')) # returns true
            user = User.objects.get(username=serializer.data['username'])
            user_obj = authenticate(username=serializer.data['username'],password=data['password']) 
            login(request, user_obj)
            if data.get('remember'):
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return Response({
                'detail': ('Logged in successfully'),
                # TODO: maybe more user info in the request would have sense
                'username': serializer.data['username']
            })
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
    def permission_denied(self, request):
        raise exceptions.PermissionDenied(_("You are already authenticated"))



class UserLogoutAPIView(APIView):
    """
    log out
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """ clear session """
        request.session.flush()
        return Response({'detail':('Logged out successfully')})

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class UserProfileChangeAPIView(RetrieveAPIView,DestroyModelMixin,UpdateModelMixin):
    serializer_class = UserProfileChangeSerializer
    parser_classes = (MultiPartParser, FormParser,)
    # lookup_field = 'username'
    permission_classes = (IsAuthenticated,UserIsOwnerOrReadOnly, )

    def get_object(self):
        username = self.kwargs['username']
        obj = get_object_or_404(User, username=username)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.update(request, *args, **kwargs)
    
    