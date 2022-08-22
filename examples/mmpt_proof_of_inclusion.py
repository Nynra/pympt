try:
    from mpt.mmpt import ModifiedMerklePatriciaTrie
except (ImportError, ModuleNotFoundError):
    import sys, os
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mmpt import ModifiedMerklePatriciaTrie

# Create the storage
storage = {}
trie = ModifiedMerklePatriciaTrie(storage)

# Insert some data
trie.put(b'do')
trie.put(b'dog')
trie.put(b'doge')
trie.put(b'horse')
trie.put(b'dogecoin')
trie.put(b'dogecoiN')
trie.put(b'dogfcoin')
trie.put(b'dogfcoin')
trie.put(b'dogecoiiin')

# Get the proof of inclusion for the key
key = b'dog'
proof = trie.get_proof_of_inclusion(trie.get_key(key))

print('Proof dict:')
for i, j in proof.items():
    print(i, ':', j)

print('\nProof valid: {}'.format(trie.verify_proof_of_inclusion(trie.root(), proof)))

