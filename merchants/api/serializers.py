from django.contrib.auth import get_user_model
from django.db.models import Q 

from rest_framework import serializers
from rest_framework.serializers import (
    CharField,
    EmailField,
    UUIDField,
    BooleanField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )


User = get_user_model()

from merchants.models import Merchant 
from account.api.serializers import UserSerializer

class MerchantSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Merchant
		# fields = ["pk","user","phone","address","city",]
