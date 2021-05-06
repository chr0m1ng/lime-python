from .serializable import Serializable
from abc import ABC

class Envelope(ABC, Serializable):

    def __init__(self): pass

    def __init__(self, id: str, from_n: str, to: str, pp: str, metadata):
        self.id = id
        self.from_n = from_n
        self.to = to
        self.pp = pp
        self.metadata = metadata


class EnvelopeListener(ABC):
    def on_envelope(envelope: Envelope): pass