from .mpt import MerklePatriciaTrie
from .hash import keccak_hash
from .nibble_path import NibblePath
from .node import Node, _prepare_reference_for_encoding, _prepare_reference_for_usage
from .proof import Proof
import rlp
import pickle


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
        """
        if self._type == 'FULL MMPT':
            # TODO: Only encode the node if it isnt already encoded, now it is possibly decoded and encoded again
            # Get all the nodes (decoded) and RLP encode them
            storage_list = [_prepare_reference_for_encoding(node) for node in self._storage.values()]
            content =  {'root': self._root,
                        'type': self._type,
                        'storage': storage_list}
        else:
            raise NotImplementedError("Saving a {} trie to json is not implemented".format(self.state))

        return pickle.dumps(content)

    def from_pickle(self, json_string):
        """
        Initialize the trie from a pickle object.
        """ 
        # Unpickle the object
        binary_string = pickle.loads(json_string)
        storage_list = binary_string['storage']

        # Load the storage
        if binary_string['type'] == 'FULL MMPT':
            storage = {}
            for encoded_node in storage_list:
                # Nodes are stored as the RPL encoded version of the full node

                # TODO: Make sure the node is encoded when put into the storage
                storage[keccak_hash(encoded_node)] = _prepare_reference_for_usage(encoded_node)  # Decode the node from RLP

            self._storage = storage
            self._root = binary_string['root']
            # print('Root type = {}'.format(type(self._root)))
            self._type = binary_string['type']
        else:
            raise NotImplementedError("Loading a {} trie from a json object is not implemented".format(binary_string['type']))

    def create_skeleton(self):
        """
        Create a skeleton of the trie.

        The skeleton is a trie with only the root node.
        The root node is the root of the trie.
        The storage is empty.
        The state is 'SKELETON MMPT'
        """
        raise NotImplementedError("Creating a skeleton is not yet implemented.")

    # TRIE FUNCTINOS
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

    # PROOF FUNCTIONS
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
        return Proof(target_key_hash=encoded_key, root_hash=self.root_hash(),
                     proof_hash=super().get_proof_of_inclusion(encoded_key, hash_key=False),
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
        if proof.trie_root != self.root_hash():
            raise KeyError("The supplied root is not meant for this trie.")
        if proof.type != 'POI':
            raise KeyError('The supplied proof is not a proof of inclusion.')

        return super().verify_proof_of_inclusion(proof.target, proof.proof, 
                                                hash_key=False)

    def get_proof_of_exclusion(self, encoded_key):
        """
        Get the proof of exclusion for a certain key.

        Parameters
        ----------
        encoded_key : bytes
            The key for wich the proof of exclusion is requested.

        Returns
        -------
        proof : Proof
            The proof of exclusion for the certain key.

        """
        return Proof(target_key_hash=encoded_key, root_hash=self.root_hash(),
                     proof_hash=super().get_proof_of_exclusiom(encoded_key, hash_key=False),
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
        if proof.root_hash != self.root_hash():
            raise KeyError("The supplied root is not meant for this trie.")
        if proof.type != 'POI':
            raise KeyError('The supplied proof is not a proof of inclusion.')

        return super().verify_proof_of_inclusion(proof.target_hash, proof.proof_hash, 
                                                hash_key=False)

