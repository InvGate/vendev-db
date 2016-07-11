from django.core.management.base import BaseCommand
from vendors.management.vendev_tools import VenDevCommand
import re
from vendors.models import USBVendor, USBDevice


vendor_pattern = re.compile('^[\w]{4}')
device_pattern = re.compile('^(\t){1}')


class Command(BaseCommand, VenDevCommand):
    help = 'Lookup for USB IDS updates'

    def handle(self, *args, **options):
        url = 'http://www.linux-usb.org/usb.ids'
        saved_file = self._save_as(url, '/tmp/usb.ids')
        self._update_vendors(saved_file, vendor_pattern, USBVendor)
        #self._update_devices(saved_file)

    def _update_devices(self, path):
        with open(path, 'r') as fp:
            for line in fp:
                if line.startswith('C'):
                    break

                if vendor_pattern.match(line):
                    vendor_id = line[:4]
                    vendor = USBVendor.objects.get(pk=vendor_id)

                elif device_pattern.match(line):
                    device_id = line[1:5]
                    device_name = line[5:].strip()

                    dev, created = USBDevice.objects.get_or_create(
                        vendor=vendor,
                        device_id=device_id,
                        defaults={'name': device_name}
                    )
