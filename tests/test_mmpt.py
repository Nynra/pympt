import sys, os
try:
    from mpt.mmpt import ModifiedMerklePatriciaTrie
    from mpt.node import Node
    from mpt.hash import keccak_hash
except (ImportError, ModuleNotFoundError):
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mmpt import ModifiedMerklePatriciaTrie
    from src.mpt.node import Node
    from src.mpt.errors import PoeError, PoiError, KeyNotFoundError, LeafPathError
    from src.mpt.hash import keccak_hash
    from src.mpt.proof import Proof
import rlp
from rlp.exceptions import DecodingError
import unittest
import random
import pickle


class TestMMPT(unittest.TestCase):
    """Test the ModifiedMerklePatriciaTrie class."""

    def test_insert_get_one_short(self):
        """Test inserting one short key-value pair and then getting it."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        value = b'value'
        trie.put(value)
        gotten_value = trie.get(keccak_hash(rlp.encode(value)))

        self.assertEqual(value, gotten_value)

        with self.assertRaises(KeyNotFoundError):
            trie.get(b'no_key')

    def test_insert_get_one_long(self):
        """Test inserting one long key-value pair and then getting it."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        value = b'value_0000000000000000000000000000000000000000000000000000000000000000'
        trie.put(value)
        gotten_value = trie.get(keccak_hash(rlp.encode(value)))

        self.assertEqual(value, gotten_value)

    def test_insert_get_many(self):
        """Test inserting many values and then getting them."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'verb')
        trie.put(b'puppy')
        trie.put(b'coin')
        trie.put(b'stallion')

        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'verb'))), b'verb')
        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'puppy'))), b'puppy')
        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'coin'))), b'coin')
        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'stallion'))), b'stallion')

    def test_insert_get_lots(self):
        """Test inserting lots of values and then getting them."""
        random.seed(42)
        storage = {}
        rand_numbers = [random.randint(1, 1000000) for _ in range(100)]
        keys = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), rand_numbers))

        trie = ModifiedMerklePatriciaTrie(storage)

        for kv in keys:
            trie.put(kv)

        for kv in keys:
            self.assertEqual(trie.get(keccak_hash(rlp.encode(kv))), kv)

    def test_delete_one(self):
        """Test deleting one value and then getting it."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'key')
        trie.delete(keccak_hash(rlp.encode(b'key')))

        with self.assertRaises(KeyError):
            trie.get(keccak_hash(rlp.encode(b'key')))

    def test_delete_many(self):
        """Test deleting many values and then getting them."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'do')
        trie.put(b'dog')
        trie.put(b'doge')
        trie.put(b'horse')

        root_hash = trie.root_hash()

        trie.put(b'a')
        trie.put(b'some_key')
        trie.put(b'dodog')

        trie.delete(keccak_hash(rlp.encode(b'a')))
        trie.delete(keccak_hash(rlp.encode(b'some_key')))
        trie.delete(keccak_hash(rlp.encode('dodog')))

        new_root_hash = trie.root_hash()

        self.assertEqual(root_hash, new_root_hash)

    def test_delete_lots(self):
        """Test deleting lots of values and then getting them."""
        random.seed(42)
        storage = {}
        rand_numbers = set([random.randint(1, 1000000) for _ in range(100)])  # Unique only.
        keys = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), rand_numbers))
        trie = ModifiedMerklePatriciaTrie(storage)

        for kv in keys:
            trie.put(kv)

        for kv in keys:
            trie.delete(keccak_hash(rlp.encode(kv)))

        self.assertEqual(trie.root_hash(), Node.EMPTY_HASH)

    def test_update_get_one(self):
        """Test updating one value and then getting it."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        value = b'value'
        new_value = b'new value'

        trie.put(value)  # Insert the value.
        trie.update(new_value, keccak_hash(rlp.encode(value)))  # Update the value.
        gotten_value = trie.get(keccak_hash(rlp.encode(new_value)))

        self.assertEqual(new_value, gotten_value)

        with self.assertRaises(KeyNotFoundError):
            trie.get(b'no_key')

    def test_update_none_existing(self):
        """Test updating one value that is not in the tree."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'value')  # Insert the value.

        with self.assertRaises(LeafPathError):
            trie.update(b'new value', keccak_hash(rlp.encode(b'no_key')))

    def test_update_get_many(self):
        """Test updating many values and then getting them."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        values = [b'verb', b'puppy', b'coin', b'stallion']
        new_values = [b'new verb', b'new puppy', b'new coin', b'new stallion']

        # Put the values in the trie.
        for i in range(len(values)):
            trie.put(values[i])

        # Update the values in the trie.
        for i in range(len(values)):
            trie.update(new_values[i], keccak_hash(rlp.encode(values[i])))

        # Get the values from the trie.
        for i in range(len(values)):
            self.assertEqual(trie.get(keccak_hash(rlp.encode(new_values[i]))), new_values[i])

    def test_update_get_lots(self):
        """Test inserting lots of values and then getting them."""
        random.seed(42)
        storage = {}
        rand_numbers = [random.randint(1, 1000000) for _ in range(100)]
        values = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), rand_numbers))

        new_values = [b'new {}' + v for v in values]

        trie = ModifiedMerklePatriciaTrie(storage)

        # Put the values in the trie.
        for v in values:
            trie.put(v)

        # Update the values in the trie.
        for i in range(len(values)):
            trie.update(new_values[i], keccak_hash(rlp.encode(values[i])))

        # Get the values from the trie.
        for v in new_values:
            self.assertEqual(trie.get(keccak_hash(rlp.encode(v))), v)

    def test_root_hash(self):
        """Test getting the root hash of a trie."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'do')
        trie.put(b'dog')
        trie.put(b'doge')
        trie.put(b'horse')

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('ac9bdffdaf45f979ab0bf7cbdcf02a3094da734b242e247764b2809cdd8d13bc'))

    def test_root_hash_after_updates(self):
        """Test getting the root hash of a trie after updates."""
        storage = {}

        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'do')
        trie.put(b'dog')
        trie.put(b'doge')
        trie.put(b'horse')

        trie.update(b'dog', keccak_hash(rlp.encode(b'dog')))
        trie.update(b'doge', keccak_hash(rlp.encode(b'doge')))
        trie.update(b'horse', keccak_hash(rlp.encode(b'horse')))

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('ac9bdffdaf45f979ab0bf7cbdcf02a3094da734b242e247764b2809cdd8d13bc'))

    def test_root_hash_after_deletes(self):
        """Test getting the root hash of a trie after deletes."""
        storage = {}

        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'do')
        trie.put(b'dog')
        trie.put(b'doge')
        trie.put(b'horse')

        trie.put(b'dodo')
        trie.put(b'hover')
        trie.put(b'capital')
        trie.put(b'a')

        trie.delete(keccak_hash(rlp.encode(b'dodo')))
        trie.delete(keccak_hash(rlp.encode(b'hover')))
        trie.delete(keccak_hash(rlp.encode(b'capital')))
        trie.delete(keccak_hash(rlp.encode(b'a')))

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('ac9bdffdaf45f979ab0bf7cbdcf02a3094da734b242e247764b2809cdd8d13bc'))

    def test_trie_from_old_root(self):
        """Test getting the root hash of a trie after deletes and updates."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'do')
        trie.put(b'dog')

        root_hash = trie.root()

        trie.delete(keccak_hash(rlp.encode(b'dog')))
        trie.update(b'do', keccak_hash(rlp.encode(b'do')))

        trie_from_old = ModifiedMerklePatriciaTrie(storage, root_hash)

        # Old.
        self.assertEqual(trie_from_old.get(keccak_hash(rlp.encode(b'do'))), b'do')
        self.assertEqual(trie_from_old.get(keccak_hash(rlp.encode(b'dog'))), b'dog')

        # New.
        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'do'))), b'do')
        with self.assertRaises(KeyNotFoundError):
            trie.get(keccak_hash(rlp.encode(b'dog')))

    def test_trie_from_old_root_after_updates(self):
        """Test getting the root hash of a trie after deletes and updates."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'do')
        trie.put(b'dog')

        root_hash = trie.root()

        trie.update(b'do', keccak_hash(rlp.encode(b'do')))
        trie.update(b'dog', keccak_hash(rlp.encode(b'dog')))

        trie_from_old = ModifiedMerklePatriciaTrie(storage, root_hash)

        # Old.
        self.assertEqual(trie_from_old.get(keccak_hash(rlp.encode(b'do'))), b'do')
        self.assertEqual(trie_from_old.get(keccak_hash(rlp.encode(b'dog'))), b'dog')

        # New.
        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'do'))), b'do')
        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'dog'))), b'dog')


class Test_proof(unittest.TestCase):
    """Test the proof class.""" 

    def test_change_attributes(self):
        """Test if the proof hash is correct."""
        trie = ModifiedMerklePatriciaTrie()

        # Add some data
        trie.put(b'do')
        trie.put(b'dog')
        trie.put(b'doge')
        trie.put(b'horse')

        # Get the proof for the key 'doge'.
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(b'doge')))

        with self.assertRaises(AttributeError):
            proof.trie_root = b'5'
        with self.assertRaises(AttributeError):
            proof.target = b'5'
        with self.assertRaises(AttributeError):
            proof.proof = b'5'


class Test_proof_of_inclusion(unittest.TestCase):
    """Test the proof functions of the MMPT."""
    files = {'one_proof': 'tests/test_proofs/mmpt_one_poi.pkl',
             'many_proofs': 'tests/test_proofs/mmpt_many_poi.pkl',
             'lots_of_proofs': 'tests/test_proofs/mmpt_lots_of_poi.pkl'}

    def test_proof_on_empty_trie(self):
        """Test getting the proof of an empty trie."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        with self.assertRaises(ValueError):
            trie.get_proof_of_inclusion(keccak_hash(rlp.encode(b'')))

    def test_root_hash(self):
        """Test if the root hash of the trie is correct."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'dog')
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(b'dog')))
        self.assertEqual(proof.trie_root, trie.root_hash(), 
                        'The root hash in the proof does not mathc the trie root.')
    
    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'dog')
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(b'dog')))
        
        with open(self.files['one_proof'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proof)):
            for j in range(len(proof[i])):
                self.assertEqual(proof[i][j], expected[i][j], 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate a proof for each key
        proofs = [trie.get_proof_of_inclusion(keccak_hash(rlp.encode(kv))).proof for kv in data]
        with open(self.files['many_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            for j in range(len(proofs[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected.')

    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [str(i).encode() for i in range(100)]
        for kv in data:
            trie.put(kv)

        proofs = [trie.get_proof_of_inclusion(keccak_hash(rlp.encode(kv))).proof for kv in data]

        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            for j in range(len(proofs[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected.')
    
    def test_valid(self):
        """Test if the validation function wokrs."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        for i in range(len(data)):
            proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(data[i])))
            self.assertTrue(trie.verify_proof_of_inclusion(proof), 
                    'Proof for {} is not valid.'.format(data[i]))

    # Test if the proof is valid when one point is removed
    def test_verify_one_item_removed(self):
        """Test if the proof is still valid after removing one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(b'doge')))
        trie.delete(keccak_hash(rlp.encode(b'do')))
        with self.assertRaises(KeyError):
            trie.verify_proof_of_inclusion(proof) 


    # Test if the proof is valid when one point is added
    def test_verify_one_point_added(self):
        """Test if the proof is still valid after adding one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(data[2])))
        trie.put(b'testing')
        with self.assertRaises(KeyError):
            trie.verify_proof_of_inclusion(proof) 

    # Test if the proof is valid when one char is removed
    def test_verify_one_char_removed(self):
        """Test if the proof is still valid after removing one char from the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(data[2])))
        proof = Proof(target_key_hash=og_proof.target, proof_hash=og_proof.proof[:-1],
                    root_hash=og_proof.trie_root, type=og_proof.type)
        self.assertFalse(trie.verify_proof_of_inclusion(proof), 
                        'Proof should not be valid.')

    # Test if the proof is valid when one char is added
    def test_verify_one_char_added(self):
        """Test if the proof is still valid after adding one char to the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(data[2])))
        proof = []
        for i in range(len(og_proof.proof)):
            proof.append(og_proof.proof[i] + b'o')
        proof = Proof(target_key_hash=og_proof.target, proof_hash=proof,
                    root_hash=og_proof.trie_root, type=og_proof.type)

        with self.assertRaises(DecodingError):
            _ = trie.verify_proof_of_inclusion(proof)


