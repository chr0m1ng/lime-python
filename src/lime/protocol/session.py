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

    # encryption_options property
    @property
    def encryption_options(self):
        return self.__encryption_options

    @encryption_options.setter
    def encryption_options(self, value):
        if isinstance(value, list) and all(isinstance(v, SessionEncryption) for v in value):
            self.__encryption_options = value
        else:
            raise ValueError(
                'encryption_options must be a list of SessionEncryption')

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

    # compression_options property
    @property
    def compression_options(self):
        return self.__compression_options

    @compression_options.setter
    def compression_options(self, value):
        if isinstance(value, list) and all(isinstance(v, SessionCompression) for v in value):
            self.__compression_options = value
        else:
            raise ValueError(
                'compression_options must be a list of SessionCompression')

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


class SessionListener:

    @staticmethod
    def on_session(command): return None
