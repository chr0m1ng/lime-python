from asyncio import Future, ensure_future, get_running_loop  # no
from functools import partial
from typing import Awaitable
from ..command import Command
from ..constants import SessionState
from ..message import Message
from ..notification import Notification
from ..security import Authentication
from ..session import Session
from .channel import Channel


class ClientChannel(Channel):
    """Client channel representation."""

    async def establish_session_async(
        self,
        compression: str,
        encryption: str,
        identity: str,
        authentication: Authentication,
        instance: str
    ) -> Session:
        """Esablish a new session.

        Args:
            compression (str): compression type
            encryption (str): encryption type
            identity (str): identity str
            authentication (Authentication): Authentication specs
            instance (str): instance name

        Returns:
            Session: A established Session
        """
        self.ensure_state([SessionState.NEW], True)

        session: Session = await self.start_new_session_async()
        if session.encryption_options or session.compression_options:
            compression = compression if compression else session.compression_options[0]  # noqa: E501
            encryption = encryption if encryption else session.encryption_options[0]  # noqa: E501
            session: Session = await self.negotiate_session_async(compression, encryption)  # noqa: E501
        else:
            if session.compression != self.transport.compression:
                self.transport.set_compression(session.compression)
            if session.encryption != self.transport.encryption:
                self.transport.set_encryption(session.encryption)

        session: Session = await self.authenticate_session_async(identity, authentication, instance)  # noqa: E501
        self.__reset_session_listeners()
        return session

    def start_new_session_async(self) -> Awaitable[Session]:
        """Start new session.

        Returns:
            Future: A new Session
        """
        self.ensure_state([SessionState.NEW], True)

        loop = get_running_loop()
        future = loop.create_future()

        self.on_session_negotiating = future.set_result
        self.on_session_authenticating = future.set_result
        self.__on_session_failed = future.set_exception

        session = Session(SessionState.NEW)
        self.send_session(session)

        return future

    def negotiate_session_async(
        self,
        session_compression: str,
        session_encryption: str
    ) -> Awaitable[Session]:
        """Handle session in negotiating state.

        Args:
            session_compression (str): session compression type
            session_encryption (str): session encryption type

        Returns:
            Future: A negotiated Session
        """
        self.ensure_state([SessionState.NEGOTIATING], True)

        loop = get_running_loop()
        future = loop.create_future()

        self.on_session_authenticating = future.set_result
        self.__on_session_failed = future.set_exception

        session = Session(
            SessionState.NEGOTIATING,
            encryption=session_encryption,
            compression=session_compression
        )

        session.id = self.session_id
        self.send_session(session)

        return future

    def authenticate_session_async(
        self,
        identity: str,
        authentication: Authentication,
        instance: str
    ) -> Awaitable[Session]:
        """Authenticate session.

        Args:
            identity (str): Identity to authenticate
            authentication (Authentication): Authentication object
            instance (str): Instance to authenticate

        Returns:
            Future: An authenticated Session
        """
        self.ensure_state([SessionState.AUTHENTICATING], True)

        loop = get_running_loop()
        future = loop.create_future()

        self.on_session_established = future.set_result
        self.__on_session_failed = future.set_exception

        session = Session(
            SessionState.AUTHENTICATING,
            scheme=authentication.scheme if authentication.scheme else 'unknown',  # noqa: E501
            authentication=authentication
        )
        session.from_n = f'{identity}/{instance}'
        session.id = self.session_id
        self.send_session(session)

        return future

    def send_finishing_session_async(self) -> Awaitable[Session]:
        """Handle session in state finishing.

        Returns:
            Future: session future
        """
        self.ensure_state([SessionState.ESTABLISHED], True)

        loop = get_running_loop()
        future = loop.create_future()

        self.__on_session_finished = future.set_result
        self.__on_session_failed = future.set_exception

        session = Session(SessionState.FINISHING)
        session.id = self.session_id

        self.send_session(session)

        return future

    def on_session_finished(self, session: Session) -> None:
        """Handle callback on session finished.

        Args:
            session (Session): Received session
        """
        pass

    def on_session_failed(self, session: Session) -> None:
        """Handle callback on session failed.

        Args:
            session (Session): Received Session
        """
        pass

    def on_session(self, session: Session) -> None:  # noqa: WPS213
        """Handle session envelope received.

        Args:
            session (Session): Received Session
        """
        self.session_id = session.id
        self.state = session.state

        if session.state == SessionState.ESTABLISHED:
            self.local_node = str(session.to)
            self.remote_node = session.from_n

        # Switch case
        if session.state == SessionState.NEGOTIATING:
            self.on_session_negotiating(session)
            return

        if session.state == SessionState.AUTHENTICATING:
            self.on_session_authenticating(session)
            return

        if session.state == SessionState.ESTABLISHED:
            self.on_session_established(session)
            return

        if session.state == SessionState.FINISHED:

            task = ensure_future(self.transport.close_async())
            task.add_done_callback(
                partial(self.__on_session_finished_callbacks, session=session)
            )
            return

        if session.state == SessionState.FAILED:
            task = ensure_future(self.transport.close_async())
            task.add_done_callback(
                partial(self.__on_session_failed_callbacks, session=session)
            )
            return

    def on_message(self, message: Message) -> None:  # noqa: D102
        pass

    def on_command(self, command: Command) -> None:  # noqa: D102
        pass

    def on_notification(  # noqa: D102
        self,
        notification: Notification
    ) -> None:
        pass

    def on_session_authenticating(self, session: Session) -> None:
        """Handle session authenticating callback.

        Args:
            session (Session): received Session
        """
        pass

    def on_session_negotiating(self, session: Session) -> None:
        """Handle session negotiating callback.

        Args:
            session (Session): received Session
        """
        pass

    def on_session_established(self, session: Session) -> None:
        """Handle session established callback.

        Args:
            session (Session): received Session
        """
        pass

    def __reset_session_listeners(self) -> None:
        self.__on_session_finished = \
            self.on_session_negotiating = \
            self.on_session_established = \
            self.on_session_authenticating = \
            self.__on_session_failed = self.__empty_method  # noqa: WPS429

    def __on_session_failed(self, session: Session) -> None:
        pass

    def __on_session_finished(self, session: Session) -> None:
        pass

    def __empty_method(self) -> None:
        pass

    def __on_session_finished_callbacks(
        self,
        fut: Future,
        session: Session
    ) -> None:
        self.__on_session_finished(session)
        self.on_session_finished(session)

    def __on_session_failed_callbacks(
        self,
        fut: Future,
        session: Session
    ) -> None:
        self.__on_session_failed(session)
        self.on_session_failed(session)
