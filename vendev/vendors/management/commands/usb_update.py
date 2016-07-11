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
        self._update_devices(saved_file)

    def _update_devices(self, saved_file):
        self._failed_dev = []
        s_lines = 0
        s_devices = 0

        self.stdout.write(
            'Processing devices in {} ...'.format(saved_file.path)
        )

        with open(saved_file.path, 'r', encoding=saved_file.encoding) as fp:
            for line in fp:
                if line.startswith('C'):
                    # Comienzo de definiciones de clases de dispositivos
                    break

                s_lines += 1

                if vendor_pattern.match(line):
                    vendor = USBVendor.objects.get(
                        pk=self._parse_vendor_id(line)
                    )

                elif device_pattern.match(line):
                    s_devices += 1

                    self.stdout.write('  {} Lines; {} Devices'.format(
                        s_lines, s_devices
                    ), ending='\r')

                    device_id, device_name = self._parse_device(line)
                    self._add_usb_device(USBDevice, vendor, device_id,
                                         device_name)

        msg = '  {} Lines; {} Devices; Done!'.format(s_lines, s_devices)
        if len(self._failed_dev) > 0:
            self.stdout.write(self.style.WARNING(msg))
            self.stdout.write(self.style.WARNING(
                '  Failed Devices: {}'.format(self._failed_dev)
            ))

        else:
            self.stdout.write(self.style.SUCCESS(msg))
