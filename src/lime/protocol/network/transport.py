from ..envelope import EnvelopeListener
from ..session import SessionCompression, SessionEncryption


class Transport(EnvelopeListener):

    # compression property
    @property
    def compression(self):
        return self.__compression

    @compression.setter
    def compression(self, value):
        if isinstance(value, SessionCompression):
            self.__compression = value
        else:
            raise ValueError('compression must be a SessionCompression')

    # encryption property
    @property
    def encryption(self):
        return self.__encryption

    @encryption.setter
    def encryption(self, value):
        if isinstance(value, SessionEncryption):
            self.__encryption = value
        else:
            raise ValueError('encryption must be a SessionEncryption')

    async def open(self, uri): pass

    async def close(self): pass

    def send(self, envelope): pass

    def get_supported_compression(self): pass

    def set_compression(self, compression): pass

    def get_supported_encryption(self): pass

    def set_encryption(self, encryption): pass
