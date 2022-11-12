try:
    from mpt import MerklePatriciaTrie, Proof
except (ImportError, ModuleNotFoundError):
    import sys, os
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mpt import MerklePatriciaTrie
    from src.mpt.node import Node
import pickle

# Create the storage
storage = {}
trie = MerklePatriciaTrie(storage, secure=True)

data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
for kv in data:
    trie.update(kv[0], kv[1])

keys = [[str(i).encode(), str(i + 1).encode()] for i in range(len(data))]
# Load the proofs from the file
proofs = [trie.get_proof_of_exclusion(k) for k, v in keys]

for i, key in enumerate(keys):
    if not trie.verify_proof_of_exclusion(key, proofs[i]):
        raise Exception('Proof of exclusion is invalid')
with open('mpt_many_poe.pkl', 'wb') as f:
    pickle.dump(proofs, f)
    
# Insert some data
#trie.update(b'do', b'verb')
#trie.update(b'dog', b'puppy')
#trie.update(b'doge', b'coin')
#trie.update(b'horse', b'stallion')

#print(trie.contains(b'wo'))

# Get the proof of inclusion for the key.
#proof = trie.get_proof_of_exclusion(b'wolf')
#print('Proof: {}'.format(proof))
#print('Proof valid: {}'.format(trie.verify_proof_of_exclusion(b'wolf', proof)))
#print('Tree root: {}'.format(trie.root()))
