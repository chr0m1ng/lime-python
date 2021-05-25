from abc import ABC, abstractmethod

from ..envelope import Envelope


class EnvelopeListener(ABC):
    """Envelope listener callback."""

    @abstractmethod
    def on_envelope(self, envelope: Envelope) -> None:
        """Handle callback to handle a received Envelope.

        Args:
            envelope (Envelope): the received Envelope
        """
        pass
