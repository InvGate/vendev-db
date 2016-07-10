from django.contrib import admin
from vendors.models import PCIVendor, PCIDevice, USBVendor, USBDevice

@admin.register(PCIVendor)
class PCIVendorAdmin(admin.ModelAdmin):
    pass

@admin.register(PCIDevice)
class PCIDeviceAdmin(admin.ModelAdmin):
    pass

@admin.register(USBVendor)
class USBVendorAdmin(admin.ModelAdmin):
    pass

@admin.register(USBDevice)
class USBDeviceAdmin(admin.ModelAdmin):
    pass
