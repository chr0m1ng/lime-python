class SessionState:
    """Session state."""

    NEW = 'new'
    NEGOTIATING = 'negotiating'
    AUTHENTICATING = 'authenticating'
    ESTABLISHED = 'established'
    FINISHING = 'finishing'
    FINISHED = 'finished'
    FAILED = 'failed'
