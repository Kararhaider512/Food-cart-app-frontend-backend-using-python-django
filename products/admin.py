from django.contrib import admin
from products.models import products

class productsAdmin(admin.ModelAdmin):
  list_display = ('product_img', 'product_name', 'product_desc', 'product_price')
  
admin.site.register(products,productsAdmin)

# Register your models here.
