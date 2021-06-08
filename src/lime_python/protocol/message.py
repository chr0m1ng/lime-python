from typing import Any
from .envelope import Envelope


class Message(Envelope):
    """Message representation."""

    def __init__(
        self,
        type_n: str = None,
        content: Any = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.type_n = type_n
        self.content = content
