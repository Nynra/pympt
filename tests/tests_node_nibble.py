import sys, os
try:
    from mpt import MerklePatriciaTrie
    from mpt.nibble_path import NibblePath
    from mpt.node import Node, Leaf
except (ImportError, ModuleNotFoundError):
    #Following lines are for assigning parent directory dynamically.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.insert(0, parent_dir_path)
    from src.mpt.nibble_path import NibblePath
    from src.mpt.node import Node, Leaf
import unittest
import rlp
import random


class TestNibblePath(unittest.TestCase):
    def test_at(self):
        nibbles = NibblePath([0x12, 0x34])
        self.assertEqual(nibbles.at(0), 0x1)
        self.assertEqual(nibbles.at(1), 0x2)
        self.assertEqual(nibbles.at(2), 0x3)
        self.assertEqual(nibbles.at(3), 0x4)

    def test_at_with_offset(self):
        nibbles = NibblePath([0x12, 0x34], offset=1)
        self.assertEqual(nibbles.at(0), 0x2)
        self.assertEqual(nibbles.at(1), 0x3)
        self.assertEqual(nibbles.at(2), 0x4)
        with self.assertRaises(IndexError):
            nibbles.at(3)

    def test_encode(self):
        nibbles = NibblePath([0x12, 0x34])
        self.assertEqual(nibbles.encode(False), b'\x00\x12\x34')
        self.assertEqual(nibbles.encode(True), b'\x20\x12\x34')

        nibbles = NibblePath([0x12, 0x34], offset=1)
        self.assertEqual(nibbles.encode(False), b'\x12\x34')
        self.assertEqual(nibbles.encode(True), b'\x32\x34')

    def test_common_prefix(self):
        nibbles_a = NibblePath([0x12, 0x34])
        nibbles_b = NibblePath([0x12, 0x56])
        common = nibbles_a.common_prefix(nibbles_b)
        self.assertEqual(common, NibblePath([0x12]))

        nibbles_a = NibblePath([0x12, 0x34])
        nibbles_b = NibblePath([0x12, 0x36])
        common = nibbles_a.common_prefix(nibbles_b)
        self.assertEqual(common, NibblePath([0x01, 0x23], offset=1))

        nibbles_a = NibblePath([0x12, 0x34], offset=1)
        nibbles_b = NibblePath([0x12, 0x56], offset=1)
        common = nibbles_a.common_prefix(nibbles_b)
        self.assertEqual(common, NibblePath([0x12], offset=1))

        nibbles_a = NibblePath([0x52, 0x34])
        nibbles_b = NibblePath([0x02, 0x56])
        common = nibbles_a.common_prefix(nibbles_b)
        self.assertEqual(common, NibblePath([]))

    def test_combine(self):
        nibbles_a = NibblePath([0x12, 0x34])
        nibbles_b = NibblePath([0x56, 0x78])
        common = nibbles_a.combine(nibbles_b)
        self.assertEqual(common, NibblePath([0x12, 0x34, 0x56, 0x78]))

        nibbles_a = NibblePath([0x12, 0x34], offset=1)
        nibbles_b = NibblePath([0x56, 0x78], offset=3)
        common = nibbles_a.combine(nibbles_b)
        self.assertEqual(common, NibblePath([0x23, 0x48]))


class TestNode(unittest.TestCase):
    def assertRoundtrip(self, raw_node, expected_type):
        decoded = Node.decode(raw_node)
        encoded = decoded.encode()

        self.assertEqual(type(decoded), expected_type)
        self.assertEqual(raw_node, encoded)

    def test_leaf(self):
        # Path 0xABC. 0x3_ at the beginning: 0x20 (for leaf type) + 0x10 (for odd len)
        nibbles_path = bytearray([0x3A, 0xBC])
        data = bytearray([0xDE, 0xAD, 0xBE, 0xEF])
        raw_node = rlp.encode([nibbles_path, data])
        self.assertRoundtrip(raw_node, Leaf)





if __name__ == '__main__':
    unittest.main()
