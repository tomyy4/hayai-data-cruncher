from django.contrib import admin

from analytics.models import OrderLine, Product, Store

admin.site.register(Product)
admin.site.register(OrderLine)
admin.site.register(Store)