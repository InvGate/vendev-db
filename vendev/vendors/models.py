from django.db import models


class PCIVendor(models.Model):
    vendor_id = models.CharField(max_length=4, unique=True,
                                 db_index=True, primary_key=True)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    def __str__(self):
        return '[{}] {}'.format(self.vendor_id, self.name)


class PCIDevice(models.Model):
    vendor = models.ForeignKey('PCIVendor')
    chipset = models.ForeignKey('self', blank=True, null=True)
    device_id = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    is_updatable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('vendor', 'chipset', 'device_id')

    def __str__(self):
        return '[{}] {}'.format(self.device_id, self.name)
