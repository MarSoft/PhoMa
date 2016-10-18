class Protocol:
    def list_directory(self):
        raise NotImplementedError

    def get_files(self, names):
        # default implementation
        for name in names:
            yield self.get_file(name)

    def get_file(self, name):
        raise NotImplementedError
