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
import rlp

storage = {}
numbers = [i for i in range(100)]
data = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), numbers))
trie = ModifiedMerklePatriciaTrie(storage)

for kv in data:
    trie.put(kv)

proofs = [trie.get_proof_of_inclusion(keccak_hash(rlp.encode(v))) for v in data]
for p in proofs:
    print(p)

# Create the storage
#storage = {}
#trie = ModifiedMerklePatriciaTrie(storage)

# Insert some data
#data = [b'do', b'dog', b'doge', b'horse']

#for d in data:
#    trie.put(d)

#trie.put(b'dogecoin')
#trie.put(b'dogecoiN')
#trie.put(b'dogfcoin')
#trie.put(b'dogfcoin')
#trie.put(b'dogecoiiin')

# Get the proof of inclusion for all the keys
#proofs = []
#for d in data:
#    proofs.append(trie.get_proof_of_inclusion(keccak_hash(rlp.encode(d))))
#print(proofs)

#proof = trie.get_proof_of_inclusion(trie.get_key(value))
##print('Proof: {}'.format(proof))
#print('Proof valid: {}'.format(trie.verify_proof_of_inclusion(trie.get_key(value), proof)))
#print('Tree root: {}'.format(trie.root()))
