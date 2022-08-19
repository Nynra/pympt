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

    This means a stored value is stored under the key keccak_hash(rlp.encode(value)).

    Methods
    -------
    update(encoded_value)
        Update the value of the certain key. If the key is not yet in the trie,
        it is added.
    get_key(encoded_value)
        Get the key associated with the given value.
    get(encoded_key)
        Get the value associated with the given key.
    delete(encoded_value)
        Delete the value from the trie.
    get_proof_of_inclusion(encoded_key)
        Get the proof of inclusion for a certain key (and thus also value).
    verify_proof_of_inclusion(encoded_key, proof)
        Verify the proof of inclusion for a certain key (and thus also value).
    
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

    def put(self, encoded_value):
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

    def update(self, encoded_value, encoded_old_key):
        """
        Update the value of the certain key.

        Doesnt actually update the value but deletes the old key and adds the new key.

        Parameters
        ----------
        encoded_value : bytes
            The value of the key.
        encoded_old_key : bytes
            The old key of the value.

        Returns
        -------
        None

        """
        encoded_value = rlp.encode(encoded_value)

        # TODO: Check if the old key is in the trie

        # Check if the new and old key are the same
        if encoded_old_key == encoded_value:
            return

        # Delete the old key
        try:
            super().delete(encoded_old_key, hash_key=False)
        except KeyError:
            # The old key is not in the trie
            raise KeyError("The old key is not in the trie")
            pass

        # Add the new key	
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
        # Generate the key dont search for the value
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

    def delete(self, encoded_key):
        """
        Delete the value of the certain key.

        Parameters
        ----------
        encoded_key : bytes
            The key of the value to be deleted.

        Returns
        -------
        None

        """
        super().delete(encoded_key, hash_key=False)

    def get_proof_of_inclusion(self, encoded_key):
        """
        Get the proof of inclusion of the certain key.

        Parameters
        ----------
        encoded_key : bytes
            The key for wich the proof of inclusion is requested.

        Returns
        -------
        proof : Proof
            The proof of inclusion of the certain key.

        """
        return super().get_proof_of_inclusion(encoded_key, hash_key=False)

    def verify_proof_of_inclusion(self, encoded_key, proof):
        """
        Verify the proof of inclusion of the certain key.

        Parameters
        ----------
        encoded_key : bytes
            The key for wich the proof was created.
        proof : Proof
            The proof of inclusion of the key.

        Returns
        -------
        bool
            True if the proof is valid, False otherwise.

        """
        return super().verify_proof_of_inclusion(encoded_key, proof)


