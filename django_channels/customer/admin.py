from django.contrib import admin
from customer.models import Customer, Device, DeviceAuthored

admin.site.register(Customer)
admin.site.register(Device)
admin.site.register(DeviceAuthored)
