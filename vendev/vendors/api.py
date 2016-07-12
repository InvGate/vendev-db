from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from vendors.models import PCIVendor, PCIDevice, USBVendor, USBDevice
from vendors.serializers import PCIVendorSerializer, PCIDeviceSerializer, \
                                USBVendorSerializer, USBDeviceSerializer


class PCIVendorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = PCIVendor.objects.all()
    serializer_class = PCIVendorSerializer


class PCIDeviceViewSet(mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = PCIDevice.objects.all()
    serializer_class = PCIDeviceSerializer

    def retrieve(self, request, *args, **kwargs):
        vendor_id, device_id = kwargs['pk'].split(':')

        try:
            instance = PCIDevice.objects.get(
                vendor_id=vendor_id,
                device_id=device_id,
                chipset__isnull=True
            )

        except PCIDevice.DoesNotExist:
            instance = get_object_or_404(PCIDevice,
                                         vendor_id=vendor_id,
                                         device_id=device_id,
                                         chipset__isnull=False)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class USBVendorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = USBVendor.objects.all()
    serializer_class = USBVendorSerializer


class USBDeviceViewSet(mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = USBDevice.objects.all()
    serializer_class = USBDeviceSerializer

    def retrieve(self, request, *args, **kwargs):
        vendor_id, device_id = kwargs['pk'].split(':')

        instance = get_object_or_404(USBDevice,
                                     vendor_id=vendor_id,
                                     device_id=device_id)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
