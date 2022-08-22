# Some custom errors to easier identify problems and catch errors.
class KeyNotFoundError(Exception):
    """
    Exception raised when a key is not found in the trie.
    """

    def __init__(self, message):
        super().__init__(message)


class ExtensionPathError(Exception):
    """
    Exception raised when an extension path is not valid.
    """

    def __init__(self, message):
        super().__init__(message)


class LeafPathError(Exception):
    """
    Exception raised when a leaf path is not valid.
    """

    def __init__(self, message):
        super().__init__(message)


class BranchPathError(Exception):
    """
    Exception raised when a branch path is not valid.
    """

    def __init__(self, message):
        super().__init__(message)


class PoeError(Exception):
    """
    Exception raised when POE cannot be generated.
    """

    def __init__(self, message):
        super().__init__(message)


class PoiError(Exception):
    """
    Exception raised when POI cannot generated.
    """

    def __init__(self, message):
        super().__init__(message)


class InvalidNodeError(Exception):
    """
    Exception raised when a node is invalid.
    """

    def __init__(self, message):
        super().__init__(message)