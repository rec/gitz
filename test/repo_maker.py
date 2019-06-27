import tempfile


class GitRepo:
    def __init__(self):
        self.root = tempfile.TemporaryDirectory()
