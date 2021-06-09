from asyncio import Future
from typing import Any, Awaitable

from pytest import fixture, mark
from pytest_mock import MockerFixture

from src import (ClientChannel, PlainAuthentication, Session,
                 SessionCompression, SessionEncryption, SessionState)

from .transport_dummy import TransportDummy

SESSION_ID = '1234'
SEND_SESSION_METHOD = 'send_session'
TO = 'me@take.net'
FROM_N = 'you@take.net'


class TestClientChannel:

    @fixture(autouse=True)
    def target(self) -> ClientChannel:
        yield ClientChannel(
            TransportDummy(SessionCompression.NONE, SessionEncryption.NONE),
            False,
            False
        )

    @mark.asyncio
    async def test_start_new_session_async(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        target.state = SessionState.NEW

        spy = mocker.spy(target, SEND_SESSION_METHOD)
        sent_session = Session(SessionState.NEW)

        # Act
        target.start_new_session_async()

        # Assert
        sent_session.id = spy.call_args[0][0].id
        spy.assert_called_once_with(sent_session)

    @mark.asyncio
    async def test_negotiate_session_async(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        target.state = SessionState.NEGOTIATING

        spy = mocker.spy(target, SEND_SESSION_METHOD)
        sent_session = Session(
            SessionState.NEGOTIATING,
            compression=SessionCompression.GZIP,
            encryption=SessionEncryption.TLS
        )

        # Act
        target.negotiate_session_async(
            SessionCompression.GZIP,
            SessionEncryption.TLS
        )

        # Assert
        sent_session.id = spy.call_args[0][0].id
        spy.assert_called_once_with(sent_session)

    @mark.asyncio
    async def test_authenticate_session_async(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        target.state = SessionState.AUTHENTICATING
        target.session_id = SESSION_ID

        spy = mocker.spy(target, SEND_SESSION_METHOD)
        identity = 'test@take.net'
        instance = 'test'
        authentication = PlainAuthentication('any-pswd')
        sent_session = Session(
            SessionState.AUTHENTICATING,
            scheme=authentication.scheme,
            authentication=authentication
        )
        sent_session.from_n = f'{identity}/{instance}'
        sent_session.id = SESSION_ID

        # Act
        target.authenticate_session_async(
            identity,
            authentication,
            instance
        )

        # Assert
        spy.assert_called_once_with(sent_session)

    @mark.asyncio
    async def test_send_finishing_session_async(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        target.state = SessionState.ESTABLISHED
        target.session_id = SESSION_ID

        spy = mocker.spy(target, SEND_SESSION_METHOD)
        sent_session = Session(SessionState.FINISHING)
        sent_session.id = SESSION_ID

        # Act
        target.send_finishing_session_async()

        # Assert
        spy.assert_called_once_with(sent_session)

    @mark.asyncio
    async def test_on_session_established(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        session = Session(SessionState.ESTABLISHED)
        session.id = SESSION_ID
        session.to = TO
        session.from_n = FROM_N

        spy = mocker.spy(target, 'on_session_established')
        # Act
        target.on_session(session)

        # Assert
        spy.assert_called_once_with(session)
        assert target.local_node == str(session.to)
        assert target.remote_node == session.from_n

    @mark.asyncio
    async def test_on_session_negotiating(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        session = Session(SessionState.NEGOTIATING)
        session.id = SESSION_ID

        spy = mocker.spy(target, 'on_session_negotiating')
        # Act
        target.on_session(session)

        # Assert
        spy.assert_called_once_with(session)

    @mark.asyncio
    async def test_on_session_authenticating(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        session = Session(SessionState.AUTHENTICATING)
        session.id = SESSION_ID

        spy = mocker.spy(target, 'on_session_authenticating')
        # Act
        target.on_session(session)

        # Assert
        spy.assert_called_once_with(session)

    @mark.asyncio
    async def test_on_session_finished(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        session = Session(SessionState.FINISHED)
        session.id = SESSION_ID

        spy_transport = mocker.spy(target.transport, 'close_async')
        # Act
        target.on_session(session)

        # Assert
        spy_transport.assert_called_once()

    @mark.asyncio
    async def test_on_session_failed(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        session = Session(SessionState.FAILED)
        session.id = SESSION_ID

        spy_transport = mocker.spy(target.transport, 'close_async')
        # Act
        target.on_session(session)

        # Assert
        spy_transport.assert_called_once()

    @mark.asyncio
    async def test_establish_session_async(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        compression = SessionCompression.GZIP
        encryption = SessionEncryption.TLS
        identity = TO
        authentication = PlainAuthentication('any-pswd')
        instance = 'test'

        target.state = SessionState.NEW

        start_result = Session(SessionState.AUTHENTICATING)

        auth_result = Session(SessionState.ESTABLISHED)

        mocker.patch.object(  # noqa: WPS316
            target,
            'start_new_session_async',
            return_value=self.__async_return(start_result)
        )
        mocker.patch.object(
            target,
            'authenticate_session_async',
            return_value=self.__async_return(auth_result)
        )

        # Act
        result: Future = await target.establish_session_async(
            compression,
            encryption,
            identity,
            authentication,
            instance
        )

        # Assert
        assert result == Session(SessionState.ESTABLISHED)

    @mark.asyncio
    async def test_establish_session_async_with_encryption_compression_options(
        self,
        mocker: MockerFixture,
        target: ClientChannel
    ) -> None:
        # Arrange
        compression = None
        encryption = None
        identity = TO
        authentication = PlainAuthentication('any-pswd')
        instance = 'test'

        target.state = SessionState.NEW

        start_result = Session(
            SessionState.NEGOTIATING,
            encryption_options=[SessionEncryption.TLS],
            compression_options=[SessionCompression.GZIP]
        )

        neg_result = Session(SessionState.AUTHENTICATING)

        auth_result = Session(SessionState.ESTABLISHED)

        mocker.patch.object(  # noqa: WPS316
            target,
            'start_new_session_async',
            return_value=self.__async_return(start_result)
        )
        mocker.patch.object(  # noqa: WPS316
            target,
            'negotiate_session_async',
            return_value=self.__async_return(neg_result)
        )
        mocker.patch.object(
            target,
            'authenticate_session_async',
            return_value=self.__async_return(auth_result)
        )

        # Act
        result: Future = await target.establish_session_async(
            compression,
            encryption,
            identity,
            authentication,
            instance
        )

        # Assert
        assert result == Session(SessionState.ESTABLISHED)

    def __async_return(self, result: Any) -> Awaitable[Any]:
        fut = Future()
        fut.set_result(result)
        return fut
