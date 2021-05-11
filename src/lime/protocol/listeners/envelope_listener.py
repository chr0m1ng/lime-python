from abc import ABC
from ..envelope import Envelope


class EnvelopeListener(ABC):
    """Envelope listener callback."""

    def on_envelope(self, envelope: Envelope):
        """Handle callback to handle a received Envelope.

        Args:
            envelope (Envelope): the received Envelope
        """
        pass
