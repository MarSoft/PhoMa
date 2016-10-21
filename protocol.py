from itertools import islice
import subprocess as sp

class Protocol:
    def __init__(self, path):
        self.path = path

    def list_directory(self):
        raise NotImplementedError

    def list_directory_page(self, page, pagesize):
        start = page * pagesize
        return islice(
            self.list_directory(),
            start, start + pagesize,
        )

    def get_files(self, names):
        # default implementation
        for name in names:
            yield self.get_file(name)

    def get_file(self, name):
        raise NotImplementedError

class AdbProtocol(Protocol):
    def __init__(self, path, host):
        super().__init__(path)
        self.host = host

    def adb(self, args):
        if isinstance(args, str):
            args = args.split()
        try:
            return sp.check_output(['adb']+args)
        except sp.CalledProcessError:
            return None

    def connect(self):
        self.adb('connect %s' % self.host)

    def list_directory(self):
        cmd = 'shell busybox ls %s -tr1' % self.path
        l = self.adb(cmd)
        if l is None:
            self.connect()
            l = self.adb(cmd)
            if l is None:
                return ['ERROR']
        return l
