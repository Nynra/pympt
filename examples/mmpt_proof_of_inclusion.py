try:
    from mmpt import ModifiedMerklePatriciaTrie
except (ImportError, ModuleNotFoundError):
    import sys, os
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mmpt import ModifiedMerklePatriciaTrie
from Crypto.Hash import keccak
import random


# Create the storage
storage = {}
trie = ModifiedMerklePatriciaTrie(storage)

# Insert some data
trie.update(b'do')
trie.update(b'dog')
trie.update(b'doge')
trie.update(b'horse')
trie.update(b'dogecoin')
trie.update(b'dogecoiN')
trie.update(b'dogfcoin')
trie.update(b'dogfcoin')
trie.update(b'dogecoiiin')

# Get the proof of inclusion for the key.
proof = trie.get_proof_of_inclusion(b'dogecoin')
print('Proof: {}'.format(proof))
print('Proof valid: {}'.format(trie.verify_proof_of_inclusion(b'dogecoin', proof)))
print('Tree root: {}'.format(trie.root()))
