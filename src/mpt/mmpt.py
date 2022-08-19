from .mpt import MerklePatriciaTrie
from .hash import keccak_hash
from .nibble_path import NibblePath
import rlp


class ModifiedMerklePatriciaTrie(MerklePatriciaTrie):
    """
    The MMPT class is a child of the MPT class and is used to enforce hashing

    A child is used instead of modified the parent so all the tests keep working.
    This class uses the hash of the value as key.

    IMPORTANT: 
    - The hash of the value is used as key.
    - Keys should not be RLP encoded.
    """

    def __init__(self, storage, root=None):
        """
        Initialize the MMPT class.

        Parameters
        ----------
        storage : dict
            The storage of the trie.
        root : bytes
            The root of the trie. If None, the root is set to the empty node.
            If not None, the root is set to the given root.
        
        """
        super().__init__(storage, root, secure=True)

    def get_root_hash(self):
        """
        Get the root hash of the trie.

        Returns
        -------
            The root hash of the trie.

        """
        return super().get_root_hash()

    def update(self, encoded_value):
        """
        Update the value of the certain key.

        Parameters
        ----------
        encoded_value : bytes
            The value of the key.

        Returns
        -------
        None

        """
        encoded_value = rlp.encode(encoded_value)
        super().update(encoded_value, encoded_value)

    def get_key(self, encoded_value):
        """
        Get the key associated with the given value.

        Parameters
        ----------
        encoded_value : bytes
            The value associated with the key.

        Returns
        -------
        bytes
            The key associated with the value.

        """
        return keccak_hash(rlp.encode(encoded_value))

    def get(self, encoded_key):
        """
        Get the value associated with the given key.

        Parameters
        ----------
        encoded_key : bytes
            The key associated with the value.

        Returns
        -------
        bytes
            The value associated with the key.

        """
        if not self._root:
            raise KeyError

        path = NibblePath(encoded_key)
        result_node = self._get(self._root, path)

        return rlp.decode(result_node.data)

    def delete(self, encoded_value):
        """
        Delete the value of the certain key.

        Parameters
        ----------
        encoded_value : bytes
            The value of the key.

        Returns
        -------
        None

        """
        super().delete(rlp.encode(encoded_value))

    def get_proof_of_inclusion(self, encoded_value):
        """
        Get the proof of inclusion of the certain key.

        Parameters
        ----------
        encoded_value : bytes
            The value of the key.

        Returns
        -------
        proof : Proof
            The proof of inclusion of the certain key.

        """
        return super().get_proof_of_inclusion(rlp.encode(encoded_value))

    def verify_proof_of_inclusion(self, encoded_value, proof):
        """
        Verify the proof of inclusion of the certain key.

        Parameters
        ----------
        encoded_value : bytes
            The value of the key.
        proof : Proof
            The proof of inclusion of the certain key.

        Returns
        -------
        bool
            True if the proof is valid, False otherwise.

        """
        return super().verify_proof_of_inclusion(encoded_value, proof)