class Envelope:

    id = str()
    from_n = str()
    to_n = str()
    pp = str()
    metadata = dict()

    is_message = lambda envelope: 'content' in envelope
    is_notification = lambda envelope: 'event' in envelope
    is_command = lambda envelope: 'method' in envelope
    is_session = lambda envelope: 'state' in envelope

class EnvelopeListener:

    on_envelope = lambda envelope: None