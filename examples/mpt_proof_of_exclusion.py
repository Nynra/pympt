try:
    from mpt import MerklePatriciaTrie, Proof
except (ImportError, ModuleNotFoundError):
    import sys, os
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mpt import MerklePatriciaTrie


# Create the storage
storage = {}
trie = MerklePatriciaTrie(storage, secure=True)

# Insert some data
#trie.update(b'do', b'verb')
#trie.update(b'dog', b'puppy')
#trie.update(b'doge', b'coin')
#trie.update(b'horse', b'stallion')

numbers = [i for i in range(100)] 
data = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), numbers))

for kv in data:
    trie.update(kv, kv * 2)

keys = [[str(i).encode(), str(i + 1).encode()] for i in range(101, 201)]

proofs = []
for d in keys:
    proofs.append(trie.get_proof_of_exclusion(d[0], d[1]))

print(proofs)
# Get the proof of inclusion for the key.
#proof = trie.get_proof_of_exclusion(b'wolf')
#print('Proof: {}'.format(proof))
#print('Proof valid: {}'.format(trie.verify_proof_of_exclusion(b'wolf', proof)))
#print('Tree root: {}'.format(trie.root()))
