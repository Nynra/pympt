from .node import Node, Leaf, Extension
from .mpt import MerklePatriciaTrie as MPT
from .nibble_path import NibblePath


# BUG: #9 If secure mode is used the keys need to be RLP encoded before lookup.
class Proof():
    """
    Child class for the mpt proof of inclusion.

    This class only contains static methods.

    Methods
    -------
    proof_of_inclusion(mpt, key)
        Returns the proof of inclusion for the key.
    verify_proof_of_inclusion(mpt, key, proof)
        Verifies the proof of inclusion for the key.
    """

    @staticmethod
    def proof_of_inclusion(trie, key):
        """
        Proof of inclusion for a key in the trie.

        Parameters
        ----------
        trie : MPT
            MPT to get the proof of inclusion from.
        key : bytes
            Key to get the proof of inclusion for.

        Returns
        -------
        list of bytes
            Proof of inclusion for the key.
        
        """
        # Check if the key is in the trie.
        try:
            trie.get(key)
        except KeyError:
            raise KeyError('Key not found in trie.')
        
        # Create the nibble path
        nibble_path = NibblePath(key)
        length = len(nibble_path)

        # Move up the tree until the root is reached.
        node = trie.root
        proof = []
        index = 0
        while not isinstance(node, Leaf):
            print(length - index)
            nibble_path = NibblePath(key, length - index)
            node = trie.get_node(nibble_path)
            if not isinstance(node, Extension):
                proof.append(node.encode())
                index += 1
            else:
                # Node is an extension node and is not encoded.
                # Get the differnce in pathlength and the node length.
                path_diff = NibblePath(node.next_ref, length - index)
                index += len(path_diff)  # Move the index to the reference

        # Move up the trie until the root node is reached.
        #node = trie.root
        #while not isinstance(node, Leaf):
        #    # Get the child node for the nibble path.
        ##    child_node = node.get_child(nibble_path.at(0))
        #    nibble_path = nibble_path.shift_right()
        #    node = child_node
        
        return proof


    @staticmethod
    def verify_proof_of_inclusion(trie, key, proof, check_duplicates=True,
                                  raise_on_error=False):
        """
        Verify the proof of inclusion for a key in the trie.

        Parameters
        ----------
        trie : MPT
            MPT to verify the proof of inclusion in.
        key : bytes
            Key to verify the proof of inclusion for.
        proof : list of bytes
            Proof of inclusion for the key.
        check_duplicates : bool
            Check for duplicate nodes in the proof.
        raise_on_error : bool
            Raise an exception if the proof is invalid.

        Returns
        -------
        bool
            True if the proof is valid, False otherwise.

        """
        # Verify that none of the items in proof are duplicates
        if check_duplicates:
            if len(set(proof)) != len(proof):
                raise ValueError('Duplicate items in proof.')

        # Verify that the root of the trie is the last item in the proof.
        if proof[-1] != trie.root:
            if raise_on_error:
                raise ValueError('Root of trie not found in proof.')
            else:
                return False

        # Verify that the first node in the proof is the node for the key.
        if proof[0] != key:
            if raise_on_error:
                raise ValueError('First node in proof is not the node for the key.')
            else:
                return False
        
        # Verify that all the keys in the proof are in the trie.
        for p in proof:
            try:
                trie.get(p)
            except KeyError:
                if raise_on_error:
                    raise KeyError('Proof-key not found in trie.')
                else:
                    return False

        # The proof is valid
        return True
        