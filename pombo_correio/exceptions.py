class NoSession(RuntimeError):
    """ forgot to call new_session()"""


class ElementNotFound(ValueError):
    """ no element to process """


class FireFoxCrashed(EnvironmentError):
    """ ouch, the browser itself crashed"""


class InvalidElement(ValueError):
    """ not a valid element object """


class InvalidTabID(ValueError):
    """ not a valid tab id """
