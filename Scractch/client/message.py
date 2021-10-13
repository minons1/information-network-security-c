class Message:
    def __init__(self, text, filename=None, filesize=None, key=None, iv=None, doc=None):
        self.message = text
        self.filename = filename
        self.filesize = filesize
        self.file = doc
        self.key = key
        self.iv = iv