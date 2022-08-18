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
import rlp
import unittest
import random


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

        with self.assertRaises(KeyError):
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

        trie.update(b'key', b'value')
        trie.delete(b'key')

        with self.assertRaises(KeyError):
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
        with self.assertRaises(KeyError):
            trie.get(b'dog')


class Test_proof(unittest.TestCase):
    """Test the proof functions of the MPT."""
    pass

    # Add one data item and create a proof

    # Add many data items and create a proof

    # Add lots of data items and create a proof