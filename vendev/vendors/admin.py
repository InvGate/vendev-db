from django.contrib import admin
from vendors.models import PCIVendor, PCIDevice

@admin.register(PCIVendor)
class PCIVendorAdmin(admin.ModelAdmin):
    pass

@admin.register(PCIDevice)
class PCIDeviceAdmin(admin.ModelAdmin):
    pass
