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
trie.update(b'do', b'verb')
trie.update(b'dog', b'puppy')
trie.update(b'doge', b'coin')
trie.update(b'horse', b'poney')
trie.update(b'dogecoin', b'crypto')

proof = trie.get_proof_of_exclusion(b'wolf')

print('Proof dict:')
for i, j in proof.items():
   print(i, ':', j)
print('\nProof valid: {}'.format(trie.verify_proof_of_exclusion(proof)))
