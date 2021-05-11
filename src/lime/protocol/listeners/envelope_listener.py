from abc import ABC
from ..envelope import Envelope


class EnvelopeListener(ABC):
    """Envelope listener callbacks."""

    def on_envelope(self, envelope: Envelope):
        """Handle callback to envelope received event.

        Args:
            envelope (Envelope): the received envelope
        """
        pass
