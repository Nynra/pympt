import sys, os
try:
    from mpt import MerklePatriciaTrie
    from mpt.node import Node
except (ImportError, ModuleNotFoundError):
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mpt import MerklePatriciaTrie
    from src.mpt.node import Node
    from src.mpt.errors import InvalidNodeError, LeafPathError, ExtensionPathError, BranchPathError, KeyNotFoundError, PoeError, PoiError
import rlp
import unittest
import random
import pickle
from rlp.exceptions import DecodingError


class TestMPT(unittest.TestCase):
    def test_insert_get_one_short(self):
        """Test inserting one short key-value pair and then getting it."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        key = rlp.encode(b'key')
        value = rlp.encode(b'value')
        trie.update(key, value)
        gotten_value = trie.get(key)

        self.assertEqual(value, gotten_value)

        with self.assertRaises(KeyNotFoundError):
            trie.get(rlp.encode(b'no_key'))

    def test_insert_get_one_long(self):
        """Test inserting one long key-value pair and then getting it."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        key = rlp.encode(b'key_0000000000000000000000000000000000000000000000000000000000000000')
        value = rlp.encode(b'value_0000000000000000000000000000000000000000000000000000000000000000')
        trie.update(key, value)
        gotten_value = trie.get(key)

        self.assertEqual(value, gotten_value)

    def test_insert_get_many(self):
        """Test inserting many key-value pairs and then getting them."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy')
        trie.update(b'doge', b'coin')
        trie.update(b'horse', b'stallion')

        self.assertEqual(trie.get(b'do'), b'verb')
        self.assertEqual(trie.get(b'dog'), b'puppy')
        self.assertEqual(trie.get(b'doge'), b'coin')
        self.assertEqual(trie.get(b'horse'), b'stallion')

    def test_insert_get_lots(self):
        """Test inserting lots of key-value pairs and then getting them."""
        random.seed(42)
        storage = {}
        rand_numbers = [random.randint(1, 1000000) for _ in range(100)]
        keys = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), rand_numbers))

        trie = MerklePatriciaTrie(storage)

        for kv in keys:
            trie.update(kv, kv * 2)

        for kv in keys:
            self.assertEqual(trie.get(kv), kv * 2)

    def test_delete_one(self):
        """Test deleting one key-value pair and then getting it."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'key', b'value')
        trie.delete(b'key')

        with self.assertRaises(KeyNotFoundError):
            trie.get(b'key')

    def test_delete_many(self):
        """Test deleting many key-value pairs and then getting them."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy')
        trie.update(b'doge', b'coin')
        trie.update(b'horse', b'stallion')

        root_hash = trie.root_hash()

        trie.update(b'a', b'aaa')
        trie.update(b'some_key', b'some_value')
        trie.update(b'dodog', b'do_dog')

        trie.delete(b'a')
        trie.delete(b'some_key')
        trie.delete(b'dodog')

        new_root_hash = trie.root_hash()

        self.assertEqual(root_hash, new_root_hash)

    def test_delete_lots(self):
        """Test deleting lots of key-value pairs and then getting them."""
        random.seed(42)
        storage = {}
        rand_numbers = set([random.randint(1, 1000000) for _ in range(100)])  # Unique only.
        keys = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), rand_numbers))

        trie = MerklePatriciaTrie(storage)

        for kv in keys:
            trie.update(kv, kv * 2)

        for kv in keys:
            trie.delete(kv)

        self.assertEqual(trie.root_hash(), Node.EMPTY_HASH)

    def test_root_hash(self):
        """Test getting the root hash of a trie."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy')
        trie.update(b'doge', b'coin')
        trie.update(b'horse', b'stallion')

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('5991bb8c6514148a29db676a14ac506cd2cd5775ace63c30a4fe457715e9ac84'))

    def test_root_hash_after_updates(self):
        """Test getting the root hash of a trie after updates."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy1')
        trie.update(b'doge', b'coin1')
        trie.update(b'horse', b'stallion1')

        trie.update(b'dog', b'puppy')
        trie.update(b'doge', b'coin')
        trie.update(b'horse', b'stallion')

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('5991bb8c6514148a29db676a14ac506cd2cd5775ace63c30a4fe457715e9ac84'))

    def test_root_hash_after_deletes(self):
        """Test getting the root hash of a trie after deletes."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy')
        trie.update(b'doge', b'coin')
        trie.update(b'horse', b'stallion')

        trie.update(b'dodo', b'pizza')
        trie.update(b'hover', b'board')
        trie.update(b'capital', b'Moscow')
        trie.update(b'a', b'b')

        trie.delete(b'dodo')
        trie.delete(b'hover')
        trie.delete(b'capital')
        trie.delete(b'a')

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('5991bb8c6514148a29db676a14ac506cd2cd5775ace63c30a4fe457715e9ac84'))

    def test_trie_from_old_root(self):
        """Test getting the root hash of a trie after deletes."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy')

        root_hash = trie.root()

        trie.delete(b'dog')
        trie.update(b'do', b'not_a_verb')

        trie_from_old = MerklePatriciaTrie(storage, root_hash)

        # Old.
        self.assertEqual(trie_from_old.get(b'do'), b'verb')
        self.assertEqual(trie_from_old.get(b'dog'), b'puppy')

        # New.
        self.assertEqual(trie.get(b'do'), b'not_a_verb')
        with self.assertRaises(KeyNotFoundError):
            trie.get(b'dog')

    def test_contains(self):
        """Test checking if a key is in the trie."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy')
        trie.update(b'doge', b'coin')
        trie.update(b'horse', b'stallion')

        # Test exising keys
        self.assertTrue(trie.contains(b'do'))
        self.assertTrue(trie.contains(b'dog'))
        self.assertTrue(trie.contains(b'doge'))
        self.assertTrue(trie.contains(b'horse'))

        # Test non-existing keys
        self.assertFalse(trie.contains(b'horse2'))
        self.assertFalse(trie.contains(b'doe'))
        self.assertFalse(trie.contains(b'dogi'))

        # Test some numbers
        keys = [str(i).encode() for i in range(101, 201)]
        for k in keys:
            self.assertFalse(trie.contains(k))

    def test_contains_secure(self):
        """Test checking if a key is in the trie."""
        storage = {}

        trie = MerklePatriciaTrie(storage, secure=True)

        trie.update(b'do', b'verb')
        trie.update(b'dog', b'puppy')
        trie.update(b'doge', b'coin')
        trie.update(b'horse', b'stallion')

        # Test exising keys
        self.assertTrue(trie.contains(b'do'))
        self.assertTrue(trie.contains(b'dog'))
        self.assertTrue(trie.contains(b'doge'))
        self.assertTrue(trie.contains(b'horse'))

        # Test non-existing keys
        self.assertFalse(trie.contains(b'horse2'))
        self.assertFalse(trie.contains(b'doe'))
        self.assertFalse(trie.contains(b'dogi'))

        # Test some numbers
        keys = [str(i).encode() for i in range(101, 201)]
        for k in keys:
            self.assertFalse(trie.contains(k))

    def test_contains_empty(self):
        """Test checking if a key is in the trie."""
        storage = {}

        trie = MerklePatriciaTrie(storage)

        self.assertFalse(trie.contains(b'do'))
        self.assertFalse(trie.contains(b'dog'))
        self.assertFalse(trie.contains(b'doge'))
        self.assertFalse(trie.contains(b'horse'))


