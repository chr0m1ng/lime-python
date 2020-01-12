from .channel import Channel
from ..session import SessionState, Session
import asyncio


class ClientChannel(Channel):

    def __init__(self, transport, auto_reply_pings=True, auto_notify_receipt=False):
        super().__init__(transport, auto_reply_pings, auto_notify_receipt)

    async def establish_session(self, compression, encryption, identity, authentication, instance):
        if self.state != SessionState.NEW:
            raise Exception(
                f'Cannot establish a session in the {self.state.value} state'
            )

        session = await self.start_new_session()

        if session.encryption_options is not None or session.compression_options is not None:
            cmpr = compression if compression is not None else session.compression_options[0]
            encrp = encryption if encryption is not None else session.encryption_options[0]
            session = await self.negotiate_session(cmpr, encrp)

        # Apply transport options
        if session.compression != self.transport.compression:
            self.transport.set_compression(session.compression)

        if session.encryption != self.transport.encryption:
            self.transport.set_encryption(session.encryption)

        session = await self.authenticate_session(identity, authentication, instance)
        self.__reset_session_listeners()

        return session

    def on_message(self, message): pass

    def on_notification(self, notification): pass

    async def on_session(self, session):
        self.session_id = session.id
        self.state = session.state

        if session.state == SessionState.ESTABLISHED:
            self.local_node = session.to_n
            self.remote_node = session.from_n

        if session.state == SessionState.NEGOTIATING:
            self.__on_session_negotiating(session)
        elif session.state == SessionState.AUTHENTICATING:
            self.__on_session_authenticating(session)
        elif session.state == SessionState.ESTABLISHED:
            self.__on_session_established(session)
        elif session.state == SessionState.FINISHED:
            await self.transport.close()
            self.on_session_finished(session)
            self.__on_session_finished(session)
        elif session.state == SessionState.FAILED:
            await self.transport.close()
            self.on_session_failed(session)
            self.__on_session_failed(session)

    def start_new_session(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        if self.state != SessionState.NEW:
            raise Exception(
                f'Cannot start a session in the {self.state.value} state'
            )

        future = loop.create_future()

        self.__on_session_failed = future.set_exception
        self.__on_session_negotiating = self.__on_session_authenticating = future.set_result

        session = Session()
        session.state = SessionState.NEW

        self.send_session(session)

        return future

    def negotiate_session(self, session_compression, session_encryption):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        if self.state != SessionState.NEGOTIATING:
            raise Exception(
                f'Cannot negotiate a session in the {self.state.value} state'
            )

        future = loop.create_future()

        self.__on_session_failed = future.set_exception
        self.__on_session_authenticating = future.set_result

        session = Session()
        session.id = self.session_id
        session.state = SessionState.NEGOTIATING
        session.compression = session_compression
        session.encryption = session_encryption

        self.send_session(session)

        return future

    def authenticate_session(self, identity, authentication, instance):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        if self.state != SessionState.AUTHENTICATING:
            raise Exception(
                f'Cannot authenticate a session in the {self.state.value} state'
            )

        future = loop.create_future()

        self.__on_session_failed = future.set_exception
        self.__on_session_established = future.set_result

        session = Session()
        session.id = self.session_id
        session.state = SessionState.AUTHENTICATING
        session.from_n = f'{identity}/{instance}'
        session.scheme = authentication.scheme if authentication.scheme is not None else 'unknown'
        session.authentication = authentication

        self.send_session(session)

        return future

    def send_finishing_session(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        if self.state != SessionState.ESTABLISHED:
            raise Exception(
                f'Cannot finish a session in the {self.state.value} state'
            )

        future = loop.create_future()

        self.__on_session_failed = future.set_exception
        self.__on_session_finished = future.set_result

        session = Session()
        session.id = self.session_id
        session.state = SessionState.FINISHING

        self.send_session(session)

        return future

    def on_session_finished(self, session): pass

    def on_session_failed(self, session): pass

    def __reset_session_listeners(self):
        self.__on_session_negotiating = \
            self.__on_session_authenticating = \
            self.__on_session_established = \
            self.__on_session_finished = \
            self.__on_session_failed = lambda: None
