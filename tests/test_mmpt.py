import sys, os
try:
    from mpt import MerklePatriciaTrie
    from mpt.node import Node
    from mpt.hash import keccak_hash
except (ImportError, ModuleNotFoundError):
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.mmpt import ModifiedMerklePatriciaTrie
    from src.mpt.node import Node
    from src.mpt.hash import keccak_hash
import rlp
import unittest
import random


class TestModifiedMerklePatriciaTrie(unittest.TestCase):
    def test_insert_get_one_short(self):
        """Test inserting one short key-value pair and then getting it."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        value = b'value'
        trie.update(value)
        gotten_value = trie.get(keccak_hash(rlp.encode(value)))

        self.assertEqual(value, gotten_value)

        with self.assertRaises(KeyError):
            trie.get(b'no_key')

    def test_insert_get_one_long(self):
        """Test inserting one long key-value pair and then getting it."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        value = b'value_0000000000000000000000000000000000000000000000000000000000000000'
        trie.update(value)
        gotten_value = trie.get(keccak_hash(rlp.encode(value)))

        self.assertEqual(value, gotten_value)

    def test_insert_get_many(self):
        """Test inserting many values and then getting them."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'verb')
        trie.update(b'puppy')
        trie.update(b'coin')
        trie.update(b'stallion')

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
            trie.update(kv)

        for kv in keys:
            self.assertEqual(trie.get(keccak_hash(rlp.encode(kv))), kv)

    def test_delete_one(self):
        """Test deleting one value and then getting it."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'key')
        trie.delete(b'key')

        with self.assertRaises(KeyError):
            trie.get(keccak_hash(rlp.encode(b'key')))

    def test_delete_many(self):
        """Test deleting many values and then getting them."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'do')
        trie.update(b'dog')
        trie.update(b'doge')
        trie.update(b'horse')

        root_hash = trie.root_hash()

        trie.update(b'a')
        trie.update(b'some_key')
        trie.update(b'dodog')

        trie.delete(b'a')
        trie.delete(b'some_key')
        trie.delete(b'dodog')

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
            trie.update(kv)

        for kv in keys:
            trie.delete(kv)

        self.assertEqual(trie.root_hash(), Node.EMPTY_HASH)

    def test_root_hash(self):
        """Test getting the root hash of a trie."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'do')
        trie.update(b'dog')
        trie.update(b'doge')
        trie.update(b'horse')

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('ac9bdffdaf45f979ab0bf7cbdcf02a3094da734b242e247764b2809cdd8d13bc'))

    def test_root_hash_after_updates(self):
        """Test getting the root hash of a trie after updates."""
        storage = {}

        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'do')
        trie.update(b'dog')
        trie.update(b'doge')
        trie.update(b'horse')

        trie.update(b'dog')
        trie.update(b'doge')
        trie.update(b'horse')

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('ac9bdffdaf45f979ab0bf7cbdcf02a3094da734b242e247764b2809cdd8d13bc'))

    def test_root_hash_after_deletes(self):
        """Test getting the root hash of a trie after deletes."""
        storage = {}

        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'do')
        trie.update(b'dog')
        trie.update(b'doge')
        trie.update(b'horse')

        trie.update(b'dodo')
        trie.update(b'hover')
        trie.update(b'capital')
        trie.update(b'a')

        trie.delete(b'dodo')
        trie.delete(b'hover')
        trie.delete(b'capital')
        trie.delete(b'a')

        root_hash = trie.root_hash()

        self.assertEqual(root_hash, bytes.fromhex('ac9bdffdaf45f979ab0bf7cbdcf02a3094da734b242e247764b2809cdd8d13bc'))

    def test_trie_from_old_root(self):
        """Test getting the root hash of a trie after deletes."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.update(b'do')
        trie.update(b'dog')

        root_hash = trie.root()

        trie.delete(b'dog')
        trie.update(b'do')

        trie_from_old = ModifiedMerklePatriciaTrie(storage, root_hash)

        # Old.
        self.assertEqual(trie_from_old.get(keccak_hash(rlp.encode(b'do'))), b'do')
        self.assertEqual(trie_from_old.get(keccak_hash(rlp.encode(b'dog'))), b'dog')

        # New.
        self.assertEqual(trie.get(keccak_hash(rlp.encode(b'do'))), b'do')
        with self.assertRaises(KeyError):
            trie.get(keccak_hash(rlp.encode(b'dog')))
