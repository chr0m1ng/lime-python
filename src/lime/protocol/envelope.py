class Envelope:

    # id property
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if isinstance(value, str):
            self.__id = value
        else:
            raise ValueError('id must be a str')

    # from_n property
    @property
    def from_n(self):
        return self.__from_n

    @from_n.setter
    def from_n(self, value):
        if isinstance(value, str):
            self.__from_n = value
        else:
            raise ValueError('from_n must be a str')

    # to_n property
    @property
    def to_n(self):
        return self.__to_n

    @to_n.setter
    def to_n(self, value):
        if isinstance(value, str):
            self.__to_n = value
        else:
            raise ValueError('to_n must be a str')

    # pp property
    @property
    def pp(self):
        return self.__pp

    @pp.setter
    def pp(self, value):
        if isinstance(value, str):
            self.__pp = value
        else:
            raise ValueError('pp must be a str')

    # metadata property
    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, value):
        if isinstance(value, dict):
            self.__metadata = value
        else:
            raise ValueError('metadata must be a dict')

    @staticmethod
    def is_message(envelope):
        return isinstance(envelope, Envelope) and hasattr(envelope, 'content')

    @staticmethod
    def is_notification(envelope):
        return isinstance(envelope, Envelope) and hasattr(envelope, 'event')

    @staticmethod
    def is_command(envelope):
        return isinstance(envelope, Envelope) and hasattr(envelope, 'method')

    @staticmethod
    def is_session(envelope):
        return isinstance(envelope, Envelope) and hasattr(envelope, 'state')


class EnvelopeListener:

    @staticmethod
    def on_envelope(envelope): pass
