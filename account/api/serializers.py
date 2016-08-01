# from django.contrib.contenttypes.model import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q 

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

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","first_name","last_name","email",)

class UserProfileChangeSerializer(ModelSerializer):
    username = CharField(required=False, allow_blank=True)
    class Meta:
    	model = User
    	fields = [
    			'username',
    			'first_name',
    			'last_name',
    	]

    def update(self, instance, validated_data):
    	instance.username = validated_data.get('username',instance.username)
    	instance.first_name = validated_data.get('first_name',instance.first_name)
    	instance.last_name = validated_data.get('last_name',instance.last_name)
    	print('instance of username',instance.username)
    	instance.save() # saves updated data to database
    	return instance

class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
				'username',
				'email',
				'first_name',
				'last_name',
		]

class UserCreateSerializer(ModelSerializer):
	email = EmailField(label='Email Address')
	email2 = EmailField(label='Confirm Email Address')
	class Meta:
		model = User
		fields = ('pk', 'username', 'password', 'email', 'email2', 'first_name', 'last_name')
		extra_kwargs = {"password":
                            {"write_only": True},
                        "pk":
                        	{"read_only": True},
                        }

	def validate(self,data):
		print('validated data is', data)
		return data

	def validate_email(self,value):
		data = self.get_initial() # intial gives the initial data that been passed
		email1 = data.get("email2")
		email2 = value
		if email1 != email2:
			raise ValidationError('Emails must match')
		user_qs = User.objects.filter(email=email2)
		if user_qs.exists():
			raise ValidationError('This user has already registered')
		return value

	def validate_email2(self,value):
		data = self.get_initial()
		print('get initial', data)
		email1 = data.get('email')
		email2 = value
		if email1 != email2:
			raise ValidationError('emails must match')
		return value
	"""
	create and return a new 'user' instance, given the validated data
	"""
	def create(self, validated_data):
		print('validated_data',validated_data)
		username = validated_data['username']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		email = validated_data['email']
		email2 = validated_data['email2']
		password = validated_data['password']
		user_obj = User.objects.create(
				username=username,
				email=email,
				first_name=first_name,
				last_name=last_name
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    # email = EmailField(label='Email Address',required=False, allow_blank=True)
    remember = BooleanField(default=True, help_text = ("If checked you will stay logged in for 3 weeks"))
    class Meta:
        model = User
        fields = [
            'username',
            # 'email',
            'password',
            'remember',
            'token',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }

    def validate(self, data):
    	user_obj = None
    	# email = data.get('email',None)
    	username = data.get('username',None)
    	password = data['password']
    	if not username:
    		raise ValidationError('A username is required to login')
    	user = User.objects.filter(Q(username=username)).distinct()
    	if user.exists() and user.count() == 1:
    		user_obj = user.first()
    	else:
    		raise ValidationError('This username is not valid')
    	if user_obj:
    		if not user_obj.check_password(password):
    			raise ValidationError('Incorrect credentials')
    	data['token'] = 'SOME RANDOM TOKEN' 
    	return data 











# class ResetPasswordSerializer(serializers.Serializer):
    
#     email = serializers.EmailField(required = True)
    
#     def validate_email(self, attrs, source):
#         """ ensure email is in the database """
#         if PROFILE_EMAIL_CONFIRMATION:
#             condition = EmailAddress.objects.filter(email__iexact=attrs["email"], verified=True).count() == 0
#         else:
#             condition = User.objects.get(email__iexact=attrs["email"], is_active=True).count() == 0
        
#         if condition is True:
#             raise serializers.ValidationError(_("Email address not verified for any user account"))
        
#         return attrs
    
#     def restore_object(self, attrs, instance=None):
#         """ create password reset for user """
#         password_reset = PasswordReset.objects.create_for_user(attrs["email"])
        
#         return password_reset


# class ResetPasswordKeySerializer(serializers.Serializer):
    
# 	password1 = serializers.CharField(
# 	    help_text = _('New Password'),
# 	    max_length=PASSWORD_MAX_LENGTH
# 	)
# 	password2 = serializers.CharField(
# 	    help_text = _('New Password (confirmation)'),
# 	    max_length=PASSWORD_MAX_LENGTH
# 	)
    
#     def validate_password2(self, attrs, source):
#         """
#         password2 check
#         """
#         password_confirmation = attrs[source]
#         password = attrs['password1']
        
#         if password_confirmation != password:
#             raise serializers.ValidationError(_('Password confirmation mismatch'))
        
#         return attrs
    
#     def restore_object(self, attrs, instance):
#         """ change password """
#         user = instance.user
#         user.set_password(attrs["password1"])
#         user.save()
#         # mark password reset object as reset
#         instance.reset = True
#         instance.save()
        
#         return instance
