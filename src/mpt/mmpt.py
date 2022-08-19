from mpt import MerklePatriciaTrie
import rlp


class Modified_merkle_patricia_trie(MerklePatriciaTrie):
    """
    The MMPT class is a child of the MPT class and is used to enforce hashing

    A child is used instead of modified the parent so all the tests keep working.
    This class uses the hash of the value as key.
    """

    def __init__(self, storage, root=None):
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