class Test_proof_of_inclusion(unittest.TestCase):
    """Test the proof functions of the MPT."""
    files = {'lots_of_proofs': 'tests/test_proofs/mpt_lots_of_poi.pkl',
             'one_proof': 'tests/test_proofs/mpt_one_poi.pkl',
             'many_proofs': 'tests/test_proofs/mpt_many_poi.pkl'}

    def test_proof_on_empty_trie(self):
        """Test getting the proof of an empty trie."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        with self.assertRaises(ValueError):
            trie.get_proof_of_inclusion(b'')
    
    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)

        trie.update(b'dog', b'puppy')

        proof = trie.get_proof_of_inclusion(b'dog')
        with open(self.files['one_proof'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proof)):
            self.assertEqual(proof[i], expected[i], 'Proof does not match expected')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)

        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Generate a proof for each key
        proofs = [trie.get_proof_of_inclusion(kv[0]) for kv in data]
        with open(self.files['many_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            for j in range(len(expected[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected')
    
    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)
        numbers = [i for i in range(100)]
        data = [[str(i).encode(), str(i * 2).encode()] for i in numbers]

        for kv in data:
            trie.update(kv[0], kv[1])

        proofs = [trie.get_proof_of_inclusion(kv[0]) for kv in data]

        # Load the proof file
        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            for j in range(len(expected[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected')
    
    def test_valid(self):
        """Test if the validation function will validate the self generated hash."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Load the proof file
        proofs = [trie.get_proof_of_inclusion(kv[0]) for kv in data]

        for i in range(len(proofs)):
            self.assertTrue(trie.verify_proof_of_inclusion(data[i][0], proofs[i]), 'Proof does not validate for {}, got {}.'.format(data[i], proofs[i])) 

    # Test if the proof is valid when one point is removed
    def test_verify_one_point_removed(self):
        """Test if the proof is still valid after removing one point."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(data[2][0])
        trie.delete(data[3][0])
        self.assertFalse(trie.verify_proof_of_inclusion(data[2][0], proof), 'Proof should not be valid.')

    # Test if the proof is valid when one point is added
    def test_verify_one_point_added(self):
        """Test if the proof is still valid after adding one point."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(data[2][0])
        trie.update(b'testing', b'testing')
        self.assertEqual(trie.verify_proof_of_inclusion(data[2][0], proof), False, 'Proof should not be valid.')

    # Test if the proof is valid when one char is removed
    def test_verify_one_char_removed(self):
        """Test if the proof is still valid after removing one char from the proof."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(data[2][0])
        for i in range(len(proof)):
            proof[i] = proof[i][:-1]

        self.assertFalse(trie.verify_proof_of_inclusion(data[2][0], proof[:-1]))

    # Test if the proof is valid when one char is added
    def test_verify_one_char_added(self):
        """Test if the proof is still valid after adding one char from the proof."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(data[2][0])
        for i in range(len(proof)):
            proof[i] += b'o'

        self.assertFalse(trie.verify_proof_of_inclusion(data[2][0], proof))


