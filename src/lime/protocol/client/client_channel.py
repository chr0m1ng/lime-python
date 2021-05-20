from asyncio import Future, get_running_loop, wait_for, loop
from typing import Callable, Dict
from ..message import Message
from ..notification import Notification
from ..command import Command
from ..session import Session
from .channel import Channel
from ..network import Transport
from ..security import Authentication
from ..constants import SessionCompression, SessionEncryption, SessionState


class ClientChannel(Channel):
    """Client channel representation"""

    def __init__(
        self,
        transport: Transport,
        auto_reply_pings: bool = True,
        auto_notify_receipt: bool = False
    ) -> None:
        super().__init__()
        self.transport = transport
        self.auto_reply_pings = auto_reply_pings
        self.auto_notify_receipt = auto_notify_receipt

    def establish_session(
        self,
        compression: SessionCompression,
        encryption: SessionEncryption,
        identity: str,
        authenticaion: Authentication,
        instance: str
    ):

        if(self.state != SessionState.NEW):
            raise ValueError(
                f'cannot establish a session in the {self.state} state'
            )

    def start_new_session(self) -> Future:
        if (self.state != SessionState.NEW):
            raise ValueError(
                f'Cannot start a session in the {self.state} state'
            )
        loop = get_running_loop()
        future = loop.create_future()

        self.__on_session_finished = future.set_result
        self.__on_session_failed = future.set_exception

        session = Session(SessionState.NEW)
        self.send_session(session)

        return future

    def start_new_session(self) -> Future:
        """Start new session.

        Raises:
            ValueError: Value error in case state is not 'new'

        Returns:
            Future: session future
        """
        if (self.state != SessionState.NEW):
            raise ValueError(
                f'Cannot start a session in the {self.state} state'
            )
        loop = get_running_loop()
        future = loop.create_future()

        self.__on_session_finished = future.set_result
        self.__on_session_failed = future.set_exception

        session = Session(SessionState.NEW)
        self.send_session(session)

        return future

    def negotiate_session(
        self,
        session_compression: str,
        session_encryption: str
    ) -> Future:
        """Negotiate session

        Args:
            session_compression (str): session compression type
            session_encryption (str): session encryption type

        Raises:
            ValueError: raise Value error in case state is not 'Negotiating'

        Returns:
            Future: negotiate session future
        """
        if (self.state != SessionState.NEGOTIATING):
            raise ValueError(
                f'Cannot start a session in the {self.state} state'
            )
        loop = get_running_loop()
        future = loop.create_future()

        self.__on_session_authenticating = future.set_result
        self.__on_session_failed = future.set_exception

        session = Session(SessionState.NEGOTIATING,
                          session_encryption,
                          session_compression
                          )

        session.id = self.session_id
        self.send_session(session)

        return future

    def __on_session_failed(self, session: Session):
        pass

    def __on_session_finished(self, session: Session):
        pass

    def __on_session_authenticating(self, session: Session):
        pass
