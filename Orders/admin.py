from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Shipment)
admin.site.register(Download)
# Register your models here.