class Test_proof_of_exclusion(unittest.TestCase):
    """Test the proof functions of the MMPT."""
    files = {'one_proof': 'tests/test_proofs/mmpt_one_proof.pkl',
             'many_proofs': 'tests/test_proofs/mmpt_many_proofs.pkl',
             'lots_of_proofs': 'tests/test_proofs/mmpt_lots_of_proofs.pkl'}     

    def test_proof_on_empty_trie(self):
        """Test getting the proof of an empty trie."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        with self.assertRaises(ValueError):
            trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))

    def test_root_hash(self):
        """Test if the root hash of the trie is correct."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'dog')
        proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        self.assertEqual(proof.trie_root, trie.root_hash(), 
                        'The root hash in the proof does not mathc the trie root.')

    def test_proof_on_existing_key(self):
        """Test getting the proof of an existing key."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        for d in data:
            with self.assertRaises(PoeError):
                # An error should be raises because the key is in the trie
                _ = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(d)))

    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'dog')
        proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        
        with open(self.files['one_proof'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proof)):
            for j in range(len(proof[i])):
                self.assertEqual(proof[i][j], expected[i][j], 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate some non existing keys
        keys = [keccak_hash(rlp.encode(i)) for i in range(4)]

        # Load the expected proofs
        proofs = [trie.get_proof_of_exclusion(kv).proof for kv in keys]
        with open(self.files['many_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            for j in range(len(proofs[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected.')

    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [str(i).encode() for i in range(100)]
        for d in data:
            trie.put(d)

        # Generate the proof for eacht item
        keys = [keccak_hash(rlp.encode(d)) for d in range(101, 201)]

        proofs = []
        for d in keys:
            proofs.append(trie.get_proof_of_exclusion(d).proof)

        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            for j in range(len(proofs[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected.')
            
    def test_valid(self):
        """Test if the validation function wokrs."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate the proof for eacht item
        keys = [b'wolf', b'giraffe', b'tiger', b'lion']

        # Get the proofs and validate
        for i in range(len(keys)):
            proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(keys[i])))
            self.assertTrue(trie.verify_proof_of_exclusion(proof), 
                    'Proof for {} is not valid.'.format(keys[i]))

    # Test if the proof is valid when one point is removed
    def test_verify_one_item_removed(self):
        """Test if the proof is still valid after removing one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate the proof for eacht item
        keys = [b'wolf', b'giraffe', b'tiger', b'lion']
        proofs = [trie.get_proof_of_exclusion(keccak_hash(rlp.encode(k))) for k in keys]
        trie.delete(keccak_hash(rlp.encode(b'do')))
        for proof in proofs:
            with self.assertRaises(KeyError):
                trie.verify_proof_of_exclusion(proof) 


    # Test if the proof is valid when one point is added
    def test_verify_one_point_added(self):
        """Test if the proof is still valid after adding one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate the proof for eacht item
        keys = [b'wolf', b'giraffe', b'tiger', b'lion']
        proofs = [trie.get_proof_of_exclusion(keccak_hash(rlp.encode(k))) for k in keys]
        trie.put(b'bear')
        for proof in proofs:
            with self.assertRaises(KeyError):
                trie.verify_proof_of_exclusion(proof) 

    # Test if the proof is valid when one char is removed
    def test_verify_one_char_removed(self):
        """Test if the proof is still valid after removing one char from the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        proof = []
        for i in range(len(og_proof.proof)):
            proof.append(og_proof.proof[i][:-1])

        proof = Proof(target_key_hash=og_proof.target, proof_hash=proof,
                    root_hash=og_proof.trie_root, type=og_proof.type)
        with self.assertRaises(DecodingError):
            _ = trie.verify_proof_of_exclusion(proof)

    # Test if the proof is valid when one char is added
    def test_verify_one_char_added(self):
        """Test if the proof is still valid after adding one char to the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        proof = []
        for i in range(len(og_proof.proof)):
            proof.append(og_proof.proof[i] + b'o')
        proof = Proof(target_key_hash=og_proof.target, proof_hash=proof,
                    root_hash=og_proof.trie_root, type=og_proof.type)
        with self.assertRaises(DecodingError):
            _ = trie.verify_proof_of_exclusion(proof)


