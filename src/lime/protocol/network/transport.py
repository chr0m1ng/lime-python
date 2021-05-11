from ..envelope import Envelope
from ..listeners import EnvelopeListener


class Transport(EnvelopeListener):
    """Transport interface."""

    def __init__(self, compression: str, encryption: str):
        self.compression = compression
        self.encryption = encryption

    def open(self, uri: str):
        """Open a new connection.

        Args:
            uri (str): the server uri
        """
        pass

    def close(self):
        """Close a open connection."""
        pass

    def send(self, envelope: Envelope):
        """Send a Envelope to the server.

        Args:
            envelope (Envelope): the Envelope to be sent
        """
        pass

    def get_supported_compression(self) -> list[str]:
        """Get supported compressions by the server.

        Returns:
            list[SessionCompression]: a list of supported Compressions
        """  # noqa: DAR202
        pass

    def set_compression(self, compression: str):
        """Set a compression to use with the server.

        Args:
            compression (SessionCompression): the compression to be used
        """  # noqa: DAR103
        pass

    def get_supported_encryption(self) -> list[str]:
        """Get supported encryptions by the server.

        Returns:
            list[SessionEncryption]: a list of supported Encryption
        """  # noqa: DAR202
        pass

    def set_encryption(self, encryption: str):
        """Set a encryption to use with the server.

        Args:
            encryption (SessionEncryption): the encryption to be used
        """  # noqa: DAR103
        pass