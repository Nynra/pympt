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


class Test_proof_of_inclusion(unittest.TestCase):
    """Test the proof functions of the MPT."""

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
        expected = b'\xffk\xda\xb7Mq>\xbb@\x05\xf8`J!\x08Y\x8e$\xcd\x03\x1b\xe3\xef(\x80\x98\x94WiPf\xbf'
        self.assertEqual(proof, expected, 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = MerklePatriciaTrie(storage, secure=True)

        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Generate a proof for each key
        proofs = [trie.get_proof_of_inclusion(kv[0]) for kv in data]
        expected = [b'Py\x80\x03\x00\x02\x02\x17\t\x12\xef\x0f9\xef\xce=\x8d\xa3>\xdc\x16\x80\xc8\xeb\x8b\x96\x01#\xfe\x00\xa5\xb4',
                    b'\xc3\x86\xb2O\x01\xc9\xffCmJ*\x0f\xee\xa0\x92\xac\xd9\xe6kS\x8a\x8dh\x01\x19\xd8\x01\x87\xe9F\xa1\xba',
                    b'\xf7-\x9f$\x13\xae\xfdo)"\xe6\x05\x93{\xf6\x85Y\x9f\xe7#/\xad\xc1\x1b\xcb\x85\xb3\xc8s\xc3\x05\xfb',
                    b'\x9f\xa6\xd3N\xc3b\xf2K\x94\xe8A\xdc\xb1bMq\xed$nG~s\xed#\x1ec\x9fW\xa2\xc4\x12\xd7']

        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        numbers = [i for i in range(100)]
        data = list(map(lambda x: bytes('{}'.format(x), 'utf-8'), numbers))
        trie = MerklePatriciaTrie(storage)


        for kv in data:
            trie.update(kv, kv * 2)

        proofs = [trie.get_proof_of_inclusion(kv) for kv in data]

        expected = [b'5:\xb6\xeaH\x8d\xcd\xaaR\xe1\xd2[J\x89\xdd\xe5,\x98Cs\xa4\xbe\xa35\xef\xfc<\x13\x91\x05\xd2w', 
        b'\xc3\xfdva\x91\xd8\x9cL\xbbO|\x983%\xc8\xae\x17\xda\xae\x82x\xd2\x8f#\x07\xc3%\xb2\xb8~i\x03', 
        b'Np\x8e\xa6=\xe8\xe1\xad\xf6\xc5\x8ea\xf7\r:\x98\xc9@*\x08\xc3\x1d\xfei\x8aF\x91\xd4\x0b\xe2Fw', 
        b'\xbeJ\x1d(b\\\x1e\xd9\xcd\x99\x9b\x9eN\xb8Hy\x0bx\x0eo\xde\x84\x017b\xa5\x96\x85\x87\x1f\x1b\xc6', 
        b'\xbb*\x8dP\xa2z\xcbf>\xb7y\x16C\x81\xc9\x89R\xfc\x80\xc1\xf4\xf8\xd1\x0c1/\xce\xb5\x0b\xa6\xc9\x9e', 
        b'\x01:\xd58\x95v_:\xd8\xac\xd85Lc\xe0\xf7\xf1\xe5,6\x135.\xa9\xc8\x17(\xaf\x06\x89\xb8.', 
        b'\x94\xbc\xea\xdc\xc9\x95\x0b\xe1\x9f.\xcc\xc0:v\x07O\\K2\xdb\x91\xd1\xd6\xf3o\xda\x07\x88:\xf7\x93p', 
        b'&?K\x82D\x892\x80\x1dv\xfd%\xb1\x05\xa2\xe3>\xfb\xf0\x04\x9c\x90\x96\xcf\xb8\xe8\xb9\xf7\xe0\x90\x18g', 
        b'\xea\xce\x95\xc6\xa5\xb9\xc6]\xda\xb0Y9b\xcf\xe7\xb8\x12[\x97;\x03QP\x87\xcb\x1b\x9a8\x99\xce\xdfG', 
        b',\x82\xb3\xbeB\x8b\xc0\xea\x81?\xe7\x18\xdc$\x8f\xac\xd3\xcfW!\xb7\xe5\xd1\xe2?\x1fl\xf0\x9a\xfa\xa0b', 
        b'\x92\x02[\xa3s\xcd\x0cpT\x13\x9d@_l\xf8\xb2\xd9\x9b\xd5OU\x9c\x0b\x9a:D\xc8$\x02\xc7\xf7Y', 
        b'\xab\xc5\x8f<;})L\xf3\xcf\xea\xb2\xcc\x07\xcd\x9b\xe63\x83\x9f\xd3IY\x02H\xfc\x18j\x8f\xf90&', 
        b'\x8b#\xbb \xac\x82X\xb3\x88\x91\x0e\x06y\xe5^\x04; \xf2V\xd5N\xd5\xd9\x94\xb2`\xb9\xc1\xc7\x99\x04', 
        b"mqB\xc3?70\xe2>0\xbd\x97\xb0\xa27\xeb\xc0\xc9\xa6\x1b\xe5\x90\xa3\xdc\x8d\x0c'*'<\xf6]", 
        b'V\xeb\x05\xce\x1c\xb8\x97\xbf\x9be=\xdb\xbcFu\xe1\x13!\x89h\xbap^\x1b\x97\xb6\x95\x0c\x01u\nH', 
        b'DdZ\xd7\xd1\x82\n\xc4\xf5\xd5\xf1\x88\xcb\xe3\xcc\xe1\x02L|`1\x0b\x0f\xceI|\xb3\x07\x0f#\xc7\xa7', 
        b'\xf9\xb3|\x9fv\xdb\xe9u\xfeR!\xfb\x1c_\x89\xc3\xa3q\x8c\ncT]\x08\xea\x97\x8b\xbb\x8b\xa7\xb3_', 
        b'\xa8M\xe7|\x19P|\x9d\x8d\xf7\x13ckQ\xe8\x8d\x0b^\xe5\xdeG&J9\x87\x9e\xf5\xe2F|\x8a]', 
        b'\xbd\xba\x16\x1f\r\xed\x8fQ\xe7:\xb0\x1a\xf7V\xe3G;\x87,\x1c\xdb\xffs!3\xb5\x8b \tfmv', 
        b'\x00\x84\xd4\xe3\xf9\x15\xb9X\xb6:\xb1z"\xe2\x97\xa3L\x90I\x99\xf2\xa0\xbb_h\xeal\xb7C\xe7\x80\xa1', 
        b'Fp\x11\x06\x17%Z\xd4\x00i<\x9d\x963Z\xa1_zc+\x02x\x8dC\xbf\xd1\xb0\xf6\xb5\xf9"Y', 
        b'#\r\xba\\\xcfR\xad\xd6\x05B\xb2\xbd\xd3{\xdd\xe27\xb0N\x1f\x8e7*\xfb\x0b*\x9a\x12\xfc\x06\x08\xd2', 
        b'\x12[\xae\x00f\xbb;\x87\xe2\xce\xd1\xa0:|\x08\xd5\\\xc0aFj\xaaznlA\x81O\x03\x1e\x08>', 
        b'\x8f<\xab\x00\xbf]\xbb\x15\x1d\xe4S@\xed\xbc\xc1\xb1\xc9\xa1\rk\x10\xe5\x1b\xaa\x8a\xba\x18-\x9c^\x19\x82', 
        b"\xea\xde$\xf8'\x00r\xcfv\xef\xfc\x15\xa0\xa1T%44]'t\x8f7\xb4H\x83H$\xf8\xae\xf8)", 
        b'\xe1<\xbe\x99\x8e\x8f\xd2\xd1I\x82RI\t\x108\x1c)\xc5\xedf\x82\x83U\x19\xad\xaf\xc6\xa8\x83C\xe1c', 
        b'!\x8d\xfc\x91\x98\xb7\xf4Q\xf2\xa8~eR\xd4\xd1\xa3\xc8\x9c\x16,\x87\xa8J0\xc09\xd3\xd7\xbb2n8', 
        b'\xa6\xcc\xbb\x82\x02,\x93c\x0f\x91\xc8\x04\xc5\xe5Z\x9f\x84\xba\x99\x91*\xfc\xb5\x7fZB\x0fqf-4N', 
        b'\xf0\xe0\x97r\xa8?\xae9\xe9 \x87&\xa0%\x7f\xb1\xa0\xb0Hb\\\x0cX\xace\x8c{U\x91`\x06\x02', 
        b'S\x89\xb4\x90\xff`O\x1f\xfb\x93\xc7aw\x18\xf7z\xdb\x0e\x1f\x81.+o\xe5\x85\x96\xcf_\xe58LA', 
        b'\x8a\x9aq\x94u\xffT\x84\xfb\xbc\xb0F\x91\x8fG\x12N\xc2\xc2!\x85DL\xa2:z\x19\xd6\xc1k\x95#', 
        b'fONh3Z\x08+#\xab2\x94\xcbL\x03\xcf\xbb\x8f\x9cq\xa4\x94\xbd\x97\xc5r\x14?p\x9a\x9f\n', 
        b'\xadr\x15\xdc\xe7\xb1\x10\xfd0\x8cQcO\xea^\xfex\x8f\xd6x\x04\xca8^ai\xa6j\xda\x98R\xe1', 
        b'\xa9\xa0\xf7\xa7}\x0b\xd9\x83^`\x0bFO.\xcc\xbe?\x16\xb7g\xc2|w8\x14q\xac\x07f\xe5^y', 
        b'\x94\xc0\x80\x0f\x1b\xf6\xe1\x16\x97\xbc\xd8\x03h\x99V\xc2P\x87\xcc\x1b\xf4\xc8\xba\xf2\n\xf3\x82\xb7?n\x9d\xae', 
        b'\x1c\xbd\x03\x14\xcdV\xd3a\xb6\x8e\xf0\xef\xc2zcO!N\xe8\xa2]V\xe8\xea\xc1\xe9\xa4\xfcKt.\xd0', 
        b'\xf4\x8e_\xd1J5\xe0*\xca\xf8I\x92 |\x8f\xf7\x19\xbc\x0b=\xa6\x1e\xf3\xee Y\xb5[T"\x8dr', 
        b'\xa1\xb7D4\x8e\xe5ap\x93\xec\xb3\x07o2\x88v8X\xc5f\xfe4\xb63\xbc\xc56\xd0}>P\x03', 
        b'\xe8\xbc\xc5W\xf0\xad@\xf6\xe2\xcd\x16?/E\xe9\xceQ\xd3\xd4\xb6#\xa1p\x01\x154\xd6\xea\x03\x95\x1d\x90', 
        b'W\x18\xe8;\x03\xf7\x022c\xe2\xd5\x19IL\xfa\x9e\xd1\x18=\xfc\xa6}\xfe~\xfanG\x16\x81x\xb9v', 
        b'7\x9bZ\xa2\xa8&@\xa2\xab..g\xbe\xfaH\xf2\x11\x1e\xf0\xe3?_\xb3\x8d%\xda\xd0\x14B|\xfbw', 
        b'\x83\xf7\x8c\xa3D\xd5\xd5\xbe\x03Y\xc0\x02\x97jQ\x12~\xb6\xec\xc0\x93\xe9\xb3\xea\xcf\xd6-g]\x8f\x9e\xc5', 
        b'\xff\x1a\xb0\xdd\xa4>\x87\xc5u\xd75\xcb\xa0\x81\xb3\xa2*\xaa\xddFM<l\xbe\x95\x9d\xf7\xbcm\xdb,O', 
        b'\x0f\x818\n\xbbH\x80\xe7\x9ehL\xb9\xbdW\xbe\x18\x7f3\xb7\x8f\x90\xb8\x86\xa1\xa4\xf6b\xe6\xb7O,,', 
        b'E\xd0t\xe5\xa3]n\xb2\xfc\xf9\xb1\xec+%w+\x8f\xb9~\r\xbe\x10\x08\x92\xbax\x87[\xe9o\xbf\x0f', 
        b'\x99\x88\xb2\x96\xbf\x05\xcb\xb3W\x94\xe5\x15\xc5\x97\xfa\xdb#\x8e\xdf5\xfd\x97\x99\xf3Y[u>\xc8_\xe5\x9e', 
        b'w\xefK\x0c\xdf\xa3@x$\xf0\xe08O\xd6e\x17\xb4\x1f\xef\xd5J%D\xcf\xb4\x06db\x9b>\x05\x8a', 
        b'\xcc\xfc\xfb\x8co\xf6|\xdd&rd\x84^\x1bkfZ\x06\xb0\x138Z\xf0\x04\x801\xc1H\xfe\x1f\x8d`', 
        b'\x18k\xbb2V\x01 \xe9Y{Z)\xc9\xeb\xd7\x84\x82y\xdc\xea\xc0G0[\x99\xa7\xda\xd1"\x85\xf8\xae', 
        b'{\xa4\xcf\x1d\x001\xe8\xe39\xf3U\xf7\x87#@\x18M\xb3\xd4\xba\xc2G\xd9\xa1\x074#\xc1\x12\x92\x80\xe2', 
        b'\xe8\x9d$\xde\xff\x85O]\xc5\xf1\xe8G\x97eT`B^3\xf6\xd0\xde\xb0\xa5:\x99\xca\xe8N\x1c\xa8\xa1', 
        b"{\x18W\x9e\xd3\xfb\xb0\xc6\xb9\xf2>H\x154\x1eQ5Y'\xcc\xaf\xdd\x1f6\xcd\xd5\t0]\x94\xed`", 
        b'G1\r|\xf2\xff\x8e\x11\xad\x02\xd6ZO11\xec\xd3kB\x86F\xc8^\x04<;f\xe8\xb3\xf1\xb6\x82', 
        b"\xe8\x00\x02\xcf\xa0\xd2'\x97//\xa4\x87\xa0c\xaaq\x0b\xc0\xe4\xfe\xfe\xe7\xf8\x01\x05\xab\xe5\xf1I!\x8bu", 
        b"p\x05m\x05\xecl\xd7r\x1a\xf4}\x93\xf2\x00:\\\x1a\x0e\xdc\xfe\xca\xd9Y'uD\xc3.Yj\xbaG", 
        b'/\xfa\xee\xb1\x19\xed?\xa7a\xbd\xa2G\xe9\xefDjZ2\xa0\x95T\xc0\x9b\x89\x1c\xed\xff\x8d3\x84\xd1\xf7', 
        b"\x065\x06' ;\xf8\xed\xda]A(\xa9\x01\x1e\xc6\x89\x1f&Z:\rW\x9c\xe9E7U\xf1}\x7f\xce", 
        b'\x9f\xed\xf8Q\x9bx\xaf\xca\xcb\x81\x90\x9f\xdd\x05\xc3\r\xdb\xf8\xdb\xe3!0*\xa3Z\xec\xe2\r\x8a\xa8 \x9c', 
        b"\xba'7!f\xdb\x82;N\x06\x07d\xb4&\x0fa1g\x18\x8e\x86\xb3\x1c\xfd~W\xe6+v8d\xff", 
        b"\xc4}\x9c<\x06\xbf\x85\x9d\x8f2_\x85w%\x94\xafv\xach\xb2zE\xc4v\x1d%\xda'c7\xd1\xf9", 
        b"\x9a,Z\x84\xbb\nJ\xd1BxM\x85\xae\xd9\x83\x88'C\x8a\xe6T!\x13t\xe1QL\xb9\xe9\xfegv", 
        b'W\x82\xf8A\x08\xbb\x1fp\xd8~?\xa7j\xe1\x8cGr\x12\x8e\xfdv\xf8\xe3\x02\x82x\xb8U3D\x0cK', 
        b'\x88\xac"~\x13&q\x89\xac\x0b\xe0\xee8\xbe\x1ak\xad\x04Iy\xa0\xa9I5\x9d\x1a\x87\xccc\x02\x7fU', 
        b"f\xc1\xe4?\xd5U2j\x87\xf2\x90U\xd9\xba\t\x8cN\xeb\x02\x1f\xeei\xe0{~\x9b'\x83Z\xa2Z\x80", 
        b'\x0c\x01W$\x0f2\xcf\xe5\x890\xb4\t\xb2\xd7\xcfl\xaf\xa7\xb7\x99>\xc1\x16\xb9\xae\xb65\xa77\xf8\xe5T', 
        b'\x88\xce\x99)n7\xbc\xec\x04\xb0\xf9\xb6N\xbd"\xd8\xbb\xd6V\x01\xbf\xcfo\xb6\xac@\xe9\xce\x103E\xe5', 
        b'\xce\x9d\xda\xea\xe6\xbe\xef\x7f\xee\xbb\x0e\xc5\n\x8f\xb1\xe7&\x93\xcd\x05\xd5\xe7H\x96\xef\xb3Sv\xc1\xe3\xb8\x94', 
        b'\xcdB\x98\xdd\xad\x9a\xe1\x91M\xc6t\x1ei\x16\r\xbfd{ >Sv\xff\xe8\xf1\x85\xfe\xe6\xce\x9bC\xb8', 
        b'\xee:\x833\xb6T\\\xf9z!\xbfs\x86SfE\x89`\xf6h5\xfd\xaf]HE2\x7f\xc2\x16\xc4\xc8', 
        b'\xb5\xfc\xa6\xc3x[\x1d6\x84t\x10!\x9a\x86\xe4">%\xa6\tC\x97\x15\x89\x96\xcb%\xd9\xf0\xa0V\xa4', 
        b'Q\xd6>\x90\xa6H\xee\x8d\xa3\x11:\xac\xd0\xeb\xad\x92\xee\xd3T\x81&~%\xd0)\xbc?d\x8ft\x0e\xe1', 
        b'Dr\x18\x88\x7f!\xef\xd6\x9fw+\xf8\xcb\xc9\x00hoW_\x02"\x05\xfc\xd8\xcc^A\x1c9\xd0\xfd<', 
        b'\xf2]_\x99\x83\xd3\xe5\x1d\xea\xe2\xae\x1c\xb9\xea\xd4~\x82L\x90@)\xba\xba^\xca\x04\xc0\xd3\x84j!\x0e', 
        b'pb`lz\x1393\xeb9\xd3\xf0}\x1c?i\xe1\xdf\x96\xf4@@9\xc5\x8c\xf4W\x11<\x9f\x8f\x00', 
        b"\x96\xf5f\x8b\x08>\xcd(\xae?K}8\xeeIP\xa7Mx\x87\xba\x86\xbfq\x94\xe1\xc9T\xdf's\x18",
        b'"\x9fw\x9dn\x1b\x14\x8e\xef\xbe\xfe\xfe\x1ew\x1d}\x1b\xaf\xb1\x94\x8a\xbf\xf0^Ui\xb0t\x87\x85\xc0\x14', 
        b"o\xcc\x06,\xd0\x1c\xa6s\xc1\\\xb10\xea'JL\x85\xc4\xb5\x03\xccE]Kg\x08\xb9\xd3\xa4\xad\x9b\x9e", 
        b'\xcf\xdc\x8a\x03+q2\xae\x93\xf0\x15\xff\x07\xad\xf4H/N\x123\x10\x861\x96\xf7\n`\x13#&@&', 
        b"\xccL1f\x83\xff:y\x1b'Q\xeaq\x96-\xd4\x8b\x0e\xf4X\xb7\xa6.\x82X9\xd2\x11\x7fm\xf9K", 
        b'W\xfeO\xdaT\xf7\x0f\x06\x82\xc2+s>i\xb4e\x94X\x10.1 \xf9&\xe8\xb2\x96M\x8a\xb2\xaeM', 
        b"'|\xfbFJ\x9f1\xfe\xa4\x182\x81{\x0c\x0b\xa72\xa2e\x89\xa7{\xeaW\xce\xeeJ\x04\xf0\x9e>\x7f", 
        b'\xc8\xef\xd1^\x86P\x18AY"\xfb\xab\xcb.\xd4~-\xcaO(\x8cz\x0f\x87\xdd\xe0\x02\xbf\x12\x10\x96?', 
        b'\xd8\xc3\xdb\xf9\xe9o\x1ak\xba\t\xd8\xe8\xf3N?\x87\x15t\x18\x16\x19\xd4\xc3\x93\x1b*\xd5\x11\xea\x80\xdf\x14', 
        b'\xa0:B\xf9\x1aL\xc80C\xe6\xca\\\xe32@\x91\xcb9s\xe1*\x9e7p\x06\xcf\x06Z\x12iv6', 
        b"J*\x8eX\xd29'\xe6\xfe\x8f\x89D\xe7\xf3:\x80\x18\x98\xf2P\xe2\x90\x98s\x96\xd0\xe5\xe5y\xd7\xd4\x10", 
        b"\x80\xd2\xc1\x16L\xfb?\xbc\xf3(\xf8\xe3\x88\xbe\x9a\xb1n|\xaa\x0c'f\xf57S\xaaXw\xce\x97\xc9\\", 
        b'\xa8\xa7\xc0\xb8>\x0e\xf0\xfd0\xf7\xc4\xf9\x96\xeeX9\xf2\x8dl(\x1ck\x00/\xd0\xf8M\xf9\t\xbf(\x83', 
        b'[\x99j\xa2\xbb-id\xaf\xdb#\x82\xbd\xcb\x02Z\xfc)C\xb2\xd1\x9d\xdfL(5\x96\xc6\x86`w\xda', 
        b'\x18\xd1\xe6\x85u\xb7\x7fF\x03f)\x8f`3\x07\xfdc\xa6\xc0+\xa0%\xcf<\x93\x86Z\xde\xf0]\xa45', 
        b'\xa7f\xd7\xda\x12\x84\xae\xe9\x1e\x01{J\x07\xfc\xd9;y\x0b\x94\xaar\xf0\x00V\x16.^7<\xf6\x15_', 
        b'n\xf0\x0e\xa4\x89K:)@\xf8\x93W\xb8\xff(!^\xe6x^\xdd\xb4k\xea\x19]\x144\xc7r\xa0\xdd', 
        b"X\xd9&\xd5\x81\x12\xd1\x0cl|1\r\xc8\x9f\xc8\xd7\xe0+\xf2\x80C\x8e\xf3'm\xa3d\xbf\xa4w_\x18", 
        b'\xf57\x88\x1fxk\x10!\xb6\x0fM\xba{\x0f\xe6x\xc3<\xfc|\xa2\xd61\x9c<J\xd24Y\xd7\xd4n', 
        b"}'\xc2\xd9\x90sH\xf2\xaa\x18\x06\xb9?C\xf6\xa8\xfb^\xae\x07?\x08\xee\xf9\x0cq\xd5\x9f@\xc1|;", 
        b'%\xa3gM&)H\xbb\xa6-\x02\x16\x02|\xbe\x13\x0b\x88p:\t\x0c:\xdd>\x1b\xf1\x10\xee\x88a\x12', 
        b'\xa8Y:Ak\x85\x02k\x0f\xc8\xd0\xef\x18\xefW\xa8\xde\x0e\xc0\x0140g\x87\xb0\x84?\x06\x8d*\x99\xaf', 
        b'\xb7\xbd)\xc8\x00\x00\xe6\xba\x15\x9d\xd7/mo\x0e\x9d\xdc\xdf\x96\xb5\x13\xea\xc4\x1e\xcd\xf4\x14\x8cbh.N', 
        b'<\x81z\xc9\xbbE}\xd4!U\xce\xae\xf0\xdc<\xdd6\xb11\xee\xb6\x80j\xc2{\xe3\xae;@\x15P5', 
        b'\xf9\x08\xa6\xd9\x1a\x88\xc9\xf5$\x11\x013Zp#\xc9H\x98\xb9o+\xfd\xd7\xf0\xa5\x91\ns\x91\xbf\xbfT', 
        b'\xa9\xb6\xc7\x13\x85\x10-\xdf\x91\xb9h-\xd3\xe2\x8b\xa6\xd4Q\xa0\x02\xefI\xd3M\xf0\xa5\x9f\xb7\x1f\xf1\xf0J']

        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
    def test_valid(self):
        """Test if the validation function."""
        storage = {}
        trie = MerklePatriciaTrie(storage)

        # Add some data
        data = [[b'do', b'verb'], [b'dog', b'puppy'], [b'doge', b'coin'], [b'horse', b'stallion']]
        for kv in data:
            trie.update(kv[0], kv[1])

        # Get the proofs and validate
        proofs = [trie.get_proof_of_inclusion(kv[0]) for kv in data]
        for cnt, p in enumerate(proofs):
            self.assertTrue(trie.verify_proof_of_inclusion(data[cnt][0], p), 'Proof is not valid.')

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