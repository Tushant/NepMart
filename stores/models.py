import os
from django.db import models

from multiselectfield import MultiSelectField

from merchants.models import Merchant

DAY = (( 'Sun', 'Sunday'),
	   ( 'Mon', 'Monday'),
	   ( 'Tue', 'Tuesday'),
	   ( 'Wed', 'Wednesday'),
	   ( 'Thu', 'Thursday'),
	   ( 'Fri', 'Friday'),
	   ( 'Sat', 'Saturday')
	)
class Store(models.Model):
	merchant = models.ForeignKey(Merchant)
	name_of_legal_entity = models.CharField(max_length=250)
	pan_number = models.CharField(max_length=20)
	registered_office_address = models.CharField(max_length=200)
	name_of_store = models.CharField(max_length=100)
	store_contact_number = models.PositiveIntegerField(null=True,blank=True)
	store_long = models.DecimalField(max_digits=12, decimal_places=8, null=True)
	store_lat = models.DecimalField(max_digits=12, decimal_places=8, null=True)
	store_start_time = models.TimeField()  # start of when a store is closed
	store_end_time = models.TimeField()  # start of when a store is closed
	store_off_day = MultiSelectField(choices=DAY, max_length=7, default='Sat')
	store_categories = models.ManyToManyField('StoreCategory',blank=True)

	class Meta:
		verbose_name = 'Store'

	
	def __str__(self):
		return self.name_of_store



class Product(models.Model):
	store = models.ForeignKey(Store)
	image = models.ForeignKey('ProductImage',blank=True,null=True)
	name_of_product = models.CharField(max_length=120)
	description	= models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	active = models.BooleanField(default=True)
	# categories = models.ManyToManyField('Category',blank=True)


	def __str__(self):
		return self.name_of_product


class ProductImage(models.Model):
	# product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='products/images/')
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	@property
	def imageName(self):
		return str(os.path.basename(self.image.name))
	


	def __str__(self):
		return str(self.image)



# class VariationManager(models.Manager):
# 	def all(self):
# 		return super(VariationManager, self).filter(active=True)

# 	def sizes(self):
# 		return self.all().filter(category='size')

# 	def colors(self):
# 		return self.all().filter(category='color')



# VAR_CATEGORIES = (
# 		('size','size'),
# 		('color','color'),
# 	)


class StoreCategory(models.Model):
	GROCERY = 0
	MEATS = 1
	SPORTS = 2
	FOODS = 3
	BAGS = 4

	STORE_CATEGORIES= (
        ('GROCERY', ('Grocery')),
        ('MEATS', ('Meats')),
        ('SPORTS', ('Sports')),
        ('FOODS', ('Foods')),
        ('BAGS', ('Bags')),
    )

	product = models.ForeignKey(Product,null=True, on_delete=models.CASCADE,related_name="store_category")
	store_category = models.CharField(choices=STORE_CATEGORIES, default='GROCERY', max_length=10)
	# objects = VariationManager()

	class Meta:
		verbose_name = 'Store Category'
		verbose_name_plural = 'Store Categories'

	def __str__(self):
		# return str(self.product.name_of_product)
		return '{0} of category {1}' .format(self.product.name_of_product, str(self.store_category))


