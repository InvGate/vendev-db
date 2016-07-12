from django.conf.urls import url, include
from rest_framework import routers
from vendors.api import PCIVendorViewSet, PCIDeviceViewSet, \
                        USBVendorViewSet, USBDeviceViewSet


router = routers.DefaultRouter()

router.register(r'vendors/pci', PCIVendorViewSet)
router.register(r'devices/pci', PCIDeviceViewSet)
router.register(r'vendors/usb', USBVendorViewSet)
router.register(r'devices/usb', USBDeviceViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
