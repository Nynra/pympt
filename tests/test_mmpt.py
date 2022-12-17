import sys, os
#Following lines are for assigning parent directory dynamically.
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from src.mpt.mmpt import ModifiedMerklePatriciaTrie
from src.mpt.node import Node
from src.mpt.exceptions import PoeError
from src.mpt.hash import keccak_hash
from src.mpt.proof import Proof
import rlp
from rlp.exceptions import DecodingError
import unittest
import pickle


class Test_proof(unittest.TestCase):
    """Test the proof class.""" 

    def test_change_attributes(self):
        """Test if the proof hash is correct."""
        proof = Proof(b'1', b'2', b'3', b'4')

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

        trie.update(b'dog', b'dog')
        proof = trie.get_proof_of_inclusion(b'dog')
        self.assertEqual(proof.trie_root, trie.root(), 
                        'The root hash in the proof does not mathc the trie root.')
    
    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'dog', b'puppy')
        proof = trie.get_proof_of_inclusion(b'dog')
        
        with open(self.files['one_proof'], 'rb') as f:
            expected = pickle.load(f)

        # Compare all the attributes of the proof
        self.assertEqual(proof.trie_root, expected.trie_root, 'Root hash does not match expected.')
        self.assertEqual(proof.target, expected.target, 'Target does not match expected.')
        self.assertEqual(proof.proof, expected.proof, 'Proof does not match expected.')
        
    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Generate a proof for each key
        proofs = [trie.get_proof_of_inclusion(kv) for kv in data]
        with open(self.files['many_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            # Compare all the attributes of the proof
            self.assertEqual(proofs[i].trie_root, expected[i].trie_root, 'Root hash does not match expected.')
            self.assertEqual(proofs[i].target, expected[i].target, 'Target does not match expected.')
            self.assertEqual(proofs[i].proof, expected[i].proof, 'Proof does not match expected.')

    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [str(i).encode() for i in range(100)]
        for kv in data:
            trie.update(kv, kv)

        proofs = [trie.get_proof_of_inclusion(kv) for kv in data]

        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            # Compare all the attributes of the proof
            self.assertEqual(proofs[i].trie_root, expected[i].trie_root, 'Root hash does not match expected.')
            self.assertEqual(proofs[i].target, expected[i].target, 'Target does not match expected.')
            self.assertEqual(proofs[i].proof, expected[i].proof, 'Proof does not match expected.')

    def test_valid(self):
        """Test if the validation function wokrs."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Get the proofs and validate
        for i in range(len(data)):
            proof = trie.get_proof_of_inclusion(data[i])
            self.assertTrue(trie.verify_proof_of_inclusion(proof), 
                    'Proof for {} is not valid.'.format(data[i]))

    def test_verify_one_item_removed(self):
        """Test if the proof is still valid after removing one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(b'doge')
        trie.delete(b'do')
        self.assertFalse(trie.verify_proof_of_inclusion(proof))

    def test_verify_one_point_added(self):
        """Test if the proof is still valid after adding one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(data[2])
        trie.update(b'testing', b'testing')
        self.assertFalse(trie.verify_proof_of_inclusion(proof) )

    def test_verify_one_char_removed(self):
        """Test if the proof is still valid after removing one char from the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_inclusion(data[2])
        proof = Proof(target_key_hash=og_proof.target, proof_hash=og_proof.proof[:-1],
                    root_hash=og_proof.trie_root, type=og_proof.type)
        self.assertFalse(trie.verify_proof_of_inclusion(proof), 
                        'Proof should not be valid.')

    def test_verify_one_char_added(self):
        """Test if the proof is still valid after adding one char to the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_inclusion(data[2])
        proof = []
        for i in range(len(og_proof.proof)):
            proof.append(og_proof.proof[i] + b'o')
        proof = Proof(target_key_hash=og_proof.target, proof_hash=proof,
                    root_hash=og_proof.trie_root, type=og_proof.type)

        self.assertFalse(trie.verify_proof_of_inclusion(proof))


class Test_proof_of_exclusion(unittest.TestCase):
    """Test the proof functions of the MMPT."""
    files = {'one_proof': 'tests/test_proofs/mmpt_one_poe.pkl',
             'many_proofs': 'tests/test_proofs/mmpt_many_poe.pkl',
             'lots_of_proofs': 'tests/test_proofs/mmpt_lots_of_poe.pkl'}     

    def test_proof_on_empty_trie(self):
        """Test getting the proof of an empty trie."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        with self.assertRaises(ValueError):
            trie.get_proof_of_exclusion(b'wolf')

    def test_root_hash(self):
        """Test if the root hash of the trie is correct."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'dog', b'dog')
        proof = trie.get_proof_of_exclusion(b'wolf')
        self.assertEqual(proof.trie_root, trie.root_hash(), 
                        'The root hash in the proof does not mathc the trie root.')

    def test_proof_on_existing_key(self):
        """Test getting the proof of an existing key."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        with self.assertRaises(PoeError):
            _ = trie.get_proof_of_exclusion(b'doge')

    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'dog', b'doge')
        proof = trie.get_proof_of_exclusion(b'wolf')
        
        with open(self.files['one_proof'], 'rb') as f:
            expected = pickle.load(f)

        # Compare all the attributes of the proof
        self.assertEqual(proof.trie_root, expected.trie_root, 'Root hash does not match expected.')
        self.assertEqual(proof.target, expected.target, 'Target does not match expected.')
        self.assertEqual(proof.proof, expected.proof, 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Generate some non existing keys
        keys = [str(i).encode() for i in range(4)]

        # Load the expected proofs
        proofs = [trie.get_proof_of_exclusion(kv) for kv in keys]
        with open(self.files['many_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            # Compare all the attributes of the proof
            self.assertEqual(proofs[i].trie_root, expected[i].trie_root, 'Root hash does not match expected.')
            self.assertEqual(proofs[i].target, expected[i].target, 'Target does not match expected.')
            self.assertEqual(proofs[i].proof, expected[i].proof, 'Proof does not match expected.')

    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [str(i).encode() for i in range(100)]
        for d in data:
            trie.update(d, d)

        # Generate the proof for eacht item
        keys = [str(d).encode() for d in range(101, 201)]

        proofs = []
        for d in keys:
            proofs.append(trie.get_proof_of_exclusion(d))

        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            # Compare all the attributes of the proof
            self.assertEqual(proofs[i].trie_root, expected[i].trie_root, 'Root hash does not match expected.')
            self.assertEqual(proofs[i].target, expected[i].target, 'Target does not match expected.')
            self.assertEqual(proofs[i].proof, expected[i].proof, 'Proof does not match expected.')

    def test_valid(self):
        """Test if the validation function wokrs."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Generate the proof for eacht item
        keys = [b'wolf', b'giraffe', b'tiger', b'lion']

        # Get the proofs and validate
        for i in range(len(keys)):
            proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(keys[i])))
            self.assertTrue(trie.verify_proof_of_exclusion(proof), 
                    'Proof for {} is not valid.'.format(keys[i]))

    def test_verify_one_item_removed(self):
        """Test if the proof is still valid after removing one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Generate the proof for eacht item
        keys = [b'wolf', b'giraffe', b'tiger', b'lion']
        proofs = [trie.get_proof_of_exclusion(keccak_hash(rlp.encode(k))) for k in keys]
        trie.delete(b'do')
        for proof in proofs:
            self.assertFalse(trie.verify_proof_of_exclusion(proof)) 

    def test_verify_one_point_added(self):
        """Test if the proof is still valid after adding one point."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Generate the proof for eacht item
        keys = [b'wolf', b'giraffe', b'tiger', b'lion']
        proofs = [trie.get_proof_of_exclusion(k) for k in keys]
        trie.update(b'bear', b'bear')
        for proof in proofs:
            self.assertFalse(trie.verify_proof_of_exclusion(proof)) 

    def test_verify_one_char_removed(self):
        """Test if the proof is still valid after removing one char from the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        proof = []
        for i in range(len(og_proof.proof)):
            proof.append(og_proof.proof[i][:-1])

        proof = Proof(target_key_hash=og_proof.target, proof_hash=proof,
                    root_hash=og_proof.trie_root, type=og_proof.type)
        self.assertFalse(trie.verify_proof_of_exclusion(proof))

    def test_verify_one_char_added(self):
        """Test if the proof is still valid after adding one char to the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Get the proofs and validate
        og_proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        proof = []
        for i in range(len(og_proof.proof)):
            proof.append(og_proof.proof[i] + b'o')
        proof = Proof(target_key_hash=og_proof.target, proof_hash=proof,
                    root_hash=og_proof.trie_root, type=og_proof.type)
        self.assertFalse(trie.verify_proof_of_exclusion(proof))


class Test_save_and_load(unittest.TestCase):
    """Test if the trie can be saved and loaded."""

    def test_save_and_load_one_value(self):
        """Test if the trie can be saved and loaded with one value."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do']
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Check if the data is still there
        for kv in data:
            self.assertEqual(trie.get(kv), kv, 'Data not found in trie.')

    def test_save_and_load_multiple_values(self):
        """Test if the trie can be saved and loaded with multiple values."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Check if the data is still there
        for kv in data:
            self.assertEqual(trie.get(kv), kv, 'Data not found in trie.')

    def test_save_and_load_lot_of_values(self):
        """Test if the trie can be saved and loaded with lot of values."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [str(i).encode() for i in range(100)]
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Check if the data is still there
        for kv in data:
            self.assertEqual(trie.get(kv), kv, 'Data not found in trie.')

    def test_save_and_load_new_item_to_copy(self):
        """Test if the roots differ when an item is only added to original."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Add new item
        new_trie.update(b'new', b'new')

        self.assertNotEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are equal but should not be.')
    
    def test_save_and_load_new_item(self):
        """Test if the roots differ when a new value is added to original and copy."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Add new item
        new_trie.update(b'new', b'new')
        trie.update(b'new', b'new')

        self.assertEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are not equal but should be.')

    def test_save_and_load_remove_item(self):
        """Test if the roots differ when an item is removed from original and copy."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Remove an item
        new_trie.delete(data[0])
        trie.delete(data[0])

        self.assertEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are not equal but should be.')

    def test_save_and_load_update_item(self):
        """Test if the roots differ when an item is updated in original and copy."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        # Update an item
        new_trie.update(b'new', b'dog')
        trie.update(b'new', b'dog')

        self.assertEqual(trie.root_hash(), new_trie.root_hash(), 'Root hashes are not equal but should be.')

    def test_proof_on_copy(self):
        """Test if the proof is correct when the original is modified."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.update(kv, kv)

        # Save the trie
        pickle_bytes = trie.to_pickle()
        new_trie = ModifiedMerklePatriciaTrie()
        new_trie.from_pickle(pickle_bytes)

        proof = trie.get_proof_of_inclusion(data[0])
        trie.update(b'new', b'dog')
        self.assertFalse(trie.verify_proof_of_inclusion(proof))
        self.assertTrue(new_trie.verify_proof_of_inclusion(proof))


if __name__ == '__main__':
    unittest.main()