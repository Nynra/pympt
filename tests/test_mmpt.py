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
        trie.put(value)
        gotten_value = trie.get(keccak_hash(rlp.encode(value)))

        self.assertEqual(value, gotten_value)

        with self.assertRaises(KeyError):
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

        with self.assertRaises(KeyError):
            trie.get(b'no_key')

    def test_update_none_existing(self):
        """Test updating one value that is not in the tree."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'value')  # Insert the value.

        with self.assertRaises(KeyError):
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
        with self.assertRaises(KeyError):
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
    """Test the proof functions of the MMPT."""
    
    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'dog')
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(b'dog')))
        expected = b']\xa4\x89[\x84\xf4\xadd\x82\x9f\x8a\x96\x92F`\x82\xe6\x00\x05\x1e$\x9b\xf3"\x02\xe5\xe21\x9b\xf6t\xe9'
        self.assertEqual(proof['proof'], expected, 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate a proof for each key
        proofs = [trie.get_proof_of_inclusion(keccak_hash(rlp.encode(kv)))['proof'] for kv in data]
        expected = [b'8R\xdaE\xcc\x8d\xe7<\xbco]\xfbsy\r\xd12\x9a\xa4\x12\x7f\x9e\x9e4\xa9\xf3w\x8b\x03\x8b\xd0\xd0', 
                    b'\\R\xc1\xcc\xa6p\xae\xd9\xc0\xac\xd9{\x1c\xcc\xe3\x16\n\x98hgJIJ\x92\x1b{!\x8b\x96\xedDr', 
                    b'z_`\xa7\xe8\x9d\xdc\x07\xacjg\x8d;A\x0ef\xe2\xbb\x1e\x94\xa9\xc5\xe8=0r\xde\xf4i\x0e\xf7C', 
                    b'h\x89\xfe\xa7\x86p\x83\xd3\xf4\x15\x93\xea\xfd[\xea\xbe\xae\xb0\xf4\x02k\x08\xad\xedO\x10\xfcE\x8b\xf5;\x15']

        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
    def test_proof_lots(self):
        """Test getting the proof of many key-value pairs with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [str(i).encode() for i in range(100)]
        for kv in data:
            trie.put(kv)

        proofs = [trie.get_proof_of_inclusion(keccak_hash(rlp.encode(kv)))['proof'] for kv in data]

        expected = [b'xk\x87?\x90D\xc0\x8d\xda\x07"\xd2T\\\xcabm\xe8%\x91g8L\x8bL\x97\xddfM\x92b\x90',
            b"TQ\x8b>'\\\xfdpjK{i\x84\xf7\xe3k\xb7\xe1,_\xf3\xea\xb4\xed.=~\xd8\xde\x14f\x13",
            b"\xbb\xdf\xa5X\xd3\xe5e\x7f\xf1U%qd\x97\xd1\x18\x98\xaf\xc1\xa5\x0b\xb8\x9d\xdb~M\x0f\xa7\x00'\x0cI",
            b'\x97\xad\xe6\xcb\xc0\xc6zR\xe6\xbb\xa84\xe3\xe5A\xda\xc1\x8cI\x86PWHn4\xc5s\x1b\xfa\xbc\x11:',
            b"B\x1d\x02\x91\x80\x01#\x14\xf0'w\xe2\x80\xc6\xffQ|\xb2\x15Y\x071m\xf8\xa1\xf5\xae+H\xf3\x9d\xec",
            b'\x02\xa9`\xba\xed\xedz\x0cl\x0b\xb6\x96\x15=\xa9\xe4,Y\xa3\x80V\x14\xd1E24\x13\xa6\x83\x893\x1e',
            b'i\x1e\xc2\x0e\xa9!\x03\xf2\xa4\xed\x8e\x94\x9b\xf1Y!\xb1\x0e\x9dL)\xb2\r\x8bW\x92\xab&\xaa\xf9\xc6\xe8',
            b'\x99\xfa\xb8\xe6\x8b\x84^EY\n\xc6\x016\xd8K\x80\xb8\xa5\x0f\xf6\x027\xd1\xfb\xc2\xae\xfa\xa6S#\xf1\xaa',
            b'\xce\xf2\x03i\x15\xe5R\xa6\xe0\xa89\xe8JNS\xbc\xeb\xf7\x0f\xe9iZ\xea\x13\xfc\x08\x86\x0e)x\xe5\xd1',
            b'b\x10x6\x1e\xe1{68\x89\x86\x0e\xc9\x87\x92j\xff\xea\xc7\xd4=P21\xe5\xd6\xbe\x7f\xa8!2y',
            b'\xeb\xc1\xc59j\x9d_\x97\xc2\xf5\xb3\\\xf2\xb9\xbc,sb\xdd\x16\xd1K\xa0%&\x95a\xc4\x12F?\x0e',
            b"@Tu\xd0\xf3\xde`\xe5\t\x15\x0b\xcb'\x11\x9aV\x96w\xa2#\x93\x80\xdbn >\x82m\x9e\x14\x7f\xbb",
            b'5\xc6\x19,\x1c\x1f\x92\xebN.\x13>1#Q\x19:e\x1aVP\x0c\x99{\x88\xe2\x066\xfd\xf5\x91\xa0',
            b"\xc5d\xeaj\x91\x81<:K'\xc7\xabPk\x98\x8f\xd9\x9e\xeb\x9d\xca\x02:\x08d>4\x01.\xdf(\x95",
            b'!\xfa0I@*\xf6\x1d\xae\x83R\xcey\\\x9a~BlL\xc6\r\x05\x8d\x01\xc5\x0b\xb0(_Hy)',
            b"\xe9'c\xca1\xfc\xc4\\\xd2\xa7\xa3\xf3\xf1V\x8a\xd6;-\xc4S\xcc5\xb4=R\xda\x07q\x1e\x93hs",
            b'TZ=,\xbe\xd1\xb4\x1eR<\xf7\xa7\xfcLW\xd8\xc3\xddm\xc3\t\xdb\xee\xea\x8a\x06]3\x97p\x96\xbb',
            b"\xd1\xd5\xe5\x1e\xb4\xa3\xce\xf7\xf0\x82\xf7<\xde\xdf`\xc0\xf0m'\xdc\xb6\xb2\x18g\x89\xa0\xf0\xc6\xb2\xab\xc7\x11",
            b'\xa3\xb7\x8a\xea\x1d\x85\xd02\x1d\xea1\xb7\xcfr\xc1\x07\xb8\x14\xfd+a!{\x13\x1a\xe1\x9f)qLK\xc2',
            b'[\xea7\xf3O\x9d\x88\xbd\x1a[2!\x13\xb8\x0c\xeb\x0b]\xb9[\x84\xf9\x18\xaf\x08\xb2\xd4A\x90\xb2\xc2Q',
            b'\xce-.yQz\x97p\x02_\xdd\xbb\xbdq\xe1V\xf2C4\xa2\x0f\x08\x98\x85\xf9\xca\xe4\xa2\xc3$\xf0\xa5',
            b';\x8f\\\xf7\x94\x05h\x8f>\xcfZ7?\x93@\x19p>~\xf4q-\x89\xa9\x12\x01\x89\xd4\xeeJ\x9b\xf2',
            b'G\xf3\x85\xc9\x89"\xd2\x10\xfb3\xb0 N \x92\xdd\x17\x94\x98\xf8\x96n=\xadZ\xc1-\x1c\x8a\xe2\xa3\xa4',
            b'A\xa8\x129\xb7\xed9\xad8h\xd1\xdb]H\x02*\x89\xda\x8a<\x88J\xac\x17IX\x15\xde=|\xaa\x0c',
            b'\x1d\x81\x9dqX\xa91\x8e@0\xa9p\xf6\x8c\x9e\x81x\xdf6\xe329\x15\x9b\x99@r|p\x19\x1a\x0c',
            b'\xa5d\xd1J\x80\xec\xbc\xb3\xdf\xfbl\xb7s\x13F(\xfe\r\xfb\xc5\x9dt\x1f\xb6r\xe7u\xf6\x928$\xa7',
            b'\t\x0e\xc0M\xf3K\xf3<\xa9\x17=\x07\xdb~U\xe9\xaf\xf9:\xf0\x01\xc8d\xbe\ne\xcd\x98^\xfcWP',
            b'\x18\x19{eX\x08\xc8A\xfc\x13\x16_ma\x08\x07\xcfN\xb6\xb2\xcb\x8a\x13\x98\xb5tnE\x997\xb7\xf3',
            b'\xbc\x93\xe4\x9e\x10rI\x9b\x96\xab\xc7\x03\xba;3)\x9fQV\x8f|l\x01\xad\xae\x8b\xfe\xa7Y#\x1e\x9f',
            b'\x8c\xf5\x86N\x195\xad\xb6\xa1\xc0!O\x18#\xaf\xa3\x85\xffz|F\x1f\x00\x10\xbe\x97\xa0\xfb<D\xd0x',
            b'\x98\xa1k\xa2e}\x99r\x12q\xc5\xddHI\xbc\x0f)\nQ\x05\x1f\xba$fq9\xb0\x06\x82fiM',
            b'\xa7V\xf1>`^\xd0\xc17]:b\xa4\xc5U\x0e?Sf\xf5?\xca\\"\x10l\x9b\xddH\xb4\x16\xa3',
            b'\x16\xb4\xb7\x12\xcc\x03\x14\xb0\x18\xfd-\x01\xfaEsKd\r\xd4\x93(1\xa8ey\xc0p*\xa7\xf9\x00=',
            b'm\x1c\xb5\x94\x17sdgx\xe1\n\x1cZ\xdew\xf2\xc2f\x9ag\xf6\x7f_\xdapb(\xa0\xa8\xfb)#',
            b'\x112\\ZH&\xbba\x89\xd80&f\x14\x05\x00\x04\xedf\xe4\x1d\x83\xb6\x06\\\xe0\xdbY\xdf\xfc\xdc~',
            b'd\xa5~Mv\x8a\xeb\x83G\x1b\xe51\xb3\x9bn\xd1\xbc6\xf7N\xbc\xc3\xafp}\xc8\xeb\x9b\xef|NR',
            b"\xba\x8c\xd8yx\xd2!\xcb\xbd'Uw;7\x98\x03\xc1%\xb8)\xff\xc4/&\xd1/\x0e\xf6\xeeCJ\x01",
            b'E\x00-E\x19-\x03\xdf\xf3\x91\x91\xb9\t\xfeYq\x84\xd1S\x9b\x8dD\xa9\xa8,4\xae\xcd=p\x9b\xaf',
            b"x\xd4\xa8\xc4c@\xed;\xa8\xb6\x06'\x18`\xd1\x83Y9\xb9\xf2\xc4\xa4\x95*\xc3~\x9dI\xb1\x9d#f",
            b':>\xb5\x02\xfd\xca\xf3g\xbc\x15)\xbaQ\x04\xff/I\xde\x08\xb7w\xf2CYI\xf6\xe1\x84GI#4',
            b'q\xa1\x04\x1f\x83-\xcfw\xedX*;\xfe\xcbE\xbe|v\xd79\x17\xb5/\n<N\xcd\x11\x1ea,:',
            b'\x96|\xf7\xa1v\xf6\xaa,\xabC\xab\x80,\x82_\xf1\xd8Ev\xd4z\x0c\xec\xe3\\\xbc\xbc\xf8M\x1f\xcbH',
            b'`<\x96y\xd8i\xc3l6\x83\xee\x9a$\xd4\xcdO\xfc\xcd\xfd~\xba\x06 F \xb0\xab"\xbd\x97\xb9\x19',
            b'\x03$\x87/yF\x80\xd9\x0c\x9d\x14_$\x02\xf0\xab\xfd\xd6\xad\xc7\xf0\xb4\xd4\x94\xda\xc9\xdd3j\x7f\x12\xb9',
            b'd1\xd3x5\x0c08\xef\x879C1\x10\x86\xf8\xe9\xa9Z\tE\x1aSt\x8e\xb1\xa6\xc4\x94\xc5>\xa4',
            b'\\\x05%(\xfe\xf8\x1d\xd6\xe1\x93\xb0\x08\x1c\xe9\x81\xd1\x15\xfc\xe6\x8d\xa4\x01\x1at\xd2]\xe5TJ\x0f\x84\x84',
            b'\xa28\xd7\xf0\x06U\xc7P\x97\xc9\x10X.\xdc\xf0\xacD\xa4.rJ\xbe*\x9a>\x13\xee\xa3\x8f\xcf3|',
            b"\xce'O_{\xc6Dbd;:pG\x85bV\xa3\xdd\xc1\xc1]\xdbN+\xaf\xc3\xa4\xa5\x0c~\x1cD",
            b'\xbd\x95,C\x84&\xba\x06$\xd8\xccA\xb7\xc9\xe83\xefb\xc5Z\xc9\x86H\xb2Y\xdb\x9fz@\x0b\x14\x82',
            b'\xa6\xa6\x8a&\xd5OV`ct\x069\xb2\xaa{\x17_\x120\xf2\xb8\x92\xac\xbe\xd20H\r\xbe+\xfd\xe3',
            b"\x86\x9a>O\xf8o\xbc\xdb_\x10\xbc\xb9\n\x93]\x16s\x1f\xffs'R\x88\xe2\x17O\t\x81o\x14#\x02",
            b'\xc0^\xaf\xc2\x86\xa3\xe1k\xedlC\x11O\x11\x05|\x83\x80\x1e\x88v\x81\n\xb2Jz\xc8\xd2\xcd\xbe7\x83',
            b'4ut<\x9b\xe2\xd9\x98\xd7\xfe\x9b\x06\x00\xd9\xe4P\x9bM\x1cq\xd2\x97II\xe2\xd59\xff\x92\xdf\x1d!',
            b'\xba\x9f\xe1:\xf5\x8ckk\x1c\xe9\x17JpJ\x1c.\x1b\xb2Y\x10\x9b\x1f.\xa9Y34~\xe0\xdb\x8c\xc1',
            b'C\xe9\x9d \xc7\xd0%\xe8\xcbn1C\x838\x89_\xd28]\x1e\x141\xc3\x8e\x19\x8f\x1c\xa3\xac\xa6\xca\x89',
            b'\x14V~+\xb5\x9f\x04r\xfbt\x9a/if\xa8\xb3@T\xd3"Un\x7f\x83\xaa\xa9\x1b;\x1a\xab[(',
            b'\xd6c\xc0Y\xa3\xc3j\xa4\xd9\x10\x91L\xb8n&\xd7\xf01B\xf6rg\xc5\xdb\xd2\x84\x1a\xba\xe9\x80-\x95',
            b'\xa9\x17\xfc\x1e\xa2w\x80\xf3TUY|\x8e\x02\x06Y\xc5\xf6\xf8\x7fj\xf6\x91\x14,\x0eNR\xd6T\xfc!',
            b"\x9b;F\xe5w\xda\xfb\xcf#E\x90\xd7'0 &\xd5\x19\xc3\x86\xd0c{\xb1\xb3\x14\x109\xcd\x0eV\xd5",
            b'\xaa\xc63\x81\x0b\xd4\x8d\x9b\x83\x82\x89\xf6*\xb1\x06\x03Q\x89\xd7\x99\x88t\xd1#\x8a\x0bZ\x9br\x88\xf1\xeb',
            b'\x99\x19\xc7\x97\xb5\x11\xe93-\x84\xcdd\xbfM\xd0b\xe2I\xbf\xa6\x8d\xdb\xc8\xac"\xa1\xef\xa3_-\xd0\xf9',
            b'aG\xf2\x0cLu \xd47(\xad0\xb7|\xd5\xac\xda\x08\xd6o\xb56/0\xf3\xbc\xacB\xc2\xcb\xd1\x0e',
            b"\xffq>\xc3\xd3#{\x0f \xc9\xfbW\xfb\x915\xb2\xa1\x1dR\xc0\xa2'\x07\xff\xb9b\x1f\xb8\xa2\x1bB\xa3",
            b'\xf7\xc6F=\t\t\x8c\xc4\xa5\xee%\r\x85\x1a\x1dcHE\xd1A$\xdd\xb1\x1d\x7f.\xe7\xc5R\x16\xd4P',
            b'\x83\xd7\x18\xc00\r&\xe7\xbd\x98l\xa2f\xf5\xab\xc6\xa0\x0bq1\xd5\x96\xf0\xfe\xdc\x9f\xd7\xdaz\x0fy\xaa',
            b'\xcd@\xa6\r%\x8f\xcc\xc6\xee\x94:\xdd>\xcbS2\x83\x8b\x84\x11(\x17\x9a2(\xe9=\xe7\xddM\x0c\xcc',
            b'\x052x\xde\xf7a]\xa8\xf8T^ \xf5\r\x05\x90\xfa\x14\xd0<\xcf4\x873\x14\xe6\xf4\x913\x9b\xf2\n',
            b'g\xab$\xa8\xe5YxC\x81\xd8\xd8\xe4\xbc\xbf)\xa5\x10\xfc\xe5~\x80\xaf,\xd3\x84\x8b\xbc\x89^\x1c\xb6\x13',
            b'Sl\xac>\x17\xef\xd8\x89k\xfat1.&"W~#L\xbb,0\xa3\xecj\xe7~|\xb5\x04\x06B',
            b's\xb5+e\xaa\xed\x96\xf0\xd5\xc3\xca\xb4a>r\x0e\xc2\x07\x1aa\xad\xbcvz\x81y\xdd\xdc$`Y\xf8',
            b'[\x9e\x7f\rs\x8e\xa1\x83J\xcaT\xc1\x9d\xc4\xca\x85\xff\x00{\xc6:\xc4\x96\x12G\xad\xaf\xb3w(\x13\x9f',
            b'S\x8eb\x7f\x18\xf3\xfbB\xfb\xac9\x9d\x05t1\xac`\x0bK\xc0\x7fS\xa8lV\x19\xb4\xddh\xb1\xb1\xb2',
            b"\xa6\xaes\xc6\xac\x1d,'I\xf4\xc3ut\xb7\xcb0\x9dn\xda\t\x92y\x9esI\xe4\x9c\xe2\xaf\xb0\xcbp",
            b'\xee(\x86\xf0+\x8b:o\xa8S\xc1&\x0c\x98\xd3\xa0\xa3$p\xec,\xef\xf4#\xc6;:#\xb6\x05\x87\x80',
            b'k\xc3\xc3$K\xcf1\xddf\xce\t_?\xe0B\xc39\xdf\xb7\xeei\x9e\xd3\xf3\r$\xa8\x01\xf9r;\xfc',
            b'N\x913\xc9\xcf\r\x8f\x0b7\\?\r\xc6\x92\x91\x8fV\xcc\x8eR\x94\xdd\xff\xd4\xfd\\\xaa\xf6\x078o\xd2',
            b'0\xcd\xaf\xd8\xcb\xf2q\xcc\x83\x94[\xa5\xb9\x15\x8d\x11$\xf7?\xdb^(\xe0!\xf1\x848\xf7\x1e\xacG0',
            b'P\xa4\x1c\xe7\xaa\x8e\x0f\x1e\x17\xd1\xd4w\xea=;\xe0\x0f\x8b\x06\xd2n\x7f0e\x87\x9d\xc3\x0c\x96\xfc+\xcf',
            b'\xd8\xf7^\xa1\xfey\x8a\x96\xc0#\x04\xa8\xf3\x1e\x18g\xcf\xe8r\xa3\xa7:\x01}4\xd4\xfcpd\xe6\xde\xe0',
            b'\xe1n\xaa;i\xceYm\xaaE\x90\x1a4\x18V{(\xfb\xd8v\xd2\xfb\x8c\xaa\xd6@\xca\xda,\xb9o\x9e',
            b'8\xca\xd4E.r+\x10\xdc\x89\x8a\x1b\x95\x0e*Fy\xc3]\x9b$\x86<\xae<\x92Wf\x87\xc2\x03\xbc',
            b'6\xf1\x03\x82\xef\x83\xe0\x11\xa9\xdf\x11$\xdd\xfb\x19x\xbc\x19R>^\xa4j\xdc\xf7\xc5;\x9dZ\xd0<6',
            b'Z\xe5\x9aDP }\xa8/\xdb^\xc8>~=\xe6#V\x8a\x9fB\xb3\xbcwj\xa7@)ok`\x17',
            b'\xf8\xc97\xc5\xcb\x99\xfd\x8f\x1c\t\xfa\x08\xf1&j\xfb3\x0cJ\xf3\xfbfL*I\xa6\xba\x9b\xee\xb8N\x11',
            b'g=\x88\xa1}\x9f\x96v\xb7\x93FNR\x86\xff\xb2\x0f\xea\x9c\xd6\xe4\xd9\xa9#\xaa\xae\xbe\xc9\xe0\xf0\x99\xbc',
            b'\xc3^\x1d\xd4qIjL\x88\xf4\x92\xc0{h\xe40>4\xb6\xc0\xf4z|\xe1_$\\\x899\x98\xdfH',
            b'\xe0;-u\x18[\xf3,\xa6\x99N\x8e\xad\x14\xe5U\xcc^\xaa\xe7\x9e#\x03\x7f\xc5v\xc4\xeb\xb2TI>',
            b"\xd0\xc3\xbd\xadm(\x03_\x1a&\x10_\xd1#\x92=\xb8\x17\xbb\x81\x7f\xe2\xda\xac\xfd'\x8c\xb25\xca\x8c\x80",
            b' }x\xae\xff\x16\x1aa\xa1E\xabQa;\x96\t\xbf\xb9\xbd\xffD\xd6\xae7+[\x8b\xdf(G\xb2\xf3',
            b'\x89\xc4\t\xe7\x11\x1bI\x92M\x1f\xba\x18h\xa2\xf6\xd7H\xbb\rO\t\x01\xa0\xe0\x8b\xe2\xf4 \xb96D\xe7',
            b'\xf3\x14],\xb9\xfeW\xa2T\xc8\xbb!\x9a\xa3\xd7\xad\x94\x89\x1d\xe5\xb3]u\xb6\xe6\x80lR\xb4\xa8\x1a\xbf',
            b'\x00\xe1\xea\xe3\xec\x7f\xf66T\xac\x16>\xe2Ua\x9fy\xbcd\xc1\xee\xd9\xe7\x81\x92\x99\xf9\xa3\xa9\xd9p\xe1',
            b'`grG\\\xaf\xe6Z\xbfT\x11x\xea\xd17r\x1e@!L\x1b\xd3m\x88\xcc\x89\xe78Q+\xecN',
            b'\xe5\xd43&}\xb1\xf2\x07K\xd6\xe6\x8crj\x9c\xd3\x99}Y\x11}\xa2[l\x14\x9f\xb7=\xb9Er\xc7',
            b"v\x1b\xdeI\xfdg'\x97\x00\xe7\xc7\x94BH3\x08E:\xe4u\xb0\x01\xd1\xb9\xbe\x95\x87\xbc\xeboL\xc0",
            b'\xfcUH\x01E\x11\x03h\x99\x03f\xfbF\xe6\xe4xD\x89\xfb`@\x8cc\xe7\x7f\xb8\x19\xc1\x95\xc5\xfb\xa7',
            b'\xa9\xdb\n\x12Je\xf1KH\xaf\xd1\x7f\x93\xd3\xf3\xa9\x9c5\x11\x8c1\xb8\x14!\xdd\xba\xde\xc8\xd1\xef\xf8g',
            b'Y\x90Z\x1c\xd6o\xee\x8c\x84\x88\x11\t\x96\x91\x17m\x91\x94\xbds\x16e(U\xd6\x12TfG\x8f\t\xfb',
            b'p\\V\xfd\x92\x1es\xa0@\xde\x99R\xcd\xb6N\x80$m\x0eR\x92\xc3|\x03\ndIve\xc7\x9d\xb7',
            b"\xdd\xf7B\x077\x1b['T\xee\xe7\x9eu\xfdl\x83\xeb\xdc<\xf5\x1e\x9f\x1a\xec\xe5\xf5e\x02H\xf1\xf6\x82"]
        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(data[i], expected[i], proofs[i]))
    
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
            self.assertTrue(trie.verify_proof_of_inclusion(
                keccak_hash(rlp.encode(data[i])), proof), 'Proof for {} is not valid.'.format(data[i]))


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
        trie.delete(keccak_hash(rlp.encode(b'dog')))

        new_proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(b'doge')))
        self.assertNotEqual(new_proof, proof, 'Proof should not be valid.')

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
            trie.verify_proof_of_inclusion(keccak_hash(rlp.encode(data[2])), proof) 

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
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(data[2])))
        proof['proof'] = proof['proof'][:-1]
        self.assertEqual(trie.verify_proof_of_inclusion(
            keccak_hash(rlp.encode(data[2])), proof), False, 'Proof should not be valid.')

    # Test if the proof is valid when one char is added
    def test_verify_one_char_added(self):
        """Test if the proof is still valid after adding one char from the proof."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        # Add some data
        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Get the proofs and validate
        proof = trie.get_proof_of_inclusion(keccak_hash(rlp.encode(data[2])))
        proof['proof'] += b'0'
        self.assertEqual(trie.verify_proof_of_inclusion(keccak_hash(rlp.encode(data[2])), 
            proof), False, 'Proof should not be valid.')


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

        # Verify proof on copy
        self.assertTrue(new_trie.verify_proof_of_inclusion(keccak_hash(rlp.encode(data[0])), proof))

