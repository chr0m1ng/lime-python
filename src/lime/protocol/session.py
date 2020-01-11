from envelope import Envelope
from reason import Reason


class SessionState:

    NEW = 'new'
    NEGOTIATING = 'negotiating'
    AUTHENTICATING = 'authenticating'
    ESTABLISHED = 'established'
    FINISHING = 'finishing'
    FINISHED = 'finished'
    FAILED = 'failed'


class SessionEncryption:

    NONE = 'none'
    TLS = 'tls'


class SessionCompression:

    NONE = 'none'
    GZIP = 'gzip'


class Session(Envelope):

    # state property
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if isinstance(value, SessionState):
            self.__state = value
        else:
            raise ValueError('state must be a SessionState')

    # encryptionOptions property
    @property
    def encryptionOptions(self):
        return self.__encryptionOptions

    @encryptionOptions.setter
    def encryptionOptions(self, value):
        if isinstance(value, list) and all(value, lambda v: isinstance(v, SessionEncryption)):
            self.__encryptionOptions = value
        else:
            raise ValueError(
                'encryptionOptions must be a list of SessionEncryption')

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

    # compressionOptions property
    @property
    def compressionOptions(self):
        return self.__compressionOptions

    @compressionOptions.setter
    def compressionOptions(self, value):
        if isinstance(value, list) and all(value, lambda v: isinstance(v, SessionCompression)):
            self.__compressionOptions = value
        else:
            raise ValueError(
                'compressionOptions must be a list of SessionCompression')

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

    # scheme property
    @property
    def scheme(self):
        return self.__scheme

    @scheme.setter
    def scheme(self, value):
        if isinstance(value, str):
            self.__scheme = value
        else:
            raise ValueError('scheme must be a str')

    # authentication property
    @property
    def authentication(self):
        return self.__authentication

    @authentication.setter
    def authentication(self, value):
        self.__authentication = value

    # reason property
    @property
    def reason(self):
        return self.__reason

    @reason.setter
    def reason(self, value):
        if isinstance(value, Reason):
            self.__reason = value
        else:
            raise ValueError('reason must be a Reason')
