from abc import ABC
from serializable import Serializable


class Envelope(ABC, Serializable):
    """Envelope representation."""

    def __init__(self, id: str, from_n: str, to: str, pp: str, metadata: dict):
        self.id = id
        self.from_n = from_n
        self.to = to
        self.pp = pp
        self.metadata = metadata


class EnvelopeListener(ABC):
    """Envelope listener callbacks."""

    def on_envelope(self, envelope: Envelope):
        """Handle callback to envelope received event.

        Args:
            envelope (Envelope): the received envelope
        """
        pass
