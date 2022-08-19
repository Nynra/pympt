try:
    from mpt.mmpt import Modified_merkle_patricia_trie
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

# Retrieve the data
old_root = trie.root()
old_root_hash = trie.root_hash()
print(old_root_hash)

trie.delete(trie.get_key(b'doge'))  # Delete one of the datapoints

# Print the old and new root hashes to see if they are different
print("Root hash is {}".format(old_root_hash.hex()))
print("New root hash is {}".format(trie.root_hash().hex()))

# Reload the trie with the old root hash
trie_from_old_hash = ModifiedMerklePatriciaTrie(storage, root=old_root)

print(trie_from_old_hash.get(trie_from_old_hash.get_key(b'doge')))

try:
    print(trie.get(b'doge'))
except KeyError:
    print('Not accessible in a new trie.')