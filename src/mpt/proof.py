from .node import Node, Leaf
from .mpt import MerklePatriciaTrie as MPT
from .nibble_path import NibblePath


# BUG: #9 If secure mode is used the keys need to be RLP encoded before lookup.
class Proof():
    """
    Child class for the mpt proof of inclusion.
    """

    @staticmethod
    def proof_of_inclusion(trie, key):
        """
        Proof of inclusion for a key in the trie.
        """
        # Check if the key is in the trie.
        try:
            trie.get(key)
        except KeyError:
            raise KeyError('Key not found in trie.')
        
        # Get the node from the trie storage
        node = trie.get_node(key[1]) 

        # If the key is in the trie, create the proof
        proof = []
        if isinstance(node, Leaf):
            raise Exception('Node is a leaf')
        while not isinstance(node, Leaf):
            print(10)
            proof.append(node.encode())
            node = node.get_child(key[len(node.path):])
        return proof


    @staticmethod
    def verify_proof_of_inclusion(trie, key, proof):
        """
        Verify the proof of inclusion for a key in the trie.
        """
        node = trie.get(key)
        for p in proof:
            node = node.get_child(p[len(node.path):])
        return node.data == key