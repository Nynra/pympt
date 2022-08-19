from .mpt import MerklePatriciaTrie
from .hash import keccak_hash
from .nibble_path import NibblePath
import rlp


class ModifiedMerklePatriciaTrie(MerklePatriciaTrie):
    """
    The MMPT class is a child of the MPT class and ised to store and verify data

    A child is used instead of modified the parent so all the tests keep working.
    This class uses the rpl encoded hash of the value as key.

    IMPORTANT: 
    - The hash of the value is used as key.
    - Keys should not be RLP encoded when passed to a function.

    This means a stored value is stored under the key keccak_hash(rlp.encode(value)).

    Methods
    -------
    update(encoded_value, encoded_old_key)
        Update the value of the certain key. 
    get_key(encoded_value)
        Get the key associated with the given value.
    put(encoded_value)
        Put the value in the trie.
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
        return {'root': self.root_hash(),
                'proof': super().get_proof_of_inclusion(encoded_key, hash_key=False),
                'target': encoded_key}

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
        if proof['root'] != self.root_hash():
            raise KeyError("The supplied root is not meant for this trie.")
        if proof['target'] != encoded_key:
            raise KeyError('The supplied proof is not meant for the given key.')
        
        return super().verify_proof_of_inclusion(encoded_key, proof['proof'], hash_key=False)


