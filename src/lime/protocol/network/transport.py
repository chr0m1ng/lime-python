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

    @staticmethod
    async def open(uri): pass

    @staticmethod
    async def close(): pass

    @staticmethod
    def send(envelope): pass

    @staticmethod
    def get_supported_compression(): pass

    @staticmethod
    def set_compression(compression): pass

    @staticmethod
    def get_supported_encryption(): pass

    @staticmethod
    def set_encryption(encryption): pass
