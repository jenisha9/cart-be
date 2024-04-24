from django.contrib import admin

# Register your models here.
from .models import CartLine, CustomUser, Cart
admin.site.register(CustomUser)
admin.site.register(Cart)
admin.site.register(CartLine)