class Test_proof_of_exclusion(unittest.TestCase):
    """Test the proof functions of the MMPT."""
    files = {'lots_of_proofs': 'tests/test_proofs/mpt_lots_of_poe.pkl',
             'one_proof': 'tests/test_proofs/mpt_one_poe.pkl',
             'many_proofs': 'tests/test_proofs/mpt_many_poe.pkl'}

    def test_proof_on_empty_trie(self):
        """Test getting the proof of an empty trie."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        with self.assertRaises(ValueError):
            trie.get_proof_of_exclusion(b'wolf')

    def test_proof_on_existing_key(self):
        """Test getting the proof of an existing key."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        for kv in data:
            with self.assertRaises(PoeError):
                # An error should be raises because the key is in the trie
                _ = trie.get_proof_of_exclusion(kv[0])

    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)

        trie.update(b'dog', b'puppy')
        proof = trie.get_proof_of_exclusion(b'wolf')
        
        with open(self.files['one_proof'], 'rb') as f:
            expected = pickle.load(f)

        # Compare the components of the proofs
        for i in range(len(proof)):
            for j in range(len(proof[i])):
                self.assertEqual(proof[i][j], expected[i][j])
   
    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)

        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        keys = [[str(i).encode(), str(i + 1).encode()] for i in range(len(data))]

        # Load the proofs from the file
        proofs = [trie.get_proof_of_exclusion(k) for k, v in keys]
        with open(self.files['many_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        numbers = [i for i in range(100)]
        data = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), numbers))
        trie = MerklePatriciaTrie(storage, secure=True)

        for kv in data:
            trie.update(kv, kv * 2)

        keys = [[str(i).encode(), str(i + 1).encode()] for i in range(101, 201)]

        proofs = [trie.get_proof_of_exclusion(d[0]) for d in keys]  

        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            for j in range(len(expected[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected.')
    
    def test_valid(self):
        """Test if the validation function."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for k, v in data:
            trie.update(k, v)

        # Get the proofs and validate
        keys = [[str(i).encode(), str(i + 1).encode()] for i in range(101, 201)]
        proofs = [trie.get_proof_of_exclusion(k) for k, v in keys]
        for cnt, p in enumerate(proofs):
            self.assertTrue(trie.verify_proof_of_exclusion(keys[cnt][0], p), 'Proof is not valid.')

    # Test if the proof is valid when one point is removed
    def test_verify_one_point_removed(self):
        """Test if the proof is still valid after removing one point."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for k, v in data:
            trie.update(k, v)

        # Get the proofs and validate
        proof = trie.get_proof_of_exclusion(b'wolf')
        trie.delete(data[3][0])  # Should change the root of the trie
        self.assertFalse(trie.verify_proof_of_exclusion(b'wolf', proof), 'Proof should not be valid.')

    # Test if the proof is valid when one point is added
    def test_verify_one_point_added(self):
        """Test if the proof is still valid after adding one point."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for k, v in data:
            trie.update(k, v)

        # Get the proofs and validate
        proof = trie.get_proof_of_exclusion(b'wolf')
        trie.update(b'testing', b'testing')  # Should change the root of the trie
        self.assertEqual(trie.verify_proof_of_exclusion(b'wolf', proof), False, 'Proof should not be valid.')

    # Test if the proof is valid when one char is removed
    def test_verify_one_char_removed(self):
        """Test if the proof is still valid after removing one char from the proof."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Get the proofs and validate
        proof = trie.get_proof_of_exclusion(b'wolf')
        for i in range(len(proof)):
            proof[i] = proof[i][:-1]

        self.assertFalse(trie.verify_proof_of_exclusion(b'wolf', proof))

    # Test if the proof is valid when one char is added
    def test_verify_one_char_added(self):
        """Test if the proof is still valid after adding one char from the proof."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Get the proofs and validate
        proof = trie.get_proof_of_exclusion(b'wolf')
        for i in range(len(proof)):
            proof[i] += b'o'

        self.assertFalse(trie.verify_proof_of_exclusion(b'wolf', proof))