from django.core.management.base import BaseCommand
from vendors.management.vendev_tools import VenDevCommand
import re
from vendors.models import PCIVendor, PCIDevice


vendor_pattern = re.compile('^[\w]{4}')
device_pattern = re.compile('^(\t){1}')
sub_pattern = re.compile('^(\t){2}')


class Command(BaseCommand, VenDevCommand):
    help = 'Lookup for PCI IDS updates'

    def handle(self, *args, **options):
        url = 'http://pciids.sourceforge.net/v2.2/pci.ids'
        saved_file = self._save_as(url, '/tmp/pci.ids')
        self._update_vendors(saved_file, vendor_pattern, PCIVendor)
        #self._update_devices(saved_file)

    def _update_devices(self, path):
        with open(path, 'r') as fp:
            for line in fp:
                if line.startswith('C'):
                    break

                if vendor_pattern.match(line):
                    vendor_id = line[:4]
                    vendor = PCIVendor.objects.get(pk=vendor_id)

                elif sub_pattern.match(line):
                    line_chunks = line.split()
                    sub_vendor_id, sub_device_id = line_chunks[:2]
                    sub_name = ' '.join(line_chunks[2:])

                    sub_vendor = PCIVendor.objects.get(
                        vendor_id=dev.vendor_id
                    )

                    obj, created = PCIDevice.objects.get_or_create(
                        vendor=sub_vendor,
                        chipset=dev,
                        device_id=sub_device_id,
                        defaults={'name': sub_name}
                    )

                elif device_pattern.match(line):
                    device_id = line[1:5]
                    device_name = line[5:].strip()

                    dev, created = PCIDevice.objects.get_or_create(
                        vendor=vendor,
                        chipset=None,
                        device_id=device_id,
                        defaults={'name': device_name}
                    )
