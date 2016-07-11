from django.contrib import admin
from vendors.models import PCIVendor, PCIDevice, USBVendor, USBDevice


@admin.register(PCIVendor)
class PCIVendorAdmin(admin.ModelAdmin):
    list_display = [
        'vendor_id', 'name', 'is_updatable', 'created_at',
        'updated_at'
    ]
    search_fields = ['name']


@admin.register(PCIDevice)
class PCIDeviceAdmin(admin.ModelAdmin):
    list_display = [
        'vendor',
        'device_id',
        'name',
        'chipset',
        'is_updatable',
        'created_at',
        'updated_at'
    ]
    search_fields = ['vendor__name', 'name']


@admin.register(USBVendor)
class USBVendorAdmin(admin.ModelAdmin):
    pass


@admin.register(USBDevice)
class USBDeviceAdmin(admin.ModelAdmin):
    pass
