
from django.contrib import admin

from .models import Category, Rate, Product

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Rate)
