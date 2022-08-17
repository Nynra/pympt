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


# Create the storage
storage = {}
trie = MerklePatriciaTrie(storage)

# Insert some data
trie.update(b'do', b'verb')
trie.update(b'dog', b'puppy')
trie.update(b'doge', b'coin')
trie.update(b'horse', b'stallion')
trie.update(b'domain', b'name')
trie.update(b'dom', b'things')

print(Proof.proof_of_inclusion(trie, b'doge'))
