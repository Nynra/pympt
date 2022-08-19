from Crypto.Hash import keccak


def keccak_hash(data):
    """
    Hash data with keccak256 algorithm.
    
    Parameters
    ----------
    data : bytes
        Data to hash.
        
    Returns
    -------
    bytes
        Hash of the data.
        
    """
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(data)
    return keccak_hash.digest()


def keccak_hash_list(data):
    """
    Hash list of data with keccak256 algorithm.
    
    Parameters
    ----------
    data : list of bytes
        Data to hash.
        
    Returns
    -------
    bytes
        Hash of the data.
        
    """
    keccak_hash = keccak.new(digest_bits=256)
    for item in data:
        keccak_hash.update(item)
    return keccak_hash.digest()