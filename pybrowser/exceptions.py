class NoSession(RuntimeError):
    """ forgot to call new_session()"""


class ElementNotFound(RuntimeError):
    """ no element to process """
