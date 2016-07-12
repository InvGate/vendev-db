import requests


class SavedFile(object):
    def __init__(self, path, encoding):
        self._path = path
        self._encoding = encoding

    @property
    def path(self):
        return self._path

    @property
    def encoding(self):
        return self._encoding


class VenDevCommand(object):

    def _save_as(self, url, path=None):
        if not path:
            raise Exception('Implementar nombre automático')

        self.stdout.write('Downloading {} ...'.format(url))
        r = requests.get(url, stream=True)
        size = 0

        with open(path, 'wb') as fp:
            for chunk in r.iter_content(512):
                size += 1
                self.stdout.write('  {}KiB'.format(size*0.5), ending='\r')
                fp.write(chunk)

        self.stdout.write(self.style.SUCCESS('  {}KiB Done!'.format(size*0.5)))

        return SavedFile(path, r.encoding)

    def _parse_vendor_id(self, line):
        return line[:4]

    def _parse_vendor(self, line):
        return line[:4], line[4:].strip()

    def _parse_device(self, line):
        return line[1:5], line[5:].strip()

    def _parse_subsystem(self, line):
        line_chunks = line.split()
        sub_vendor_id, sub_device_id = line_chunks[:2]
        sub_device_name = ' '.join(line_chunks[2:])
        return sub_vendor_id, sub_device_id, sub_device_name

    def _add_or_update(self, model, data, new_value, failed_list):
        try:
            obj, created = model.objects.get_or_create(**data)

            if not created and obj.name != new_value and obj.is_updatable:
                obj.name = new_value
                obj.save()

        except:
            failed_list.append(data)

    def _update_vendors(self, saved_file, vpattern, model):
        self._failed_ven = []
        s_lines = 0
        s_vendors = 0

        self.stdout.write(
            'Processing vendors in {} ...'.format(saved_file.path)
        )

        with open(saved_file.path, 'r', encoding=saved_file.encoding) as fp:
            for line in fp:
                if line.startswith('C'):
                    # Comienzo de definiciones de clases de dispositivos
                    break

                s_lines += 1

                if vpattern.match(line):
                    s_vendors += 1

                    self.stdout.write('  {} Lines; {} Vendors'.format(
                        s_lines, s_vendors
                    ), ending='\r')

                    vendor_id, vendor_name = self._parse_vendor(line)
                    data = {
                        'vendor_id': vendor_id,
                        'defaults': {'name': vendor_name}
                    }
                    self._add_or_update(model, data, vendor_name,
                                        self._failed_ven)

        msg = '  {} Lines; {} Vendors; Done!'.format(s_lines, s_vendors)
        if len(self._failed_ven) > 0:
            self.stdout.write(self.style.WARNING(msg))
            self.stdout.write(self.style.WARNING(
                '  Failed vendors: {}'.format(self._failed_ven)
            ))

        else:
            self.stdout.write(self.style.SUCCESS(msg))
