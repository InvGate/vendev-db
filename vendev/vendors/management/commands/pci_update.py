from django.core.management.base import BaseCommand, CommandError
import requests
import re
from vendors.models import PCIVendor, PCIDevice





class Command(BaseCommand):
    help = 'Lookup for PCI IDS updates'

    def handle(self, *args, **options):
        url = 'http://pciids.sourceforge.net/v2.2/pci.ids'
        saved_file = self._save_as(url, '/tmp/pci.ids')
        stats = self._update_vendors(saved_file)

        self.stdout.write(
            self.style.SUCCESS(
                'Lines: {lines}; Vendors: {vendors}; C: {created_vendors}; U: {updated_vendors}; I: {ignored_vendors}; UT: {untouched_vendors};'.format(**stats)
            )
        )

    def _save_as(self, url, path=None):
        if not path:
            raise Exception('Implementar nombre automático')

        r = requests.get(url, stream=True)

        with open(path, 'wb') as fp:
            for chunk in r.iter_content(512):
                fp.write(chunk)

        return path

    def _update_vendors(self, path):
        vendor_pattern = re.compile('^[\w]{4}')

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

        return stats
