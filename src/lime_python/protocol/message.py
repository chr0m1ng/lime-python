from .envelope import Envelope


class Message(Envelope):
    """Message representation."""

    def __init__(self, type_n: str, content) -> None:
        super().__init__()
        self.type_n = type_n
        self.content = content
