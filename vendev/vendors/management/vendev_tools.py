import requests


class VenDevCommand(object):

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
