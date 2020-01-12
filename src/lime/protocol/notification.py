from envelope import Envelope
from reason import Reason
from enum import Enum


class NotificationEvent(Enum):

    FAILED = 'failed'
    ACCEPTED = 'accepted'
    VALIDATED = 'validated'
    AUTHORIZED = 'authorized'
    DISPATCHED = 'dispatched'
    RECEIVED = 'received'
    CONSUMED = 'consumed'


class Notification(Envelope):

    # event property
    @property
    def event(self):
        return self.__event

    @event.setter
    def event(self, value):
        if isinstance(value, NotificationEvent):
            self.__event = value
        else:
            raise ValueError('event must be a NotificationEvent')

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


class NotificationListener:

    @staticmethod
    def on_notification(command):
        return None
