from .envelope import Envelope


class Message(Envelope):

    # content_type property
    @property
    def content_type(self):
        return self.__content_type

    @content_type.setter
    def content_type(self, value):
        if isinstance(value, str):
            self.__content_type = value
        else:
            raise ValueError('content_type must be a str')

    # content property
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value


class MessageListener:

    def on_message(self, command): pass
