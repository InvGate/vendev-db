from django.core.management.base import BaseCommand
import requests
import re
from vendors.models import PCIVendor, PCIDevice


vendor_pattern = re.compile('^[\w]{4}')
device_pattern = re.compile('^(\t){1}')
sub_pattern = re.compile('^(\t){2}')


class Command(BaseCommand):
    help = 'Lookup for PCI IDS updates'

    def handle(self, *args, **options):
        url = 'http://pciids.sourceforge.net/v2.2/pci.ids'
        saved_file = self._save_as(url, '/tmp/pci.ids')
        #self._update_vendors(saved_file)
        self._update_devices(saved_file)

    def _save_as(self, url, path=None):
        if not path:
            raise Exception('Implementar nombre automático')

        r = requests.get(url, stream=True)
        size = 0

        with open(path, 'wb') as fp:
            for chunk in r.iter_content(512):
                size += 1
                fp.write(chunk)

        self.stdout.write(self.style.SUCCESS('{}KiB'.format(size*512/1024)))

        return path

    def _update_devices(self, path):
        with open('/tmp/pci.ids', 'r') as fp:
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

                    sub_vendor = PCIVendor.objects.get(vendor_id=dev.vendor_id)

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

    def _update_vendors(self, path):
        stats = {
            'lines': 0,
            'vendors': 0,
            'created_vendors': 0,
            'updated_vendors': 0,
            'ignored_vendors': 0,
            'untouched_vendors': 0
        }

        with open('/tmp/pci.ids', 'r') as fp:
            for line in fp:
                stats['lines'] += 1

                if vendor_pattern.match(line):
                    stats['vendors'] += 1

                    vendor_id = line[:4]
                    vendor_name = line[4:].strip()

                    obj, created = PCIVendor.objects.get_or_create(
                        vendor_id = vendor_id,
                        defaults={'name': vendor_name}
                    )

                    if created:
                        stats['created_vendors'] += 1

                    elif obj.name != vendor_name:
                        if obj.is_updatable:
                            obj.name = vendor_name
                            obj.save()
                            stats['updated_vendors'] += 1
                        else:
                            stats['ignored_vendors'] += 1

        stats['untouched_vendors'] = stats['vendors'] - stats['created_vendors'] - stats['updated_vendors'] - stats['ignored_vendors']

        self.stdout.write(self.style.SUCCESS(stats))

        return stats
