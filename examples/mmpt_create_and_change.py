import sys, os

#Following lines are for assigning parent directory dynamically.
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from src.mpt.mmpt import ModifiedMerklePatriciaTrie
from src.mpt.exceptions import BranchPathError, LeafPathError, ExtensionPathError


# Create the storage
storage = {}
trie = ModifiedMerklePatriciaTrie(storage)

# Insert some data
trie.update(b'do', b'a deer')
trie.update(b'dog', b'a doge')
trie.update(b'doge', b'a doge')
trie.update(b'horse', b'a horse')

# Retrieve the data
old_root = trie.root()
old_root_hash = trie.root_hash()
print(old_root_hash)

trie.delete(b'doge')  # Delete one of the datapoints

# Print the old and new root hashes to see if they are different
print("Root hash is {}".format(old_root_hash.hex()))
print("New root hash is {}".format(trie.root_hash().hex()))

# Reload the trie with the old root hash
trie_from_old_hash = ModifiedMerklePatriciaTrie(storage, root=old_root)

print('From the old trie: {}'.format(trie_from_old_hash.get(b'doge')))

try:
    print(trie.get(b'doge'))
except (BranchPathError, LeafPathError, ExtensionPathError):
    print("The key b'doge' is not accessible in a new trie.")