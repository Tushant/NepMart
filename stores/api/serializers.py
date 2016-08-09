from django.contrib.auth import get_user_model
from django.db.models import Q 
from rest_framework.exceptions import NotFound

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
import json

User = get_user_model()

from stores.models import Store, Product, ProductImage, StoreCategory
from merchants.models import Merchant 
from merchants.api.serializers import MerchantSerializer
from account.api.serializers import UserSerializer
# from product.api.serializers import ProductSerializers

class ProductImageSerializer(ModelSerializer):
	class Meta:
		model = ProductImage
		fields	=	( 'id','imageName','image', )

class ProductSerializers(ModelSerializer):
	image = ProductImageSerializer()
	class Meta:
		model = Product
		fields=('id','image','name_of_product','description','price','active',)

class StoreCategorySerializer(ModelSerializer):
	product = ProductSerializers()
	class Meta:
		model = StoreCategory
		# fields=["id","store_category",]

class StoreSerializer(ModelSerializer):
	# url = HyperlinkedIdentityField(view_name='stores_detail_api')
	store_categories = StoreCategorySerializer(many=True) 
	merchant = UserSerializer(read_only=True)
	class Meta:
		model = Store
		fields=("id",
				# "url",
				"merchant",
				"store_categories",
				"name_of_legal_entity",
				"pan_number",
				"registered_office_address",
				"name_of_store",
				"store_contact_number",
				"store_long",
				"store_lat",
				"store_start_time",
				"store_end_time",
				"store_off_day",
				)


class StoreCreateSerializer(ModelSerializer):
	store_categories = StoreCategorySerializer()
	merchant = UserSerializer()
	class Meta:
		model = Store
		fields=("id",
				"merchant",
				"store_categories",
				"name_of_legal_entity",
				"pan_number",
				"registered_office_address",
				"name_of_store",
				"store_contact_number",
				"store_long",
				"store_lat",
				"store_start_time",
				"store_end_time",
				"store_off_day",
				)
	def create(self,validated_data):
		store_categories_data = validated_data.pop('store_categories')
		print('store_categories_data',store_categories_data) 

		'''
		store_categories_data 
		OrderedDict([('product', OrderedDict([('image', OrderedDict([('image', <InMemoryUploadedFile: bag.jpg (image/jpeg)>)])), 
		('name_of_product', 'Ladies Pink Bag'), ('description', 'description'), ('price', Decimal('1600')), ('active', True)])), 
		('store_category', 'BAGS')])
		'''
		merchant_data = validated_data.pop('merchant')
		# merchant,created = Merchant.objects.get_or_create(user=merchant_data['user'])
		for merchantKey, merchantVal in merchant_data.items():
			print('merchantKey',merchantKey)
			print('merchantVal',merchantVal)
			print('merchant_data with key',merchant_data)
			try:
				merchant,created = User.objects.get_or_create(username=merchantVal)
				print('merchant',merchant)
				print(type(merchant))
				validated_data['merchant']=merchant
				'''
				merchant_data 
				OrderedDict([('user', OrderedDict([('username', 'Tushant'), ('first_name', 'Tushant'), ('last_name', 'Khatiwada'), 
				('email', 'tushant@gmail.com')])), ('phone', 999999999), ('address', 'Ganesh chowk'), 
				('city', 'Biratnagar')])
				'''
				print('______________________________________')
				print('validated_data is',validated_data)

				'''
				validated_data is 
				{'store_long': Decimal('26.4525'), 'registered_office_address': 'Ithari', 'store_end_time': datetime.time(18, 0), 
				'pan_number': '9843698469', 'store_start_time': datetime.time(10, 0), 'name_of_store': 'Priyanka Bag Shop', 
				'store_contact_number': 9843698469, 'store_off_day': 'Sat', 'name_of_legal_entity': 'Priyanka Bag Center', 
				'store_lat': Decimal('29.8900')}
				'''

				store = Store.objects.create(**validated_data)
				print('__________________________________')
				print('store.objects.create',store)
				image = store_categories_data["product"]["image"]
				print('image pop results',image)
				'''
				image pop results OrderedDict([('image', <InMemoryUploadedFile: grocery.jpg (image/jpeg)>)])
				'''
				image_instance = ProductImage(**image)
				# image_instance grocery.jpg
				print('image_instance',image_instance)
				image_instance.save()
				product = store_categories_data["product"]
				print('product creation returns',product['name_of_product'])
				#product creation returns OrderedDict([('name_of_product', 'Pepsodent'), ('description', 'Description on Pepsodent'), ('price', Decimal('220')), ('active', True)])
				product_instance = Product(
											store=store,
											image=image_instance,
											name_of_product=product['name_of_product'],
											description=product['description'],
											price=product['price'],
											active=product['active']
										)
				print('product_instance store',product_instance.store)
				print('product_instance name_of_product',product_instance.name_of_product)
				product_instance.save()
				print('product_instance',product_instance)
				store_category = store_categories_data['store_category']
				print('store_category',store_category)
				store_category = StoreCategory(product=product_instance, store_category=store_category)
				print('store category instance',store_category)
				print('store category product',store_category.product)
				print('store category store_category',store_category.store_category)
				store_category.product.store = store
				print('store categories.product.store',store_category.product.store)
				store_category.save()
				print('saved')
				return merchant
				print('returned')
			except User.DoesNotExist:
				raise NotFound('not found')