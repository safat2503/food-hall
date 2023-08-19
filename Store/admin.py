from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Ebook)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('store', 'name','price')
admin.site.register(Product, ProductAdmin)

class MerchantDiscountAdmin(admin.ModelAdmin):
    list_display = ('store', 'discount_percentage','merchant')
admin.site.register(MerchantDiscount, MerchantDiscountAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user','product','quantity','tableNumber','totalPrice','orderStatus','paymentStatus','order_time','order_date')
admin.site.register(Orders, OrdersAdmin)