from .mpt import MerklePatriciaTrie
from .hash import keccak_hash
from .nibble_path import NibblePath
from .node import Node, _prepare_reference_for_encoding, _prepare_reference_for_usage
from .proof import Proof
import rlp
import pickle


class ModifiedMerklePatriciaTrie(MerklePatriciaTrie):
    """
    The MMPT class is a child of the MPT class and used to store and verify data.

    This means a stored value is stored under the key keccak_hash(rlp.encode(value)).

    Methods
    -------
    update(encoded_value, encoded_old_key)
        Update the value of the certain key. If the key does not exist, it is created.
    get(encoded_key)
        Get the value associated with the given key.
    delete(encoded_value)
        Delete the value from the trie.
    get_proof_of_inclusion(encoded_key)
        Get the proof of inclusion for a certain key (and thus also value).
    verify_proof_of_inclusion(encoded_key, proof)
        Verify the proof of inclusion for a certain key (and thus also value).
    get_proof_of_excllusion(encoded_key)
        Get the proof of exclusion for a certain key (and thus also value).
    verify_proof_of_exclusion(encoded_key, proof)
        Verify the proof of exclusion for a certain key (and thus also value).
    to_pickle()
        Convert the trie to a pickle object.
    from_pickle(pickle_data)
        Initialize the trie from a pickle object.
    
    """

    def __init__(self, storage={}, root=None):
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
        self._type = 'FULL MMPT'
        super().__init__(storage, root, secure=True)

    # SAVING AND LOADING
    def to_pickle(self):
        """
        Convert the trie to a json object.

        Returns
        -------
        bytes
            The pickled trie.

        """
        if self._type == 'FULL MMPT':
            storage_list = [_prepare_reference_for_encoding(node) for node in self._storage.values()]
            content =  {'root': self._root,
                        'type': self._type,
                        'storage': storage_list}
        else:
            raise NotImplementedError("Saving a {} trie to json is not implemented".format(self.state))

        return pickle.dumps(content)

    def from_pickle(self, pickle_data):
        """
        Initialize the trie from a pickle object.

        Parameters
        ----------
        pickle_data : bytes
            The pickle object.
        """ 
        # Unpickle the object
        data = pickle.loads(pickle_data)
        storage_list = data['storage']

        # Load the storage
        if data['type'] == 'FULL MMPT':
            storage = {}
            for encoded_node in storage_list:
                # Nodes are stored as the RPL encoded version of the full node
                storage[keccak_hash(encoded_node)] = _prepare_reference_for_usage(encoded_node)  # Decode the node from RLP

            self._storage = storage
            self._root = data['root']
            self._type = data['type']
        else:
            raise NotImplementedError("Loading a {} trie from a json object is not implemented".format(data['type']))

    def create_skeleton(self):
        """
        Create a skeleton of the trie.

        The skeleton is a trie with only the root node.
        The root node is the root of the trie.
        The storage is empty.
        The state is 'SKELETON MMPT'
        """
        raise NotImplementedError("Creating a skeleton is not yet implemented.")

    # PROOF FUNCTIONS
    def get_proof_of_inclusion(self, key):
        """
        Get the proof of inclusion of the certain key.

        Parameters
        ----------
        key : bytes
            The key for wich the proof of inclusion is requested.

        Returns
        -------
        proof : Proof
            The proof of inclusion of the certain key.

        """
        return Proof(target_key_hash=key, root_hash=self.root(),
                     proof_hash=super().get_proof_of_inclusion(key),
                     type='POI')

    def verify_proof_of_inclusion(self, proof):
        """
        Verify the proof of inclusion of the certain key.

        Parameters
        ----------
        proof : Proof
            The proof of inclusion of the certain key.

        Returns
        -------
        bool
            True if the proof is valid, False otherwise.

        """
        if not isinstance(proof, Proof):
            raise TypeError("The proof must be a Proof object.")

        return super().verify_proof_of_inclusion(proof.target, proof.proof)

    def get_proof_of_exclusion(self, key):
        """
        Get the proof of exclusion for a certain key.

        Parameters
        ----------
        key : bytes
            The key for wich the proof of exclusion is requested.

        Returns
        -------
        proof : Proof
            The proof of exclusion for the certain key.

        """
        return Proof(target_key_hash=key, root_hash=self.root_hash(),
                     proof_hash=super().get_proof_of_exclusion(key),
                     type='POE')

    def verify_proof_of_exclusion(self, proof):
        """
        Verify the proof of exclusion of the certain key.

        Parameters
        ----------
        proof : Proof
            The proof of exclusion of the key.

        Returns
        -------
        bool
            True if the proof is valid, False otherwise.

        """
        if not isinstance(proof, Proof):
            raise TypeError("The proof must be a Proof object.")
        return super().verify_proof_of_exclusion(proof.target, proof.proof)

