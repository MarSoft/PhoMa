from itertools import islice
import subprocess as sp
import tempfile
from os import path as op

class Protocol:
    def __init__(self, path):
        self.path = path

    def list_directory(self):
        raise NotImplementedError

    def list_directory_page(self, page, pagesize):
        start = page * pagesize
        ldir = self.list_directory()
        if ldir is None:
            return None
        return islice(
            ldir,
            start, start + pagesize,
        )

    def get_files(self, names):
        # default implementation
        for name in names:
            yield self.get_file(name)

    def get_file(self, name):
        raise NotImplementedError

    async def delete_list(self, names):
        raise NotImplementedError

class AdbProtocol(Protocol):
    def __init__(self, path, host):
        super().__init__(path)
        self.host = host
        self.tdir = tempfile.TemporaryDirectory()

    def adb(self, args):
        if isinstance(args, str):
            args = args.split()
        try:
            ret = sp.check_output(['adb']+args)
            return ret.decode()
        except sp.CalledProcessError:
            return None

    def connect(self):
        self.adb('connect %s' % self.host)

    def list_directory(self):
        cmd = 'shell busybox ls %s -t1' % self.path
        l = self.adb(cmd)
        if l is None:
            self.connect()
            l = self.adb(cmd)
            if l is None:
                return None
        return l.strip().splitlines()

    def get_file(self, name):
        tpath = '{}/{}'.format(self.tdir.name, name)
        if not op.exists(tpath):
            r = self.adb(
                'pull {path}/{name} {tpath}'.format(
                    path=self.path,
                    name=name,
                    tpath=tpath,
                ),
            )
            if r is None:
                return False
        with open(tpath, 'rb') as t:
            return t.read()

    async def delete_list(self, names):
        r = self.adb(
            'shell rm %s' % ' '.join(
                '%s/%s' % (self.path, name)
                for name in names
            )
        )
        if r is None:
            return False
        return r
