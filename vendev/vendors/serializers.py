from rest_framework import serializers

from vendors.models import PCIVendor, PCIDevice, USBVendor, USBDevice


class PCIVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCIVendor


class PCIDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCIDevice


class USBVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = USBVendor


class USBDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = USBDevice
