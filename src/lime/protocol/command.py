from envelope import Envelope
from reason import Reason


class CommandMethod:

    GET = 'get'
    SET = 'set'
    DELETE = 'delete'
    OBSERVE = 'observe'
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'
    MERGE = 'merge'


class CommandStatus:

    SUCCESS = 'success'
    FAILURE = 'failure'


class Command(Envelope):

    # uri property
    @property
    def uri(self):
        return self.__uri

    @uri.setter
    def uri(self, value):
        if isinstance(value, str):
            self.__uri = value
        else:
            raise ValueError('uri must be a str')

    # resource_type property
    @property
    def resource_type(self):
        return self.__resource_type

    @resource_type.setter
    def resource_type(self, value):
        if isinstance(value, str):
            self.__resource_type = value
        else:
            raise ValueError('resource_type must be a str')

    # resource property
    @property
    def resource(self):
        return self.__resource

    @resource.setter
    def resource(self, value):
        self.__resource = value

    # method property
    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, value):
        if isinstance(value, CommandMethod):
            self.__method = value
        else:
            raise ValueError('method must be a CommandMethod')

    # status property
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if isinstance(value, CommandStatus):
            self.__status = value
        else:
            raise ValueError('status must be a CommandStatus')

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

    # timeout property
    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        if isinstance(value, bool):
            self.__timeout = value
        else:
            raise ValueError('timeout must be a bool')


class CommandListener:

    @staticmethod
    def on_command(command): return None
