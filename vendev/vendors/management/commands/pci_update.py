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
        self._update_devices(saved_file)

    def _update_devices(self, saved_file):
        self._failed_dev = []
        s_lines = 0
        s_devices = 0
        update_output = False

        self.stdout.write(
            'Processing devices in {} ...'.format(saved_file.path)
        )

        with open(saved_file.path, 'r', encoding=saved_file.encoding) as fp:
            for line in fp:
                if line.startswith('C'):
                    # Comienzo de definiciones de clases de dispositivos
                    break

                s_lines += 1
                update_output = False

                if vendor_pattern.match(line):
                    vendor = PCIVendor.objects.get(
                        pk=self._parse_vendor_id(line)
                    )

                elif sub_pattern.match(line):
                    s_devices += 1
                    update_output = True

                    sub_vendor_id, sub_device_id, sub_device_name = \
                        self._parse_subsystem(line)

                    try:
                        sub_vendor = PCIVendor.objects.get(
                            vendor_id=sub_vendor_id
                        )
                    except PCIVendor.DoesNotExist:
                        continue

                    device = PCIDevice.objects.get(
                        vendor=vendor,
                        chipset=None,
                        device_id=device_id
                    )
                    data = {
                        'vendor': sub_vendor,
                        'chipset': device,
                        'device_id': sub_device_id,
                        'defaults': {'name': sub_device_name}
                    }
                    self._add_or_update(PCIDevice, data, sub_device_name,
                                        self._failed_dev)

                elif device_pattern.match(line):
                    s_devices += 1
                    update_output = True

                    device_id, device_name = self._parse_device(line)
                    data = {
                        'vendor': vendor,
                        'chipset': None,
                        'device_id': device_id,
                        'defaults': {'name': device_name}
                    }
                    self._add_or_update(PCIDevice, data, device_name,
                                        self._failed_dev)

                if update_output:
                    self.stdout.write('  {} Lines; {} Devices'.format(
                        s_lines, s_devices
                    ), ending='\r')

        msg = '  {} Lines; {} Devices; Done!'.format(s_lines, s_devices)
        if len(self._failed_dev) > 0:
            self.stdout.write(self.style.WARNING(msg))
            self.stdout.write(self.style.WARNING(
                '  Failed Devices: {}'.format(self._failed_dev)
            ))

        else:
            self.stdout.write(self.style.SUCCESS(msg))
