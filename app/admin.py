from django.contrib import admin
from .models import Product,Cart,CustomUser

admin.site.register(Product)
admin.site.register(CustomUser)
admin.site.register(Cart)