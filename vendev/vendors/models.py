from django.db import models


class Vendor(models.Model):
    vendor_id = models.CharField(max_length=4, unique=True,
                                 db_index=True, primary_key=True)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Device(models.Model):
    device_id = models.CharField(max_length=4, unique=True,
                                 db_index=True, primary_key=True)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    class Meta:
        abstract = True


class PCIVendor(Vendor):
    pass


class PCIDevice(Device):
    chipset = models.ForeignKey('PCIDevice', blank=True, null=True)


class USBVendor(Vendor):
    pass


class USBDevice(Device):
    pass
