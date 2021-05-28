from typing import List

from src import Envelope, Transport


class TransportDummy(Transport):
    async def open_async(self, uri: str) -> None:
        pass

    def send(self, envelope: Envelope):
        pass

    def get_supported_compression(self) -> List[str]:
        pass

    def get_supported_encryption(self) -> List[str]:
        pass

    def on_envelope(self, envelope: Envelope) -> None:
        pass

    def set_compression(self, compression: str):
        pass

    def set_encryption(self, encryption: str):
        pass

    async def close_async(self) -> None:
        pass
