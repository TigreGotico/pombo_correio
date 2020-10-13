class DriverNotSet(EnvironmentError):
    """ webdriver not initialized """


class NoSession(RuntimeError):
    """ forgot to call new_session()"""


class ElementNotFound(ValueError):
    """ no element to process """


class TabDiscarded(RuntimeError):
    """ tab no longer exists"""


class FireFoxCrashed(EnvironmentError):
    """ ouch, sounds like the browser itself crashed"""


class InvalidElement(ValueError):
    """ not a valid element object """


class InvalidTabID(ValueError):
    """ not a valid tab id """


class TorNotFound(EnvironmentError):
    """ tor not found in xdg path or wrong binary path specified"""


class PreferencesFileNotFound(FileNotFoundError):
    """ """


class PreferencesParseError(RuntimeError):
    """ failed to parse prefs.js """
