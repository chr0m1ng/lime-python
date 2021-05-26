from asyncio import Future
import pytest
from pytest_mock import MockerFixture

from src import (ClientChannel, PlainAuthentication, Session,
                 SessionCompression, SessionEncryption, SessionState)

from .transport_dummy import TransportDummy

SESSION_ID = '1234'
SEND_SESSION_METHOD = 'send_session'
TO = 'me@take.net'
FROM_N = 'you@take.net'


class TestClientChannel:

    @pytest.mark.asyncio
    async def test_start_new_session_async(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()
        client.state = SessionState.NEW

        spy = mocker.spy(client, SEND_SESSION_METHOD)
        sent_session = Session(SessionState.NEW)

        # Act
        client.start_new_session_async()

        # Assert
        spy.assert_called_once_with(sent_session)

    @pytest.mark.asyncio
    async def test_negotiate_session_async(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()
        client.state = SessionState.NEGOTIATING

        spy = mocker.spy(client, SEND_SESSION_METHOD)
        sent_session = Session(
            SessionState.NEGOTIATING,
            compression=SessionCompression.GZIP,
            encryption=SessionEncryption.TLS
        )

        # Act
        client.negotiate_session_async(
            SessionCompression.GZIP,
            SessionEncryption.TLS
        )

        # Assert
        spy.assert_called_once_with(sent_session)

    @pytest.mark.asyncio
    async def test_authenticate_session_async(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()
        client.state = SessionState.AUTHENTICATING
        client.session_id = SESSION_ID

        spy = mocker.spy(client, SEND_SESSION_METHOD)
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
        client.authenticate_session_async(
            identity,
            authentication,
            instance
        )

        # Assert
        spy.assert_called_once_with(sent_session)

    @pytest.mark.asyncio
    async def test_send_finishing_session_async(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()
        client.state = SessionState.ESTABLISHED
        client.session_id = SESSION_ID

        spy = mocker.spy(client, SEND_SESSION_METHOD)
        sent_session = Session(SessionState.FINISHING)
        sent_session.id = SESSION_ID

        # Act
        client.send_finishing_session_async()

        # Assert
        spy.assert_called_once_with(sent_session)

    @pytest.mark.asyncio
    async def test_on_session_established(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()

        session = Session(SessionState.ESTABLISHED)
        session.id = SESSION_ID
        session.to = TO
        session.from_n = FROM_N

        spy = mocker.spy(client, 'on_session_established')
        # Act
        client.on_session(session)

        # Assert
        spy.assert_called_once_with(session)
        assert client.local_node == str(session.to)
        assert client.remote_node == session.from_n

    @pytest.mark.asyncio
    async def test_on_session_negotiating(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()

        session = Session(SessionState.NEGOTIATING)
        session.id = SESSION_ID

        spy = mocker.spy(client, 'on_session_negotiating')
        # Act
        client.on_session(session)

        # Assert
        spy.assert_called_once_with(session)

    @pytest.mark.asyncio
    async def test_on_session_authenticating(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()

        session = Session(SessionState.AUTHENTICATING)
        session.id = SESSION_ID

        spy = mocker.spy(client, 'on_session_authenticating')
        # Act
        client.on_session(session)

        # Assert
        spy.assert_called_once_with(session)

    @pytest.mark.asyncio
    async def test_on_session_finished(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()

        session = Session(SessionState.FINISHED)
        session.id = SESSION_ID

        spy = mocker.spy(client, 'on_session_finished')
        spy_transport = mocker.spy(client.transport, 'close_async')
        # Act
        client.on_session(session)

        # Assert
        spy.assert_called_once_with(session)
        spy_transport.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_session_failed(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()

        session = Session(SessionState.FAILED)
        session.id = SESSION_ID

        spy = mocker.spy(client, 'on_session_failed')
        spy_transport = mocker.spy(client.transport, 'close_async')
        # Act
        client.on_session(session)

        # Assert
        spy.assert_called_once_with(session)
        spy_transport.assert_called_once()

    @pytest.mark.asyncio
    async def test_establish_session_async(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()
        compression = SessionCompression.GZIP
        encryption = SessionEncryption.TLS
        identity = TO
        authentication = PlainAuthentication('any-pswd')
        instance = 'test'

        client.state = SessionState.NEW

        start_result = Session(SessionState.AUTHENTICATING)

        auth_result = Session(SessionState.ESTABLISHED)

        mocker.patch.object(  # noqa: WPS316
            client,
            'start_new_session_async',
            return_value=self.__async_return(start_result)
        )
        mocker.patch.object(
            client,
            'authenticate_session_async',
            return_value=self.__async_return(auth_result)
        )

        # Act
        result: Future = await client.establish_session_async(
            compression,
            encryption,
            identity,
            authentication,
            instance
        )

        # Assert
        assert result == Session(SessionState.ESTABLISHED)

    @pytest.mark.asyncio
    async def test_establish_session_async_with_encryption_compression_options(
        self,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        client = self.__get_target()
        compression = None
        encryption = None
        identity = TO
        authentication = PlainAuthentication('any-pswd')
        instance = 'test'

        client.state = SessionState.NEW

        start_result = Session(
            SessionState.NEGOTIATING,
            encryption_options=[SessionEncryption.TLS],
            compression_options=[SessionCompression.GZIP]
        )

        neg_result = Session(SessionState.AUTHENTICATING)

        auth_result = Session(SessionState.ESTABLISHED)

        mocker.patch.object(  # noqa: WPS316
            client,
            'start_new_session_async',
            return_value=self.__async_return(start_result)
        )
        mocker.patch.object(  # noqa: WPS316
            client,
            'negotiate_session_async',
            return_value=self.__async_return(neg_result)
        )
        mocker.patch.object(
            client,
            'authenticate_session_async',
            return_value=self.__async_return(auth_result)
        )

        # Act
        result: Future = await client.establish_session_async(
            compression,
            encryption,
            identity,
            authentication,
            instance
        )

        # Assert
        assert result == Session(SessionState.ESTABLISHED)

    def __get_target(
        self,
        compression: str = SessionCompression.NONE,
        encryption: str = SessionEncryption.NONE,
        auto_reply_pings: bool = False,
        auto_notify_receipt: bool = False
    ) -> ClientChannel:
        return ClientChannel(
            TransportDummy(compression, encryption),
            auto_reply_pings,
            auto_notify_receipt
        )

    def __async_return(self, result) -> Future:
        fut = Future()
        fut.set_result(result)
        return fut
