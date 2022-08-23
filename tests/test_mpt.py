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


class Test_proof_of_inclusion(unittest.TestCase):
    """Test the proof functions of the MPT."""
    files = {'lots_of_proofs': 'tests/test_proofs/mpt_lots_of_proofs.pkl',
             'proof_valid': 'tests/test_proofs/proof_valid.pkl',}

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
        expected = [b'\xe8\xa1 Ay\x11\x02\x99\x9c3\x9c\x84H\x80\xb29PpL\xc4:\xa8@\xf3s\x9e6S#\xcd\xa4\xdf\xa8\x9ez\x85puppy'] 
        self.assertEqual(proof[0], expected[0], 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)

        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Generate a proof for each key
        proofs = [trie.get_proof_of_inclusion(kv[0]) for kv in data]
        expected = [[b'\xf8\x91\x80\x80\x80\x80\xa0d\x01R.l"\xd1\xf0\xb3\nf"\x9b\xdb\xba\xe1\x85\xe3\x88\xef\xe1\xde=\xac\xc2\x18/\x0f\x7f\xe5P\xd1\x80\x80\x80\x80\x80\xa0\xa4\xa8\xc2\x17\xa8\xf9\x01~\xa2\xa5\x02Y\x8b\x0b\xc2_\xc5\x93$\x12\xc7\x92j\x07\x03\xbc{##\x1c\x15%\x80\xa0\xdat7h92kXG_\x96D\xe2[\xa6\xa5\x9d\x16\xc5\x12\x02h\xec\x0f\xa0\xdbX\xd8y\x80\x04\x85\x80\x80\xa0\xb7! \xa1\xa0Y\xb4\t5/]\x17\xca\x80\xc0\x8b\xa7QD\xb05\xec\xff\xec\x93A4\x10\xd4\x18\xdd\xa1\x80', b"\xe6\xa02]\xd17'n\xcc\xd5\x04\x8f\x80\x8e\xc1\xa5Q\x02\xf9\xcd\xe0\xdc\x9fG\xbe3\xbc\x0c)\xfa3\x1ax\x9d\x84verb"], 
                    [b'\xf8\x91\x80\x80\x80\x80\xa0d\x01R.l"\xd1\xf0\xb3\nf"\x9b\xdb\xba\xe1\x85\xe3\x88\xef\xe1\xde=\xac\xc2\x18/\x0f\x7f\xe5P\xd1\x80\x80\x80\x80\x80\xa0\xa4\xa8\xc2\x17\xa8\xf9\x01~\xa2\xa5\x02Y\x8b\x0b\xc2_\xc5\x93$\x12\xc7\x92j\x07\x03\xbc{##\x1c\x15%\x80\xa0\xdat7h92kXG_\x96D\xe2[\xa6\xa5\x9d\x16\xc5\x12\x02h\xec\x0f\xa0\xdbX\xd8y\x80\x04\x85\x80\x80\xa0\xb7! \xa1\xa0Y\xb4\t5/]\x17\xca\x80\xc0\x8b\xa7QD\xb05\xec\xff\xec\x93A4\x10\xd4\x18\xdd\xa1\x80', b'\xe7\xa01y\x11\x02\x99\x9c3\x9c\x84H\x80\xb29PpL\xc4:\xa8@\xf3s\x9e6S#\xcd\xa4\xdf\xa8\x9ez\x85puppy'], 
                    [b'\xf8\x91\x80\x80\x80\x80\xa0d\x01R.l"\xd1\xf0\xb3\nf"\x9b\xdb\xba\xe1\x85\xe3\x88\xef\xe1\xde=\xac\xc2\x18/\x0f\x7f\xe5P\xd1\x80\x80\x80\x80\x80\xa0\xa4\xa8\xc2\x17\xa8\xf9\x01~\xa2\xa5\x02Y\x8b\x0b\xc2_\xc5\x93$\x12\xc7\x92j\x07\x03\xbc{##\x1c\x15%\x80\xa0\xdat7h92kXG_\x96D\xe2[\xa6\xa5\x9d\x16\xc5\x12\x02h\xec\x0f\xa0\xdbX\xd8y\x80\x04\x85\x80\x80\xa0\xb7! \xa1\xa0Y\xb4\t5/]\x17\xca\x80\xc0\x8b\xa7QD\xb05\xec\xff\xec\x93A4\x10\xd4\x18\xdd\xa1\x80', b'\xe6\xa09J\xdc\xdd9\xeb\x15k`vbd\xff\x00\x05\x8bN\xd5@\xa4\x1f\xcd\x1e?\x0e\xf43(X\x85\xf76\x84coin'], 
                    [b'\xf8\x91\x80\x80\x80\x80\xa0d\x01R.l"\xd1\xf0\xb3\nf"\x9b\xdb\xba\xe1\x85\xe3\x88\xef\xe1\xde=\xac\xc2\x18/\x0f\x7f\xe5P\xd1\x80\x80\x80\x80\x80\xa0\xa4\xa8\xc2\x17\xa8\xf9\x01~\xa2\xa5\x02Y\x8b\x0b\xc2_\xc5\x93$\x12\xc7\x92j\x07\x03\xbc{##\x1c\x15%\x80\xa0\xdat7h92kXG_\x96D\xe2[\xa6\xa5\x9d\x16\xc5\x12\x02h\xec\x0f\xa0\xdbX\xd8y\x80\x04\x85\x80\x80\xa0\xb7! \xa1\xa0Y\xb4\t5/]\x17\xca\x80\xc0\x8b\xa7QD\xb05\xec\xff\xec\x93A4\x10\xd4\x18\xdd\xa1\x80', b"\xea\xa08\x7fe\xff?'\x1b\xf5\xdc\x86CHOf\xb2\x00\x10\x9c\xaf\xfeK\xf9\x8cL\xb3\x93\xdc5t\x0b(\xc0\x88stallion"]]
        for i in range(len(proofs)):
            for j in range(len(expected[i])):
                self.assertEqual(proofs[i][j], expected[i][j], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        numbers = [i for i in range(100)]
        data = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), numbers))
        trie = MerklePatriciaTrie(storage)

        # Put the keys in the trie
        for kv in data:
            trie.update(kv, kv * 2)

        proofs = [trie.get_proof_of_inclusion(kv) for kv in data]

        # Load the proof file
        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
    def test_valid(self):
        """Test if the validation function will validate the self generated hash."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Load the proof file
        with open(self.files['lots_of_proofs'], 'rb') as f:
            expected = pickle.load(f)

        # Get the proofs and validate
        for cnt, p in enumerate(expected):
            self.assertTrue(trie.verify_proof_of_inclusion(data[cnt][0], expected[cnt]), 'Proof is not valid.')

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
        self.assertEqual(trie.verify_proof_of_inclusion(data[2][0], proof[:-1]), False, 'Proof should not be valid.')

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
        proof = trie.get_proof_of_inclusion(data[2][0]) + b'0'
        self.assertEqual(trie.verify_proof_of_inclusion(data[2][0], proof), False, 'Proof should not be valid.')


class Test_proof_of_exclusion(unittest.TestCase):
    """Test the proof functions of the MMPT."""

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
        expected = [b'\xe7\xa1 \n$\xb3io\xc1\xb4H\x15\xc86\xb1\xf5\x03\xc9\x06q\x14"w\x1b&\xbc\xcbM\xb6\xdd1_u\x9b.\x84null']
        
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

        # Generate a proof for each key
        proofs = [trie.get_proof_of_exclusion(k) for k, v in keys]
        expected = [b'\xc7\x84\xba\x7fP\xc5\xfa\xdfX\xffL\x8c\xf2#M\xc1\xb9\x8ee\r\x842\xd3\xf7JH\xd7\xe5\x02\xa0G\x1c', 
                    b'\xf8\xdeT_)%[\xbe%\xae&<\x83{\xbe\x0b\xbf\x8b\x15\xc5\xff\x07&>=Y}\xd7\x96X\xed8', 
                    b'M\x98\xca\xb2\xfc+\x8b\xc7\xa0a\xa7\x07\x97\x84\xb8<\xf3\xf35g\xd95t]\xf3\x01\xcb\x9e\xa7\x87\x9e\xdc', 
                    b'\xef\x98F9Y010\x92\xe6\x0c\xfd\xe4X\xf9\xca\xeaF\xb9\xcc0\xa6\x1a\x8c\xeb|d\xdc\xe2\xc8\x92\x18']

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

        expected = [b'\x04\xafWc%\xb2\xb6\x0bz\xb7\xfe\x0fI\x1b"{\x97\x15\x8e\xca\x9b\x81u\xde52\x02\x82\x10\xfea\x8c', 
                    b'Ag\xd2\xbdo8Ef\xdf\xec[<N\xd71\x06\x8a\x11iu:\xc4\x11\x0f\xe8\x8d!)\xf1Z\xba\x07', 
                    b'\x99yt\xac\xa9\x86\x15D,\xcf\xce]\x95\x10\xb2\xf5{U\x9fu\x16\xdd\x16\x9fK4X\xfe\xb4o\xef-', 
                    b"'c\xbfT\xfe\x9c\xa0x\xb9\x9a7\xbf\x8e\x0c\x0f3\x99)\xa06\xf5\x18H\x01\x03mg\x85\x08o\x1cO", 
                    b'\xe4\x91\x813\x90\x85M\xbc\xc2)\xe2\xc7I\xaf\xd0&[\xc5\xfb\xc2@\x8aq\xf3d\xed\x03\xf35\xf3R\xb7', 
                    b'\xa9\x0c\x1b>\xc1\x8a\x00&}p\xe1\xe8\xfa\x92\xe6\xe5\x88\xad\xf42\xdcF\x9c\xd0\xc6\xb4\xaf\xaa\xef\xd62\xa0', 
                    b'\x94\xcf\xbdQa\xef\xf1\xe2<\xba\x00\x7f^\xdf\xd5\xb8\xd7WD.\xf5d]\x0c\x95\xae\x99\x06\x99\x82\x0b\xb2', 
                    b'\x18l\x92\xcf"\xbaa\xadH\xfb\x82U\x86\x14_Z\xa7h\xae\xe0\x8b\x0b^\x0c]\x12\xa0\x00\xe6\xb7\x85\xa9', 
                    b'k\xdb}\xc7\x98\x8b\xc3\xf2\x82WN\xe7$\x9fY\x9b\xa0\xfa^\x13w7\xf2\xfe\x11\xa4\xa1\x11\x08,\x81\xce', 
                    b'\xdd\n\x17\x00\x14\x06\xea3\xd2\xe4\xe2\xcd\x91c\xae\xdb\x15\x88\x9d\xcc*\x03#0\x0e\xa6/6\x8dp\x00\x9a', 
                    b'.\\\xcd\r2\x9b\x88l\x8467p["I\x1a\xdb\x03\x044\xbc\x92$\xac1\xec\x1ae\xb6\xceJ\xd7', 
                    b'\x1b\xa8\x06\x16\x850\xef\xccL\x0c\x9fkV\xc3\x95}\xce\x8ebWf\xfb\xd8\xcc8\x96z \xeda9\x8b', 
                    b'\x01\x8f\xc5\xa70\xea.\x87\xcc\x01N\xf3d\xf24T\xd5\t\x00\x08p\xda\xbe1\xe4Z{\xfb\xd0\xcb\x89\x1b', 
                    b'\xa3\x1cfhe>\x97e\x06d%\xee`\x84\xaa\x02\tS\x8c\x05A;\xd7\xec&v\xca\xb2\xbb\xb1A\x12', 
                    b'KB\xed\x9c:z\x8e_@\xf0\x04\x90\xaa\xb0\xa5\x81\xb50\x15\xd2(ey\xd4\x95\x83O?\xf5Y32', 
                    b'\xf2D\xd4\xbb)\x90\xde\xd9\xe8\x916\xf5\xf7\xb5\x8am$\x82\xbe\x8aI+\xcb"OYk\x17\xa2\xad#\x99', 
                    b'A\xf3\xa0\xf7\xc60\xdc\xd5EQh\x8a?\xba\x16`\xa7X\xaa\xc2\x80\xe8\xe7X\x88<J\x9b\xd5IM\xe0', 
                    b'\x12\x8a\xb9\xa1\xf3\x88b\xaf+8N\x84\\\xba\x10`\xfe\xb0\xdb4\xc19$\x10\x03GCI\xcc\xeeH}', 
                    b'\x14\x00D\x10G\xb2b4\xa4\x99\x17\xdf\xc3|j\xa9\xe3"4\xf9"\x14\x03\x11\x91\xce\xbb\x9b\x80A :', 
                    b'Q\xb6(\xc1v\xca\x88\xcd\x19O\x0cl\xbc\x85\xe4tA\xd2\x83\xbbqPLx8Dqe4\xe3\xdf\xae', 
                    b'\x9b\xbd\x95\xbe\r?W\xf9\x0e\x0c\x93\xf5\xcfAh\xf4\xb4(\xbb:\xbb\xb9\x9b\xb7H\xb6\x80\xd46\x91\xa16', 
                    b'\xb2\x18D\x1f\x84\xd5\x91\xb0\xc2L\x84\x1b?\x1d<s\xb2\x88&\xe4\x97\xd9\xdb\xd5SU\xa3\xc8\xa1\xae\xba_', 
                    b'\t\x1d\xec\xf2]@\xce\xcdSYo\x8dg\x81\xaf\xfd\xec$\xb3\x15\x9e\x80\xa6\x1f\xf0k\xaf\xa2\xad\xd7\r;', 
                    b"+K,'\xe0\xb9\xbaF\x1ba\r\xd0,F\x8c\xa7\x9f\x86&0\xe8*]!\xd4S\xa5\xaa\x88r\x8d\\", 
                    b'\xae\xbb5Dv@\x89\xc7\xc3d0\xf5W\xccm\x83\xf5\x03sg\x8cj|\xe4Q\x9c*\xeb\xc2\x8b\xd5\xc8', 
                    b'\xe1\xb1\xfa\xe9\xeb\x1c\xadW\x16\\\xc2\xd9Q\x9f\xc9\x06\x89B|\x85_60\xfa\xc9\xf7\xfc\x87\x0c%)B', 
                    b'`\x1d\x7fj\xfcJ\xc0<\xd4\xe6R\x96\x0b \x16z\xbd\x1b/b\xbb\x1do\xd1\x07\x17\xd8#\xb4\xa2\x17\xd8', 
                    b"\x13\xaa\xc8\xdc\x18Z\xcc\x00\x8a\xc0s\x9b\xd4%\x96K\x8e(\xdc\xf1'\xc1W\xfb\xdfA,\r\xf9\x87\x07\xdd", 
                    b"\x95$\x89\x9b\xc8z\xba\xf2n\x89\x95\x15G\x11m\xb9\xc0\xa2\xe1\xec\xa0\xc6rb[\xec\xbcC\xbf\xe2'u", 
                    b"B\xce\x16\xec\x13#A\x037\xde\x1dr\x86\x83\r\x7f\xc2N'9\x12z\xb8\x82Zz\xe6\xe7\x9e\x97m\xe3", 
                    b'\x92k\x97s\x8cJ\xa0\xecb\xc1\xf5\xc0\xcev\xb6\x95\x16\xb0\xba\xcf\xee\xa2&:8\x99\x1a\x06d\xf9\xad"', 
                    b'\xa5\xb3(\xe8\xe1]a+\x00\xd0\x88-)[\xae\xf4\x08\x08S!u\xe0*[\x7fH\xec\xde\x1fyo\xb5', 
                    b'\xa4\x95i\xa4o;E\x99\x0eT\xf38j\xf8\xfe\xdb\xf3\x03\xc6\r\xc1\xa5\x1bg\xf4\x0f\xbb%[*\xe28', 
                    b'\x82g\xa5\x94S\xeb\xb5\xdb,\xea\xc5\x98\xeay\x8b\x80\xdd\xe2\xb2\xd6\x1f\xf0\x18\xb9\xf0\xa2l\xaf\xe7\xf9;\xbc', 
                    b'\x9b\xef"\x8a\x95&yq\x86\\\xceaG\x95\xe4\x0e\x84\xb8\xe1\x9e\x05j\x91\x88y\xfc\x94^\x13\x88\x02\xe1', 
                    b'\x11\x90\x94S\xf4\xf2MEii\xd7\xe7"\n}\x03\xfa\xe1[)\xd0\xd0-C\xf2\xa2V7\xb0@\xd3\x95', 
                    b'H. !/\x11c\xccd&d\xe6M`+<<\xa6\x0b\x89\x8a\xf1\xce1S\x16\x18nPe\xd2\xde', 
                    b'\xaf\x10\xd3\x99\x1c\xb7w\xca\xbd\xc5Bi\x92c\x18tY\x036,\x90\xab\\_\xe7\x8a\xc7&\xa9\x07\xbb|', 
                    b'\xfb\xa4\xe3\xafl7|\xc3Flg\xc9\xa7\xe7Eh\xf5\x08\xd6\x81\x08{\x88\xdd\x96\xfc\xb1K\x97\x85U\xd4', 
                    b'\xd9 m\xfa\xa2+\nl\x18O\x1dgo\xb7\x14)1\x0ceJ\xd3\xd5#\x19oVb/\x0f^\xde\xdb', 
                    b'\x97\xac\xb5w+\x83\x90&k*j\xfa.\xc6\xc9#\x0c\xa4l\xa3\x0c\xca\x01\x18\x8a\x7f\x8bBU\x1e8\x17', 
                    b"XF\x11\x84\xd6\xe3\xa9.\xd5\xdc\xa9']C\xc7Y\xaa/y\x12-\xf3\xb7\xb4\xcee\x84\xb5)\xcb)\xbf", 
                    b'\x06\xfa7\xd7\x95F\xb91:\xf6\xa6&N\xc0\xcau\x95\xe7\x03\x03N8\xa4\xb3\x97\xb8\xe8\xd8\xfd\xb9\x1d\xb7', 
                    b'\x87M\xca\xc94\xa9\xae\xd1\x8c\x18\x897>\x90\xfc\xef\x04U\x0f\x01\x9d\x9b\x08\xee\x9d\xf5:\x00e\xee\x85\xce', 
                    b'\x04\x86\xbb\xc5Aj}\xaa9\xc1\xa5C7B\xfe\xa6\xfb{\xbd%\x81\xf9\xb4\xb2\xc4\x1e\x95\xff\xd4\x7f*\x8c', 
                    b'\xeb\x91\x8c}\xc3X\xc8\x1cZg\xee\xe5@\x0e\xfbN0m\xe4\x166\xcb^d\xd9%\x0c\x14\x12\xf7~\xb2', 
                    b'\xe7\xdf\xee\x00\xb9#\xcb\xe0\x8b\xbe\x9eg%s\xad(!J\nT7)\xda\xe9^\x08\xb5\t\xc0\r\xbe\x81', 
                    b'\xb5}\xb1\x9a%\xdf\xfb\xb5%\xd9Q\xbb\xb2:>\xc0\x11<\xd47W;\xc5s\xednI\xe3\xe5\xe2\xeap', 
                    b"5,\x13'ag\x9f{\xae\x1a/\x1d\x15\xae\x8d\xb8y\xc6A\x19Xr\x81\xdc\xacJ\xd5%\xb0#7$", 
                    b'|\xfe\xed\xceoO\xdb\xc6b\xa0"\x12X\x1d\xcb\xfeF\xd7\x16\x00\x1b&pQ!X\n\xdb\xdePm\xb1', 
                    b'\xb6\xcc\xbbB\x8c\xb2\xe4\x02\xc6:!\xda$\xf9\x9a\xe5\xc4\x9620\x89\x81\xcet\xbf\x045\xe5e\x06Z\xeb', 
                    b'd\xf7\xc4\x1a\x92\xcdm\xa2\xae\xf5p\xf4\xcb)\x97\xceGZ-\x82C\x0e\xa1z\xbe\xcf\x1ad\xe2*08', 
                    b'+o\x8e\xf1\xb6Yb\xe61;\xfc\x07\x0f\xd8\xc4\xd9\x18\xa2\xd5\x99*\xfb\xbd\x90\xeaO\x19\\\xd781\x19', 
                    b'}\xf6\xffY\xe6\xf4&\x91\xe0\x05s\x82\x18\x0f\xfd\x83\xef&\xfd\xfdVX\xf6\xd2\x87g\xd0[L\xd2_\xce', 
                    b's\xb7}\xc4\x98\xa8\x14\xe4\xaeG\xbd\xcf\xdfW\n\xbd/\x12z\xa5+\x97\xc7\xbd\x8c\xc3\x8fL\xefy\x99\xdf', 
                    b')T!E\xd4\xb3\xb4\\J\x89\xb3^\x98\xbdm\xe2\xa1\xa3\xcfP\x9d\xa8\xa10#\x8c\x88\x8e\xcc\xbc\t\x10', 
                    b"\xd9\xdd\x7f\xe7Q\xf1\xbeg\x98.\x86I\n\x91\xf2\xac\x14\xf4\x91a\xca\x83'\x1d\x04\xf5M\x1e\xf8\x84\xb7*", 
                    b'I\xd6s\xd7\xf9\x12\xfb\x8a\xd2G\xb0q\xa1\xba=\xb1\xe0\x90\x848z\xaf^\x87_6m^NNf\xf1', 
                    b'7\xce\x19\xdc\xff-uBZR\xcep\\\xf5M\xcb\xfa\x82\x0c\x87\x0f\xa7\xbdM\xb7\x9f\x1c+p\xad]\x9d', 
                    b'~S\x96\xcf\xc8(\xdco\xce\x97\x8b\xc8\x18&\xac\xb7\xd4CQ\xd2M\xa5#\xa4\xe7D\n\xf6\xe7*@\xf3', 
                    b'\x85\xfc\xc8\x08\xee\xd5P\xfbJrq\xd7KL\xf2n\xbd\x94\xa3[\xa0\xc2\xffZ\x10#c\x04\x1f\xe8x\x1a', 
                    b'\xa6)H\xc0\xac%\x9b\xb0\xc2\xdaL2\xfd\x17\xec\xb2\x16\xdbK\x01pe\x035\xf6\x1f\xe2\x92\xbb]f\xe8', 
                    b'\\\x8d\xe8\x1b.\xc8\xe7\x03\x9e\xc5wuV\xd1y\xd2\x91L\xec\x9b\xf3\xf3\x18Nr\xce\x193\r \xd3\xd7', 
                    b'\xa8Q\x1a \xab\xfa\x82\xe0\xfb;L/\xf3\x15T<\x98\xcd \xf1Y\xf4\xa8\xed\xa6\xf5L`\\A\x8f\xd5', 
                    b'\x97\xc31q\xcf\x12\x7f+q\x8a\x88F\xea\x90\x9d\x02\x1e\xf8\x1f\xd4\x14\xc43\x9aG\xabOT1\x8f\xb4&', 
                    b'"\xbf\xe2\xa1\x02\xd6;\x87\xac\xf0\xc0\x14\x9fK+Hm\'\xf6\xc6\x8f\xc9gb\x8c\xbb%JL\xdbqF', 
                    b'z\x98/\xe0\x9fw\xdd:\xb4\xf8\xc4=\xe9HuQ\xe4\xa1oe\xdfq\xe7#\xbb\xec\x0e^\x8d\xce\xea\xf1', 
                    b'\xf34/\xfe\x87\xbc\r\xce\xfd\x9chk\x90\x8d\xf2\xf0\x83\x18\t\x1c\xdd\xbf\x18\xcf\xb0\xe4\x1dQ"\xc10Z', 
                    b'\xbd\xca\x80\x98\xd6\x83\x94o\xd2\xf8P7\x84k{\xa9K\xden1\xd7D\x9ae\x8b\xf6\xde\xf8^[7\x19', 
                    b'7\x86\xea\xd7\x9e\x90\x18)U\x83\x01\xe1J\\\xde\xfc\x97\\2\xfd\xcc[\xce\xa2S\xd1\xe9q\xd1`\xde(', 
                    b'\xd6|o\xcb6\xa5\xb3 \x91\xf1\xcd\xb1+\xd9\xcc\x0bQ\xd8W\xa8\xb0E[o5\xb3eF\xc0V0\xb9', 
                    b'\xaf\x87\xde,_\x8a\xff\nqr\x97e\xb6\xb64\xc1u\xa2\xe7c\xea;@\xa02\x80\xc5Y\x82\x15\xb6\x1d', 
                    b"\x10\xb8\xe0=\xbe-*\xbc+A,Z\xaf\xad\xccQ'5\xce\n0\xd4<\x90\xec\x01(\xa2\t*\x17\xa9", 
                    b'5\x1b9\x04\xceK\x1b>\x00E\xfd6\x84\xce`<\xd0\xeft\xa9W}cyzv\x1e)\x13\x91;\x8d', 
                    b'\xbf\x02\x9a:2\xaf\x93\x8d/\xb6z\x8c\x00\xe17S\x10~+\xf7\x9a\x87\x9f\xb0\x98~V\x1b\x98\xe3S2', 
                    b'\x95\xcf\xe5X\x06L\x91\xf2\xfe\xbc\xbb\xb8\x9a\xad\xa3\x8b>\x8d11Lv\xe0w=\r\xd6\xb0\x9a\xa6\xab\xed', 
                    b'x\x8a\xb9\xf2\x1b\xc0L}\x98\xba\x9d\xb3\x16\x0b\x03>\x0c\xc4Y/\n\x06\x9f2\xe3p\xcfj\xd4\x15\x9bI', 
                    b'\xed\xd4b\xa7K\x94eS\x89\x1b.ws\x1d\xea\xa1\xf7\xa4\x15\xbd\xc7@\x8f\xa9\xd5\x9f\xb4\x8e\xbc\xfe\xa4\xee', 
                    b'\x0c\xd1\\\xdb\x93\xcb\xad~C\xe5\x12\xbb\xa2\xcc\x7f\x94\x1c\x17\x170rP\x08w\xdbi\x00\x12\x12\xbd\xc6\xa0', 
                    b'{\xa1\xdc\xc0\xe7\x8e\x957ow\xcf\x96\xcdWu\xf2\xdeZ\xf7\x85\xac:R }\xe5\xdc\xe4b\x08\xf8\xd2', 
                    b't\x1e\xb2\xf5[\xe96\x82{\xd7\x0e\xc4\x99\xd8\xd8\xef\xf4\xda\xc6\xd8G\xebj\x9a\x01\xf0\x157\xf74\x1aj', 
                    b'\xbe\x02M\xa7&\x18d\x95\x8b\x9d\xb7\x19\xb2^.\x14MN["\xab\x1d\x99\xb6\xe1\x1dG\x99C^\xa4\xf8', 
                    b'-\xcb\x94|Ti\xa1\xfb\xf4\x88\x87\xc1iz&\x84oLn\x973\x0cK\x1d\x9a\xc3P\xb5ZQM\xfe', 
                    b'\xe4\xdbu\xb9\x84\x1d\xf8\xdf\xcc\x86\x84\x9e\x9c\n\xdd\xfb\x1a\xf3\x8d\xcep\x18\x8e\xd4\x05\xf8\x1c}\xe5-\xa6\x8f', 
                    b'\x17\xf5\x90\x9c\xff\xaf\xd4{\x91\x94\xce\xf3\x95?\x1b\x00e\xff\xbd\xc2\xf6bYiAH\x92\xd9\xf6HAf', 
                    b'\x0c`>\xf68\x8d\x0e\xb4jT#\x97Y\xc5\x9a\x87\x16"\xeb\xf4Mv-\x88\x01\xd9\xf6\xd9\x9bi\xe4d', 
                    b'\xcai\xceB\xfe\x96dU!\x81\xc7^[\x19\x11%\x7fA2\xbe\xf2\tG\x13DD\xce\x8e\x88\x83\xcc\x85', 
                    b'\xd0\x8c#\x12Q\xc6+\x8cF\xfb8\\\x86ZC\xb7\xf04!\xdb\x08\x0f\xbe\xc9\x12g\x05\x0c\xcf{k\xa6', 
                    b'\r\xe9\x14g\x90{\xc3\xff\n=\x0c\xf2\x7f\x9cZ\xdf\xbco\xb8\x01=Q\xa3\x87{!\xf3y\xa2TI\xed', 
                    b'm\x1c/T\x01g\xf0\xd7\xd1\x08_8\xe3\x8aQFe}\xe2B\x1c\xab\x8d\x8d\xfc\x1f\xa5\xd1C\xba\xf5\x91', 
                    b'\x8d\xcd$~\xe43u\xca\xa1b_~\xec7q\xbe\x84\xea\xb6 [\x04y\x8b\xa5\n\x98V\xf1\x1a_*', 
                    b'6\x11*\x1b]<\t\xfa\x94Sl\xafn?\xc5\xd0\x8f9\x84\xdf\x8eX\xe4\x91Gw\x9a\x15\x87R\x88\x8c', 
                    b'~?\xa8Ey)\xabN\xd9\x87\xc4<sR\xa5xj.\xb41W\xfc7\xdf\xab\xc6%{TP\x97E', 
                    b'\x16\xd9\x8dR!\xadQ\x7f\xd8Cx3\xfd0\xd54\x18\x90\xc0\x969\xff\xe4\xe1\tZ\x9d)\x86Gz\xf3', 
                    b'\x1c\x14V\x0b\xda\xa7)\xfe;H\xae&\xc4\x94\x91\xbaq\xae(\xeb\xe1\xb4\xd3K\xa5\xae@k1t\xec\x0b', 
                    b'7\x98\x9b\nv\xfa\xdab\xc9\xdbuL\xa92\xe1\x8f\xa8S\x7fG\x17G4\x06\xe1\xe3m"\x10,\xe3\x0f', 
                    b'\xd1\x93\x9b\x9d\xdb\x01\xd7\xed\xa4\xd3d\xcf\xc13\xad\x11\x90\xf7\xf20\xf1\xbd\x9eJ`\\\xb6\x04z\xe4\xa2\xc9', 
                    b'\x94%\xe0}\x01\xe4\xc62\xc4#\x86q6\xad\xe7%\xce\x88o\xf5\xac\xa9Fp9w\x1b\xa5\x8aPO\xdd', 
                    b'\xe4\xb5\x7f\xcc\x9cB9\xc5\xae\xb7\xd7d\xd0f\x10\x81\xed\xfc\xee\xb60@a\xb7\xf7\xd6\x91"\x9d\xf8\x98`', 
                    b'\xc32\xbc\xdf\x14\xb8CJi\x10I\xcc\x05\xb4\x8f\xa41\x85\xcb\x06\xc4q\x89\xf5\xab*\x19\xcdLK\xac\xbf']

        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
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
        trie.delete(data[3][0])
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
        trie.update(b'testing', b'testing')
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
        self.assertEqual(trie.verify_proof_of_exclusion(b'wolf', proof[:-1]), False, 'Proof should not be valid.')

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
        proof = trie.get_proof_of_exclusion(b'wolf') + b'0'
        self.assertEqual(trie.verify_proof_of_exclusion(b'wolf', proof), False, 'Proof should not be valid.')