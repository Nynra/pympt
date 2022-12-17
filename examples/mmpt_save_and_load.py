import sys, os

# Following lines are for assigning parent directory dynamically.
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from src.mpt.mmpt import ModifiedMerklePatriciaTrie


# Create the storage
storage = {}
trie = ModifiedMerklePatriciaTrie(storage)

# Insert some data
trie.update(b"do", b"a deer")
trie.update(b"dog", b"a doge")
trie.update(b"doge", b"a Doge")
trie.update(b"doggo", b"a Doggo")
trie.update(b"horse", b"a horse")

trie_file = trie.to_pickle()  # Get the trie in json form
trie_from_json = ModifiedMerklePatriciaTrie()
trie_from_json.from_pickle(trie_file)

# Get a key from the original and the value from the new trie
print("Value in original: {}".format(trie.get(b"doge")))
print("Value from copy : {}".format(trie_from_json.get(b"doge")))
