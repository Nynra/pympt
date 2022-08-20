from .mpt import MerklePatriciaTrie as MPT
from datetime import datetime
import pickle


class Proof():
    """
    Class to hold the information for different kind of proofs.

    IMPORTANT: The attributes of the proof cannot be changed aferter creation.

    Attributes
    ----------
    timestamp : datetime
        Timestamp of the proof.
    target : bytes
        Hash of the target key.
    trie_root : bytes
        Hash of the root of the trie.
    proof : bytes
        Hash of the proof.
    type : str
        Type of the proof (POI or POE).

    Methods
    -------
    to_json()
        Convert the proof to a json object.
    to_pickle()
        Convert the proof to a pickle object.
    
    """

    def __init__(self, target_key_hash, root_hash, proof_hash, type):
        """
        Initialize the proof.

        Parameters
        ----------
        target_key_hash : bytes
            Hash of the target key.
        root_hash : bytes
            Hash of the root of the trie.
        proof_hash : bytes
            Hash of the proof.
        type : str
            Type of the proof (POI or POE).

        """
        self._timestamp = datetime.now()
        self._target_key_hash = target_key_hash
        self._root_hash = root_hash
        self._proof_hash = proof_hash
        self._type = type

    def to_json(self):
        """
        Convert the proof to a json object.

        Returns
        -------
        dict
            The proof as a json object (dict).

        """
        return {'type': self._type,
                'timestamp': self._timestamp,
                'target_key_hash': self._target_key_hash.hex(),
                'root_hash': self._root_hash.hex(),
                'proof_hash': self._proof_hash.hex()}

    def to_pickle(self):
        """
        Convert the proof to a pickle object.

        Returns
        -------
        bytes
            The proof as a pickle object in bytes.

        """
        return pickle.dumps(self.to_json())

    # ATTRIBUTES
    @property
    def timestamp(self):
        return self._timestamp

    @property
    def target(self):
        return self._target_key_hash

    @property
    def trie_root(self):
        return self._root_hash

    @property
    def proof(self):
        return self._proof_hash

    @property
    def type(self):
        return self._type