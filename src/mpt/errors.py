# Some custom errors to easier identify problems and catch errors.
class KeyNotFoundError(Exception):
    """
    Exception raised when a key is not found in the trie.

    This error is meanth to create a different error for dictionary KeyErrors
    and Trie KeyErrors. KeyNotFoundError is for when a nibblepath is not found,
    KeyError for when a node in the storage (dict) is not found.
    """

    def __init__(self, message):
        super().__init__(message)


# Following errors are for making debugging easier. This way we can see what kind
# of node produces the error
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


class InvalidNodeError(Exception):
    """
    Exception raised when a node an invalid type.
    """

    def __init__(self, message):
        super().__init__(message)


# For distinction between proof of inclusion and exclusion
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
