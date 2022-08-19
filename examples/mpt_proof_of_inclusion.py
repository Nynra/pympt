try:
    from mpt import MerklePatriciaTrie, Proof
except (ImportError, ModuleNotFoundError):
    import sys, os
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mpt import MerklePatriciaTrie
    from src.mpt.proof import Proof
from Crypto.Hash import keccak
import random


# Create the storage
#storage = {}
#trie = MerklePatriciaTrie(storage, secure=True)

# Insert some data
#trie.update(b'do', b'verb')
#trie.update(b'dog', b'puppy')
#trie.update(b'doge', b'coin')
#trie.update(b'horse', b'stallion')

# Get the proof of inclusion for the key.
#proof = trie.get_proof_of_inclusion(b'horse')
#print('Proof: {}'.format(proof))
#print('Proof valid: {}'.format(trie.verify_proof_of_inclusion(b'do', proof)))
#print('Tree root: {}'.format(trie.root()))

storage = {}
numbers = [i for i in range(100)]
keys = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), numbers))
trie = MerklePatriciaTrie(storage)

for kv in keys:
    trie.update(kv, kv * 2)

# Generate the proofs
proofs = []
for kv in keys:
    proofs.append(trie.get_proof_of_inclusion(kv))

print(proofs)