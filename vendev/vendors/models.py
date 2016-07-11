from django.db import models


class Audit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PCIVendor(Audit):
    vendor_id = models.CharField(max_length=4, unique=True,
                                 db_index=True, primary_key=True)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    def __str__(self):
        return '[{}] {}'.format(self.vendor_id, self.name)


class PCIDevice(Audit):
    vendor = models.ForeignKey('PCIVendor')
    chipset = models.ForeignKey('self', blank=True, null=True)
    device_id = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('vendor', 'chipset', 'device_id')

    def __str__(self):
        return '[{}] {}'.format(self.device_id, self.name)


class USBVendor(Audit):
    vendor_id = models.CharField(max_length=4, unique=True,
                                 db_index=True, primary_key=True)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    def __str__(self):
        return '[{}] {}'.format(self.vendor_id, self.name)


class USBDevice(Audit):
    vendor = models.ForeignKey('USBVendor')
    device_id = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('vendor', 'device_id')

    def __str__(self):
        return '[{}] {}'.format(self.device_id, self.name)
