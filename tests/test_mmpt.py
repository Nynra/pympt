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
    from src.mpt.proof import Proof
import rlp
import unittest
import random



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
        expected = b']\xa4\x89[\x84\xf4\xadd\x82\x9f\x8a\x96\x92F`\x82\xe6\x00\x05\x1e$\x9b\xf3"\x02\xe5\xe21\x9b\xf6t\xe9'
        self.assertEqual(proof.proof, expected, 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate a proof for each key
        proofs = [trie.get_proof_of_inclusion(keccak_hash(rlp.encode(kv))).proof for kv in data]
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

        proofs = [trie.get_proof_of_inclusion(keccak_hash(rlp.encode(kv))).proof for kv in data]

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
        proof = Proof(target_key_hash=og_proof.target, proof_hash=og_proof.proof + b'o',
                    root_hash=og_proof.trie_root, type=og_proof.type)
        self.assertFalse(trie.verify_proof_of_inclusion(proof), 
                        'Proof should not be valid.')


class Test_proof_of_exclusion(unittest.TestCase):
    """Test the proof functions of the MMPT."""

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
            with self.assertRaises(KeyError):
                # An error should be raises because the key is in the trie
                _ = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(d)))

    def test_proof_one(self):
        """Test getting the proof of a single key-value pair with trie in secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        trie.put(b'dog')
        proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        expected = b'\xf6\xb3\xc4\xe6T\xb6[@\xdb\xf7\xeaZUj\xad1\xda>\x84\x170E\x01\xe3KQ/\x90\xdd|\xf68'
        self.assertEqual(proof.proof, expected, 'Proof does not match expected.')

    def test_proof_many(self):
        """Test getting the proof of many key-value pairs with trie in non secure."""
        storage = {}
        trie = ModifiedMerklePatriciaTrie(storage)

        data = [b'do', b'dog', b'doge', b'horse']
        for kv in data:
            trie.put(kv)

        # Generate some non existing keys
        keys = [keccak_hash(rlp.encode(i)) for i in range(4)]

        # Generate a proof for each key
        proofs = [trie.get_proof_of_exclusion(kv).proof for kv in keys]
        expected = [b"\x16\x97\x9bj\xf2<X\x9ds'\x99+t;i\x9d|\x8a\xc1\x80.\xce\xfc\xae\x0c\x00\xc9\xb9\xa5,\x02T",
                    b'\r\x00\xa6nE\x13\xfd\x95O\xaf\xbf)88\xfd\xc3,\x14\x16\xcc]\x00 \xb5\xd1\xe8*=eIh\xc6',
                    b'\x0f\x1a5\x11\t-9\xe4X\x87\xec\x80\xc3kH\x15\xce9y\x02\xf8F\xcf\xd6?\xfbU\xeb\xb2M\x89\x11',
                    b'\x8f\xc6\xd4\xfa\x00)\xec/\x0e\xe7\x14\xb6\xaeS\x183\xbf]\xb6\x0c\xff\xddM\xa99\x12\xe0{\xbf\xda\x84+']

        for i in range(len(proofs)):
            self.assertEqual(proofs[i], expected[i], 'Proof does not match expected for {}, expected {}, got {}.'.format(
                            data[i], expected[i], proofs[i]))
    
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

        expected = [b'\xb8\xe2\t\xf6U\xf5O5\xb4\x9ad\xbbWR\xfb9\x18/\x07mw\na\xb4\x18.a\x1e(\xe72\x07', 
                    b'\xddd\x9d\x8d\xc6\x04O$\xc7\x95#\xa2x\x112\xd6\x99S\xec.\xbf\x02\x8f2s\x12GC\xc2\xbe\x06\x07', 
                    b'\x93m\xe13\xfb\xc0\x04\xdf\x93\xec"\x99\x0e\x00\x88F\xd3\xe0\xfb\xdf\xe9\xed4\xc7x\xc6\xcfK\xc0a!4', 
                    b'\xfbfy\x95\x13j\xe9r\x08g\xb4\xa7Q\xec\xd0fU\xf6 \xcf\xeb\xc4\xe6\xc4\xb8`\xee!\xb6\xbba\xb1', 
                    b'\xe7E\x82\xe0\xa6\xe4\xf4\xe6v\xdb\x8f-\xed}9[\xc73w\xa2\xec+\xd5c\xcf\x13\x85\xfe\x87\xf4\xb9\xe8', 
                    b'\xbd\x88\xbeD\x88E\x94\xca\xe4\xe2\x98\xd7uk\xb4\xbeR\xc2\xc8M\xcb\x1b\xd3\xc9\xda8\x80\x0f\xe5\x12\x89*', 
                    b"\x8f\xf3\x94\xc9j\xc0\xff\xc7'8\x06\xafHB\xb2\xb3U\x81\x16\x87\x87\x8f\xba\x8dU\xf3\xc7\xc0\xf91'\x9f",
                    b'&\xa6,\xa6(\xe7\x96\xcf\x8b\x17\r\xf8\r\xc3\xf4x\xbd\x15*\xc9\xb43\xfa\x06R\xd0P\x93o^\x12\x9a', 
                    b'^\x8cs09\xab\xba\x1e\xe2\x8cpd\xec\xaet\xbc\r)\x98>G-(Pe5\xb2\xe5\xeb\x0e\xff\xba', 
                    b"\xfd\x80\xfbcT\rQ\xaexG'\x97\xb8'\xc4\xae\xa8b\x97\xb9FE\xa4\r\x97^\xb0\x86\xbc^\xc5\xad", 
                    b"bY\xa0m\xcf\xb9\x1c\xf1\xb2Jt'\x89{=|\x91\x17\x80\x86uK\xc8\x81X\xe4\xb1\x04\xcdk\xe9g", 
                    b'\xaf/\x00\x04w\xe9\xccA\xbe\xd5t\xe8\xc9(\x15\xba\x8d\x9f\xa2\x185\xe5\xa8\xea\xba*\xdcs\xafg?\xdc', 
                    b'\xf9^4\xac]I\xcd\x8b\xb0\xf7\xb9\xef;\x0cb\xd1\xa4\xdcJ\xfc\xaey\xa6\xa8B\x0fun\xad\xf9\x80\xb4', 
                    b'\xfa\x00\x893\xbe\x90n\x1f\x04\x9dfBo\xc3\xc2\x14\x14\xcf\x0egAd\x96\x0b(\x00\xc4\x99\x80\x08\xeb5', 
                    b'#V\x9cz\xe7\xfc<\xe1\x84\xe4\xccxl\x16x\x98j\x14p\x89@f\x94\x81ZG\x0bJ\x11!\xad*', 
                    b'\x8dRc\xf2\x82\xc2\xd7\t\xd2\xe3\xda\xc3\xab\x87\xf9\x8b\xedGc\x07E\xca\xdd\xb2z\xa2\xd3\x9b\xc9\xc9%\x91', 
                    b';\xdf\xf0k\xd4\x1b\xe6\xa0\x15\x01\xaazu\x9d\xb1#\xe4\x19Y\xf1\xa3\x7f4~b\x0b\xde\x19M\x1e\xcc\x98', 
                    b'I\x15D\xd7s?\x05\x1fdx\xe0It`\x87\xe1bQ\xeb\xd8\xe5\x0e\xd4\xe9\x0f\xbb\xbbg[\x8f.i', 
                    b'\x82\xa3b\xfa\xb5\xae\xba\x18<\xb6\xc4\xddAF\xf4m\xb23\x83\xdc\xcb|\xa8\xb5\x00\xe8/\xefE\xc1\xab\xad', 
                    b'ed\xf9clAF\xae\nZg\x1e\t\x91\xe7\xd8\xf2\xc65\x1c\xbd\xf2TgMvY\xaf\x1d\xcf#\xaf', 
                    b'\x13! \xa8\x0b\xc6\xc4\xf1\x8e\xcbg\x86\x1a.Z(\xf6\xba\x05\x8f\xeb3\xb8\x91\x99\xafr\xef\xdas#\xdb', 
                    b'\xc8d\x0e\x8b\xe3\xe3\x88\xed~\xb4\xc0\x1f\x85|\xb4f\xe8n>\xc3\x9a6\x8a\xe5\xda\xe4{\xc9|\xc0\xc3\xbf', 
                    b'\xf6\xfaB\xd5\x84)\xd99\xf9\xde\xe3<\x98M?\xd8`1\xaa\x8aK}\x8a\xba\x1c\x84\xa6\xcauwU\x1b', 
                    b"\xc3\x0b\x99\x8e\xd4O\xdd\xf0Bw7\xee>\x7f\xa9\xfc\xf5\xc5%\xd3'\xdd~\xf5P\x1b'\xf2\x8a\x7f\x9fT", 
                    b'\xa1e\xb0<\xdb\xb9r$)\xd0\xcdFx\x16\xc6\xa1\xf4\x83\xc3\xff\x7f\x9c\x19<{\x1b\xa9\x86\x90\x12\x8c\x93',
                    b'.\xfc\x1c7@P\x95\xff\xfe\x1d\x8c\xb4\x96\xe1\x08\xf3k\xdb\xab\xc5Sv\xdc/\xc6`]\xda\\\xe4\xc9\xcb',  
                    b'c\xe6h\xcc<:\xdc\x02\x15n\xde\x9b\x88Sa\xf8\x83\xb6\xfd\xd2\xdf\x9eo\x80\x13\xd5\x96\x80o\xe9D\xba', 
                    b'\xd4\xe4\xa7\xb6Y.\xef\xd9c\x8f\x08\xd57\xae\xd3D\xd5\x85\xd8\x19\xcc\xf8\xa5cuV\n\xec\xde\xeaj\x04', 
                    b'\x1e\xcd\x94N\x93\xd6\xd0\x9c\x90\xf5M\xc9\x11\x10\xea\xbfv\xed\xab\x1e\xc9\xc5\xe5\xaf\x1eT1\xbf\xf4I\xb7k', 
                    b"z\xf1\x16E\xa5\x83\x0e\x9e\xe4\xdfO_'\xf8D\xcdh+\xd7\xad\x0e&9Mf\xa3U\x8a\xb8i\x02/", 
                    b'\xeb\xea\xdf\xc7\xe8\xae\xd8\x8f\xac\xed=\x83\x8f\xdd\xf7H8,{\xe1\xaf0e\xbaP\xa76\xc8>\xdcz\x80', 
                    b'\x94(\xf7?\xfd\xb3\xfdU\x00<h\xcfq\xe85\x9a\x11\xeeu\x8f\xd0k\xc9A\xd0\x9c\xe9\xe7\x9e\xcd\xca\xcf', 
                    b'\xff\xbd\xcc\xd1\xe3\xedm\x84J\xe3\xd3\x0es\xaa\xf0b\x80h\xad\xeb:!\x94a\x8b\xbf\xf4\x08\x8a\xa6\x7f\x08', 
                    b"L\xbcF\xb9\xc9\xbc\x98\xa6'`\xea\xdeu\x8e\x86\x1c\x15L\xa5y\xd7n\xad,\xcc0-\x0b3`?\x8e", 
                    b'\x8f\x89\xeb\xb3\\\x96\xc5\xe2>\x9eB\xa9\xf9\t\xf6y\xfd\xd7V!\x16\xec\x96\x15\x99\x86\xf6\xac\xccW?\x0f', 
                    b'\x05\xe2\xbcg\x9fU+!\xe3\xad\xd0l\x8c\xf8\x1fX\xad\x81\xdc\x13C\xca\xa4yd\x03\x1e\xbd\xd5z\x95\xfc', 
                    b'\xcef\x03b\x91Y\xe4\xe3\x83\xf3\x90(<W\xc1\xc1\x9e\xd9\x91/h\xf9\xd6r\xc6>\xd1\xa0\xa8uF1', 
                    b'\xd2\xb1\xb9_\x17\xd1\x8e\xac\xdf\xfe\xad"\xc0\xb7D\xa4"\x99~\xb8\x00,2\xd1\x8b\x0f\x96\x8b)\x92\x11\xa7', 
                    b'\x0eW\x1f+Pr<\xce\x0f\x85z>\xd9C\xc7d"\xd5G\x86\xce9\xe6\x96\x01c\xd2\x96\x89\x8b\x0f\x81', 
                    b'\xb3\xd8\xfe\xa8\xae\xfao\xfb2DS\x026\xe8\xa6\xd3L\x12\xe8\xac\x9a\xbaO\x8f\xb0\xf8\xac\xc0\xccf\xabK', 
                    b'\xf7\xfbS}\x8a\xa8\xcc\xf0\x02\xee$\xa4\x90\xb3\xac@O\xec\xf4A\xed\xde\xd3r\xd2\xa5\xa7\xf96\xd4\xd5\x01', 
                    b'Q\xc3\x8b\x91,\x7fQHaf\x8e`\xbeL\xcfd\xbc\x86\xb1\x1e\x84}\xf2\x8c\xba\x88tH\xb0\xaaC2', 
                    b'\xfa\x18<|k\xb7\xe1\xeb\xc6)\xb6\xcc^\xa9\xc5\xb0@\x8a9\xee)\xa5&\xd6\xcf\xb6\x1cVZ\xcaO\xd3', 
                    b'\xdd:\xdc_\x18\xa2\xd1\xb0fr\x99_\x83\xa0)\xaf\xa7\xb5\xeaQ\x8aK>-\x81\x8b]\x0c\x16Wj\xfe', 
                    b'\xa7\xc9\x9d\x9cm\xe7\xf0Wq\x08\xfa}\xae:\x9a\xa9]\xb3\xaf\xfa\x952\xfd\x1cg\xd9\xf8\xa6\x94\xf6)\xaa', 
                    b'\x8e\x04f\x1c\x0c\x9eY\x81\xd3\x97&\x02oT\xe3A\xce\xae\xf4\xa7\x9c\x06\xd4\xd5\x9a\x97\x9b8\x1bIsD', 
                    b'\xf2\xd5\xady\x13\x96\xd6}\xc6\xc4\x0b\xa3\x9a|\x193\xf9\xe5\xb1\x88\xc4\xd1,\x13\x1d\xc6Pq\xd7\xbd\xd5\xfe', 
                    b"\x88'\x7f\xe9yQ\x95t\xf6[\x8b\xeaXt\x13\x97WU\xa4\xbb\\\x1dq\x0e\xf1\\zY\x1dr2`", 
                    b"g\x04U\\o%\x85'\xa6Qe[\x05\x80h/[c:\x17!\xec\xa0y\n\x15\xd8W`,\x03\x1f", 
                    b'\xb9\xb87\xe2P\xad\x0ej/\xdfn\x19\x92\x06\xb4\x99p[\xc4\xb4\xeemi\xd5\xa6\xad\x8b\x80;\x9f\x9d\x9c', 
                    b'\x150\xa7w\x91\x9c\x08S@\xb6_kI\xef\xd2\xbf$\xc9\xa5%f\x1bS"\xef\x9b\x86f2\xd8\'|', 
                    b'\x02SD*\x9d<\x98\x8b\xf2\x05\x9c/<\xa5|\x99\x1b\xd5\x9a\xf8B=\x99.\x94\x83P\x87\xbe\x9f(\xab', 
                    b'C\x7f\x1d\x19\x8a\xd2(c\xedA\xad\xb9P\xc3 z__\xf9\xa8\r\xac\xe8\xfd\x85|h\xbc\xd2\x9d=\xce', 
                    b'\xde\xe5\x90\xaf\xaa\xc16\x7f\x9a\x0e\x85\x12\x16\xf4\xe81 \xa2D\x0b\xe3\x1c\xbd\x0e\x1e\xab\xb9\x1c\x81-\x19\xfb', 
                    b'h\xf7\x10\x9d\x10\x9c\x06\xfch\xd3G\xb5\x0c \xe4\xb8?B\xc6\x92\x91\xbbYJJ\xfa\x8b\xda\xac,&&', 
                    b"v99\xff\x87\xfd\xdc\xc0+\x85\xdf\xff'\xcb\x88\xa6\xcf\x9c/\xa2/X\xbd!\x7fn5\x08\x9a)\xd1\x8b", 
                    b'{\xff\xfe\x06~I\xd2XR\xf6\xc6\xa3e\x82\xbd\xc4_a\xb5 \xc3o\xe7\x8d\xc7\xc9\xb3\x0f\xd5\xe8\xbbS', 
                    b'\xed\xa2\xfeW\xcf\xc3\xd1xF\xd0x\xbc\xc6E\xad\xf7:$\x84\x80z\xf5t2=\xd0G(-\xa5\xfe\x82', 
                    b'\x9a\x14\xe6\xeb\x8f\x15^\xee\xdc\x04|\xbb\xee8\xc0\xda\x16\xf63Km]7\x96\x85\\&\xf2$\xb9\xd3\xd5', 
                    b'r\x94\x9e\xbe\t.\xe2YD\xae\xc4\x91\x08\xe1z\x1b\xa5\x10\x8d\xd1\xe5\xe4\xab,\xcc\xa5\x18\xfe\r\xc9f\x8e', 
                    b'\x84\xc6\x90\xfc\xc20\xc5\xeeN\x80\xc2w\xd2\x07\xf0\x82\xae\xf6\x9ac\xc4K\x13H\xb6\xafQ\x9e\xcb(\xceC', 
                    b'(6\x9c\x10\x06U\x13\x8a\xde\xf7-\x92\x9b\x19\'\xd3\x81"L\xb5X\x00\xcdY\xab2\x8e\x98O:j\xf7', 
                    b'\nqGC\xd5\xc4\xe8\xbd5\x19\xcd~\xa9\xf1\x8f\xfb\xce9[\xec\x9d4\xb7\xcf\xb7\xf64d\xf8\xd2\xdc\xcc', 
                    b"\xc6\xa3\x13g\x80\xb6{\x10rJ\xcc]E\x86\xbe\xd3'-:\xd1@\x0f\xff\x1eVbv\x1b,\xbe\xb0\x91", 
                    b'\xf5\xd3\x8e\xd4d&Hn\x19\xe2\xac\x9e[\xc7MR\x04a+j\xc6\xccX\xc8\x85\xc1g\xd3\x04\x00\x85\xeb', 
                    b'\xd0\x83>+\x94#\x9b\x7f\xf3\xcd\x04SC\xeb\xeb\xf8\xa6E!\xdb\x18\xb2\xfa\x8c\xc1&\xe6RP\xf0\xf7\xb7', 
                    b'\xda d\xfc\x12\x94\xfb\xa44\xa2\x8e\xf0\x91_\x0b\x98\xdf\x10\xe8%\xa9\xcd\x12\xb4\x1bq#{&\xef7\t', 
                    b'M\xbf\xf0\x84\xe8\x9fPY\x1a4\x94\xac\x91P\xd7\xc9A\x19b9gI\x80\n\x91\xb8\xe8\xcd\xc5\x93\xe5\xe9', 
                    b'e\x99%\xd8\n5h\xbd\x80e\x9cQH\x97\x04V\xb6\t\xd8\x85\xac\xa1\xb6\xd7uq*\xdb\xc4\xce\xea\x95', 
                    b'<i\xa1\x978=-\x13\x88*\xceJU\xb8\x9a\x83\x0blMTe\x84\x0c\xec~mD\xbf\x1c\xd8\x1dR', 
                    b'%\xdcd\x87\xce\xb64\x85U\xc3\xb6\x95\xc1\xfc\xc9\xe4\xdd_\x98\x01\xf4\xab\x86lj\x94\xab:l^T\xcf', 
                    b'*(\xd8\x01\\\xc4\x18\x90kt\xc9\xda\xd8D\xa7q\x98\x12\xe1\x12\x11\xd5,\xdd\xba\x1f\x16\xfb&\r\xc7"', 
                    b'\x0c8\xe5\xb7\x15\xfe\xc5\n,s\xe8\xf2z\xbe\x9eH\xc8\xe9}\x92\xc4C\xc8D\xf4D\x0e\x0f\xd1b\xdf\x81', 
                    b'\xa22\x9a\x07\x03d\x01~\xd4/\xaf\x9a\x19\xbd\xa0=\x035\xdf3\x00\xf1\xb5\xd5\x82\x9c\x85\xd1\xe9$\xff\xdd', 
                    b'\xd3\xdeI:\x86\x03\x83\xef\x1d\xb2\x94@\xfa5}\\\xd7mr*\xaa\xbd-\xc8\x0f\xb58KbrF\xa9', 
                    b'\xc36\xef\xc9\xce\xda\x94%\xc7\xb8f\xf2\xff\xdd0\xb9n8\r3O\xef\xf2\xad0C\xcdC\x1e\x91M\xfd', 
                    b'9}\xb4\xe8\x9e\xd2\xf5\x7f%\x92\x82u\xa7\x8d\xe7\xba\x9cq\xedX"J\x93&\x15D\x10\xa6\xf7\xeexn', 
                    b'\x08\xce\xc32\x1an\x83\xed{G[\xf0\x8dk\xc7:\xcd\t\xe3\xafD\xc8q\x86r!\xb0t\xea\xc1\xb25', 
                    b'\x948\x16\x06\x01ss\xc9\xd4\x8eEp\xc2.CV\x1ehv\xd9#\xef\xc9\xa0.?)\xda?\xea\x10\xc7', 
                    b'\xd7\xbe\xcb\xca\xa6M\xc4C\xa3\xe9m\x8d\xbb0|\x85\xcc\xe6\xa1\xf1\x8a\x90\x07\x0c\x87\x13\xb8\x92\xf1\xceK\xb3', 
                    b'R*q\x98\x87\xf6\r\\\x9652n\x1e\xb8\xc9RW\xfa\x0b)\xecA\xfd\x86\xc4\xbe\x87$\xdeV\xc7\x0c', 
                    b'\t\xc2\xd8\xa1Qw/\x19\x08+f7\x9fT\xbf\x16B\x07F\x7fbR\xa13\xb9\xbcs\xda\x8bE\x1c\xd9', 
                    b"\x9fc\xa5\xe7\xe4K\x08\xb6\xd4u\x9em\xe9W\x82z\xb2\xc0'\xbe\xcf\xb0\xb7\x9b&zJ\xa7\x19\xbf\x1b\xf6", 
                    b'\x18^\xe9*\x80\x9c\xee\xd6\xeb\xe1r1\x81\xe5c\xbd\x02\xb9\x12Ym\xca\xe9\x83\x16\xf7\xbb7\x9fv\xe6\x98', 
                    b"\x00\xe5e\xd5\xe6\x8d0\xba\xb1\xb5m<\x86E\xf5_'\xe4\xb1\xe7\x81\x08U\xcd\x9c8\xa4.\xbby6\xdd", 
                    b'3s\xc7\xcf\x94]L\xa4\xcc\xf0\xa5\xc2\xd8\xcdC\xcc\x16eS\xaa\xcej@\xd5\xb0\rw\x1d\x83\xae\xd5\r', 
                    b',\xfb#\x93\x9f\xa0\xae\xa3\xa1\xcc\xbaS0\x90>Bt@\xa9\x81\x91\xd4\x8e\x07bf9/\xec,\xecY', 
                    b'A\x88\x06\x173\xe0\xc3\xa2\x1b~U\xc9`\x88\x0bX\xbd\xda\\\xad\x0bu\xfbM[\x85\xf3qx\x88\xb6\xd5', 
                    b'&\xbf\xa5A\xb4\x9aLDk\\t\xbf\tC\xf0\x94\x0f \x1e)\xea+]\xd7\x85\xb14I~\x1cj\xb7', 
                    b'U\xac\x94\x80\x86\xea\xa4\xc0\xc9N\xf7k\xe5\x15\x91\xc2\xfa4\xa2\x82\xa9\x83\xc3\x925\xaef\x9b\xdfG\x9er', 
                    b'\x88\xef\xf0 \x84\x8f<Mjv\xf6C\xf1k\xb0\xdd\xb2sV\x7f\xa1\xf6fZ\xdbt\xa58"\xf00\xd5', 
                    b'\x0c\x81\xfeDsV\xf8DK2e\n\xcc\x8d\xf4\x04\xd6{\xd3\x8b7\xa2\x8a\xd2\x08\xa7k0J\x89~\xb2', 
                    b'[x\xd6\x01\xd40n\x91\x13(\xde\x04~\x90\xf4Ck\xb6\x17\xf7=\xb3\x0f\xea\xbd\xa6\x1f\x95\x17t\x99\xd2', 
                    b'd\x00\x18\x85n`\xfe\xf9\xc0g\xcb\x14\xf2\xedn\xc2}\x8d\x99\x17\x06\xba6\x0e8\xed\xc7)\xddcpV', 
                    b'F4\x9bf\x15\xe0\x1c\xb2\xdb\x11Q\xa7G\x06X?\xa4D6\xceE\x86l\xe2C\x02\xf2\xc9\x87,\xe3\xf8', 
                    b'\x13P\xeb\x8dK\xc8\xe9\xbc~\x17\x04?\x93`\x9a\xc3\xe1\xfc\x86;\t\xf0\x94\xca\xea\x8eR\xfbMb@~', 
                    b'\x86\xf8\x0bg\xd5\xe7`\xf6Iz\xd2T\xb6\x83\x81ls\x0b\x038\x11\xf9SHhK\xd2>\xbc\x15\xe3\xa9', 
                    b"4\xf0\x9c\xc2\xd2'ag*\xce\x10\xcad\x07\xabnpyml\xb4\xea\x03\xac>{\x03\xe4\xaa\x92l\xc4", 
                    b'\x1a\xcaE!\x1f\xe6d6\xd7r\x01\x19%\xc2B\x92\xfbh\x13Ox\x99\x9ck\xb7\x83\xbeC\xe4\xc9W=', 
                    b'\n\x15\x81\xa4]\xd1\xb7\x17\xed\x01m\xf8D\x840\x06\xb9\x08\x00\xa9h\xf5\x9f\x10|]\xb1\x9eX\x04{V']

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
        proof = Proof(target_key_hash=og_proof.target, proof_hash=og_proof.proof[:-1],
                    root_hash=og_proof.trie_root, type=og_proof.type)
        self.assertFalse(trie.verify_proof_of_exclusion(proof), 
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
        og_proof = trie.get_proof_of_exclusion(keccak_hash(rlp.encode(b'wolf')))
        proof = Proof(target_key_hash=og_proof.target, proof_hash=og_proof.proof + b'o',
                    root_hash=og_proof.trie_root, type=og_proof.type)
        self.assertFalse(trie.verify_proof_of_exclusion(proof), 
                        'Proof should not be valid.')


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

