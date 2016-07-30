from django.contrib import admin

from .models import Store,Product,StoreCategory, ProductImage

class StoreAdmin(admin.ModelAdmin):
	list_display = ['name_of_legal_entity','registered_office_address','name_of_store']
	class Meta:
		model = Store
admin.site.register(Product)
admin.site.register(StoreCategory)
admin.site.register(ProductImage)
admin.site.register(Store,StoreAdmin)