class Test_save_and_load(unittest.TestCase):
    """Test if the trie can be saved and loaded."""

    def test_save_and_load_one_value(self):
        """Test if the trie can be saved and loaded with one value."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do']
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Check if the data is still there
        for kv in data:
            self.assertEqual(trie.get(keccak_hash(rlp.encode(kv))), kv, 'Data not found in trie.')

    def test_save_and_load_multiple_values(self):
        """Test if the trie can be saved and loaded with multiple values."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Check if the data is still there
        for kv in data:
            self.assertEqual(trie.get(keccak_hash(rlp.encode(kv))), kv, 'Data not found in trie.')

    def test_save_and_load_lot_of_values(self):
        """Test if the trie can be saved and loaded with lot of values."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [str(i).encode() for i in range(100)]
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Check if the data is still there
        for kv in data:
            self.assertEqual(trie.get(keccak_hash(rlp.encode(kv))), kv, 'Data not found in trie.')

    def test_save_and_load_new_item_to_copy(self):
        """Test if the roots differ when an item is only added to original."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Add new item
        new_trie.put(b'new')

        self.assertNotEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are equal but should not be.')
    
    def test_save_and_load_new_item(self):
        """Test if the roots differ when a new value is added to original and copy."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Add new item
        new_trie.put(b'new')
        trie.put(b'new')

        self.assertEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are not equal but should be.')

    def test_save_and_load_remove_item(self):
        """Test if the roots differ when an item is removed from original and copy."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Remove an item
        new_trie.delete(keccak_hash(rlp.encode(data[0])))
        trie.delete(keccak_hash(rlp.encode(data[0])))

        self.assertEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are not equal but should be.')

    def test_save_and_load_update_item(self):
        """Test if the roots differ when an item is updated in original and copy."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Update an item
        new_trie.update(b'new', keccak_hash(rlp.encode(b'dog')))
        trie.update(b'new', keccak_hash(rlp.encode(b'dog')))

        self.assertEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are not equal but should be.')

    def test_proof_on_copy(self):
        """Test if the proof is correct when the original is modified."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Create proof on original
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(data[0])))

        # Add data to the original (invalidates the proof on the original trie)
        trie.put(b'new')

        # Verify that the proof is invalid on the original trie
        with self.assertRaises(KeyError):
            trie.verify_proof_of_inclusion(proof)
        
        # Verify proof on the copy
        self.assertTrue(new_trie.verify_proof_of_inclusion(proof))

