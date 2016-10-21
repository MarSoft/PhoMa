from itertools import islice

class Protocol:
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
