from abc import abstractmethod
from typing import List

from ..listeners import EnvelopeListener


class Transport(EnvelopeListener):
    """Transport interface."""

    def __init__(self, compression: str, encryption: str) -> None:
        self.compression = compression
        self.encryption = encryption

    @abstractmethod
    async def open_async(self, uri: str = None) -> None:
        """Open a new connection.

        Args:
            uri (str): the server uri
        """
        pass

    @abstractmethod
    async def close_async(self) -> None:
        """Close a open connection."""
        pass

    @abstractmethod
    def send(self, envelope: dict) -> None:
        """Send a Envelope to the server.

        Args:
            envelope (dict): the serialized Envelope to be sent
        """
        pass

    @abstractmethod
    def get_supported_compression(self) -> List[str]:
        """Get supported compressions by the server.

        Returns:
            list[SessionCompression]: a list of supported Compressions
        """  # noqa: DAR202
        pass

    @abstractmethod
    def set_compression(self, compression: str) -> None:
        """Set a compression to use with the server.

        Args:
            compression (SessionCompression): the compression to be used
        """  # noqa: DAR103
        pass

    @abstractmethod
    def get_supported_encryption(self) -> List[str]:
        """Get supported encryptions by the server.

        Returns:
            list[SessionEncryption]: a list of supported Encryption
        """  # noqa: DAR202
        pass

    @abstractmethod
    def set_encryption(self, encryption: str) -> None:
        """Set a encryption to use with the server.

        Args:
            encryption (SessionEncryption): the encryption to be used
        """  # noqa: DAR103
        pass
