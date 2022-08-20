try:
    from mpt.mmpt import ModifiedMerklePatriciaTrie
    from mpt.hash import keccak_hash
except (ImportError, ModuleNotFoundError):
    import sys, os
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mmpt import ModifiedMerklePatriciaTrie
    from src.mpt.hash import keccak_hash
import pickle


# Create the storage
storage = {}
trie = ModifiedMerklePatriciaTrie(storage)

# Insert some data
trie.put(b'do')
trie.put(b'dog')
trie.put(b'doge')
trie.put(b'doggo')
trie.put(b'horse')

trie_file = trie.to_pickle() # Get the trie in json form
trie_from_json = ModifiedMerklePatriciaTrie()
trie_from_json.from_pickle(trie_file)

# Get a key from the original and the value from the new trie
key = trie.get_key(b'doge')
print('Value in original: {}'.format(trie.get(key)))
print('Value from copy : {}'.format(trie_from_json.get(key)))