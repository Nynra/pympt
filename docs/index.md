mpt
~~~~~
Python implementation of Merkle Patricia Trie.

:copyright: © 2019 by Igor Aleksanov.

:license: MIT, see LICENSE for more details.

<a id="mpt.__version__"></a>

#### \_\_version\_\_

<a id="mpt.MerklePatriciaTrie"></a>

## MerklePatriciaTrie

<a id="mpt.name"></a>

#### name

<a id="mpt.hash.keccak"></a>

## keccak

<a id="mpt.hash.keccak_hash"></a>

#### keccak\_hash

```python
def keccak_hash(data)
```

Hash data with keccak256 algorithm.

Parameters
----------
data : bytes
    Data to hash.

Returns
-------
bytes
    Hash of the data.

<a id="mpt.mpt.Enum"></a>

## Enum

<a id="mpt.mpt.keccak_hash"></a>

## keccak\_hash

<a id="mpt.mpt.NibblePath"></a>

## NibblePath

<a id="mpt.mpt.Node"></a>

## Node

<a id="mpt.mpt.Leaf"></a>

## Leaf

<a id="mpt.mpt.Extension"></a>

## Extension

<a id="mpt.mpt.Branch"></a>

## Branch

<a id="mpt.mpt.MerklePatriciaTrie"></a>

## MerklePatriciaTrie Objects

```python
class MerklePatriciaTrie()
```

This class represents a trie.

MerklePatriciaTrie works like a wrapper over provided storage. 
Storage must implement dict-like interface. Any data structure 
that implements `__getitem__` and `__setitem__` should be OK.

Attributes
----------
_storage: dict-like
    Data structure to store all the data of MPT.
_root: bytes
    (Optional) Root node (not root hash!) of the trie.
    If not provided, tree will be considered empty.
_secure: bool
    (Optional) In secure mode all the keys are hashed 
    using keccak256 internally.

Methods
-------
get(encoded_key)
    This method gets a value associtated with provided key.
update(encoded_key, encoded_value)
    This method updates a provided key-value pair into the trie.
delete(encoded_key)
    This method removes a value associtated with provided key.

<a id="mpt.mpt.MerklePatriciaTrie.__init__"></a>

#### \_\_init\_\_

```python
def __init__(storage, root=None, secure=False)
```

Create a new instance of MPT.

Parameters
----------
storage: dict-like
    Data structure to store all the data of MPT.
root: bytes
    (Optional) Root node (not root hash!) of the trie. 
    If not provided, tree will be considered empty.
secure: bool
    (Optional) In secure mode all the keys are hashed using keccak256 internally.

<a id="mpt.mpt.MerklePatriciaTrie.root"></a>

#### root

```python
def root()
```

Return a root node of the trie. 

Returns
-------
Node
    Root node of the trie. Type is `bytes` if trie isn't empty and `None` otherwise.

<a id="mpt.mpt.MerklePatriciaTrie.root_hash"></a>

#### root\_hash

```python
def root_hash()
```

Returns a hash of the trie's root node. 

For empty trie it's the hash of the RLP-encoded empty string. 

Returns
-------
bytes
    Hash of the trie's root node.

<a id="mpt.mpt.MerklePatriciaTrie.get"></a>

#### get

```python
def get(encoded_key)
```

This method gets a value associtated with provided key.

Note: this method does not RLP-encode the key. 
If you use encoded keys, you should encode it yourself.

Parameters
----------
encoded_key: bytes
    RLP-encoded key.

Returns
-------
bytes
    Stored value associated with provided key.

Raises
------
KeyError
    KeyError is raised if there is no value assotiated with provided key.

<a id="mpt.mpt.MerklePatriciaTrie.get_node"></a>

#### get\_node

```python
def get_node(encoded_key)
```

This method gets a node from storage.

Parameters
----------
node_ref: bytes
    Reference to the node.

Returns
-------
Node
    Node from storage.

<a id="mpt.mpt.MerklePatriciaTrie.update"></a>

#### update

```python
def update(encoded_key, encoded_value)
```

This method updates a provided key-value pair into the trie.

If there is no such a key in the trie, a new entry will be created.
Otherwise value associtaed with key is updated.
Note: this method does not RLP-encode neither key or value. 
If you use encoded keys, you should encode it yourself.

Parameters
----------
encoded_key: bytes
    RLP-encoded key.
encoded_value: bytes
    RLP-encoded value.

<a id="mpt.mpt.MerklePatriciaTrie.delete"></a>

#### delete

```python
def delete(encoded_key)
```

This method removes a value associtated with provided key.

Note: this method does not RLP-encode the key. 
If you use encoded keys, you should encode it yourself.

Parameters
----------
encoded_key: bytes
    RLP-encoded key.

Raises
------
KeyError
    KeyError is raised if there is no value assotiated with provided key.

<a id="mpt.mpt.MerklePatriciaTrie.get_proof_of_inclusion"></a>

#### get\_proof\_of\_inclusion

```python
def get_proof_of_inclusion(encoded_key)
```

This method returns a proof of inclusion for a key.
Proof is a list of nodes that are necessary to reconstruct the trie.
Note: this method does not RLP-encode the key. 
If you use encoded keys, you should encode it yourself.

<a id="mpt.mpt.MerklePatriciaTrie.verify_proof_of_inclusion"></a>

#### verify\_proof\_of\_inclusion

```python
def verify_proof_of_inclusion(encoded_key, proof)
```

This method verifies a proof of inclusion for a key.
Note: this method does not RLP-encode the key. 
If you use encoded keys, you should encode it yourself.

<a id="mpt.mpt.MerklePatriciaTrie._get_node"></a>

#### \_get\_node

```python
def _get_node(node_ref)
```

This method gets a node from storage.

Parameters
----------
node_ref: bytes
    Reference to the node.

Returns
-------
Node
    Node from storage.

<a id="mpt.mpt.MerklePatriciaTrie._get"></a>

#### \_get

```python
def _get(node_ref, path)
```

Get support method.

Returns a value associated with provided key.

Parameters
----------
node_ref: bytes
    Reference to a node.
path: NibblePath
    Path to a value.

Returns
-------
bytes
    Value associated with provided key.

Raises
------
KeyError
    KeyError is raised if there is no value assotiated with provided key.

<a id="mpt.mpt.MerklePatriciaTrie._get_proof_of_inclusion"></a>

#### \_get\_proof\_of\_inclusion

```python
def _get_proof_of_inclusion(node_ref, path)
```

Get proof of inclusion support method.

Used to iterate over the trie and get a proof of inclusion for a node ref.

Parameters
----------
node_ref: bytes
    Reference to a node.
path: NibblePath
    Path to a value.

Returns
-------
bytes
    Raw node associated with provided key.

Raises
------
KeyError
    KeyError is raised if there is no node assotiated with provided key.

<a id="mpt.mpt.MerklePatriciaTrie._verify_proof_of_inclusion"></a>

#### \_verify\_proof\_of\_inclusion

```python
def _verify_proof_of_inclusion(node_ref, path, proof)
```

Verify proof of inclusion support method.

Used to iterate over the trie and verify a proof of inclusion for a node ref.

Parameters
----------
node_ref: bytes
    Reference to a node.
path: NibblePath
    Path to a value.
proof: list of bytes
    Proof of inclusion.

Returns
-------
bool
    True if the proof is valid, False otherwise.

Raises
------
KeyError
    KeyError is raised if there is no node assotiated with provided key.

<a id="mpt.mpt.MerklePatriciaTrie._update"></a>

#### \_update

```python
def _update(node_ref, path, value)
```

Update support method.

Updates a value associated with provided key.

Parameters
----------
node_ref: bytes
    Reference to a node.
path: NibblePath
    Path to a value.
value: bytes
    Value to be stored.

Returns
-------
bytes
    New root of the trie.

Raises
------
KeyError
    KeyError is raised if there is no value assotiated with provided key.

<a id="mpt.mpt.MerklePatriciaTrie._create_branch_node"></a>

#### \_create\_branch\_node

```python
def _create_branch_node(path_a, value_a, path_b, value_b)
```

Create a branch node with up to two leaves and maybe value. 

Parameters
----------
path_a: NibblePath
    Path to a leaf.
value_a: bytes
    Value to be stored in a leaf.
path_b: NibblePath
    Path to a leaf.
value_b: bytes
    Value to be stored in a leaf.

Returns
-------
bytes
    Reference to created node.

<a id="mpt.mpt.MerklePatriciaTrie._create_branch_leaf"></a>

#### \_create\_branch\_leaf

```python
def _create_branch_leaf(path, value, branches)
```

If path isn't empty, creates leaf node and stores reference in appropriate branch.

Parameters
----------
path: NibblePath
    Path to a leaf.
value: bytes
    Value to be stored in a leaf.
branches: list of bytes
    List of references to nodes.

Returns
-------
None

<a id="mpt.mpt.MerklePatriciaTrie._create_branch_extension"></a>

#### \_create\_branch\_extension

```python
def _create_branch_extension(path, next_ref, branches)
```

If needed, create an extension node and stores reference in appropriate branch.
Otherwise just stores provided reference.

Parameters
----------
path: NibblePath
    Path to an extension node.
next_ref: bytes
    Reference to a node.
branches: list of bytes
    List of references to nodes.

Returns
-------
None

<a id="mpt.mpt.MerklePatriciaTrie._store_node"></a>

#### \_store\_node

```python
def _store_node(node)
```

Build the reference from the node and if needed saves node in the storage.

Parameters
----------
node: Node
    Node to be stored.

Returns
-------
bytes
    Reference to the node.

<a id="mpt.mpt.MerklePatriciaTrie._DeleteAction"></a>

## \_DeleteAction Objects

```python
class _DeleteAction(Enum)
```

Enum that shows which action was performed on the previous step of the deletion.

<a id="mpt.mpt.MerklePatriciaTrie._DeleteAction.DELETED"></a>

#### DELETED

<a id="mpt.mpt.MerklePatriciaTrie._DeleteAction.UPDATED"></a>

#### UPDATED

<a id="mpt.mpt.MerklePatriciaTrie._DeleteAction.USELESS_BRANCH"></a>

#### USELESS\_BRANCH

<a id="mpt.mpt.MerklePatriciaTrie._delete"></a>

#### \_delete

```python
def _delete(node_ref, path)
```

Delete method helper.

Parameters
----------
node_ref: bytes
    Reference to the node.
path: NibblePath
    Path to the node.

Returns
-------
_DeleteAction
    Action that was performed on the previous step of the deletion.

<a id="mpt.mpt.MerklePatriciaTrie._build_new_node_from_last_branch"></a>

#### \_build\_new\_node\_from\_last\_branch

```python
def _build_new_node_from_last_branch(branches)
```

Combine nibble of the only branch left with underlying node and creates new node.

Parameters
----------
branches : list of bytes
    List of references to the branches.

Returns
-------
tuple
    Tuple of `_DeleteAction` and reference to the new node.

Raises
------
KeyError
    If there is no branches left.

<a id="mpt.nibble_path.NibblePath"></a>

## NibblePath Objects

```python
class NibblePath()
```

Class to represent the nibble path as a linked list.

Class variables
----------------
ODD_FLAG : int
    Flag to indicate that the path has odd length.
LEAF_FLAG : int
    Flag to indicate that the path is a leaf.

Methods
-------
__len__()
    Returns the length of the path.
__repr__()
    Returns a string representation of the path.
__str__()
    Returns a string representation of the path.
__eq__()
    Checks if two paths are equal.
at(idx)
    Returns nibble at the certain position.
consume(amount)
    Cuts off nibbles at the beginning of the path.
combine(other)
    Combines two paths.
starts_with(other)
    Checks if `other` is prefix of `self`.
common_prefix_with(other)
    Returns the common prefix of two paths.

Static methods
--------------
encode(path)
    Encodes NibblePath to raw bytes.
decode_with_type(data)
    Decode the NibblePath and its type from raw bytes.
decode(data)
    Decodes NibblePath without its type from raw bytes.

<a id="mpt.nibble_path.NibblePath.ODD_FLAG"></a>

#### ODD\_FLAG

<a id="mpt.nibble_path.NibblePath.LEAF_FLAG"></a>

#### LEAF\_FLAG

<a id="mpt.nibble_path.NibblePath.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data, offset=0)
```

Initiates NibblePath with raw bytes and an offset.

Offset is the number of nibbles that are skipped at the beginning of the path.
If offset is odd, first nibble is skipped. If offset is even, first two nibbles are skipped.
If offset is 0, no nibbles are skipped, if the offset is -1, the last nibble is skipped, etc.

Parameters
----------
data : bytes
    Raw bytes of the path.
offset : int
    Offset of the path.

<a id="mpt.nibble_path.NibblePath.__len__"></a>

#### \_\_len\_\_

```python
def __len__()
```

Return the length of the path.

<a id="mpt.nibble_path.NibblePath.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__()
```

Return a string representation of the path.

Returns the data in hex format and the offset.

<a id="mpt.nibble_path.NibblePath.__str__"></a>

#### \_\_str\_\_

```python
def __str__()
```

Return a string representation of the path.

Returns the data in hex format and the raw data.

<a id="mpt.nibble_path.NibblePath.__eq__"></a>

#### \_\_eq\_\_

```python
def __eq__(other)
```

Check if two paths are equal.

Parameters
----------
other : NibblePath
    Other path to compare with.

Returns
-------
bool
    True if paths are equal, False otherwise.

<a id="mpt.nibble_path.NibblePath.decode_with_type"></a>

#### decode\_with\_type

```python
@staticmethod
def decode_with_type(data)
```

Decode the NibblePath and its type from raw bytes.

Parameters
----------
data : bytes
    Raw bytes of the path.

Returns
-------
tuple
    Tuple of NibblePath and its type.

<a id="mpt.nibble_path.NibblePath.decode"></a>

#### decode

```python
@staticmethod
def decode(data)
```

Decodes NibblePath without its type from raw bytes.

Parameters
----------
data : bytes
    Raw bytes of the path.

Returns
-------
NibblePath
    Decoded path.

<a id="mpt.nibble_path.NibblePath.starts_with"></a>

#### starts\_with

```python
def starts_with(other)
```

Checks if `other` is prefix of `self`.

Parameters
----------
other : NibblePath
    Prefix to check.

Returns
-------
bool
    True if `other` is prefix of `self`, False otherwise.

<a id="mpt.nibble_path.NibblePath.at"></a>

#### at

```python
def at(idx)
```

Returns nibble at the certain position.

Parameters
----------
idx : int
    Position of the nibble.

Returns
-------
int
    Nibble at the certain position.

<a id="mpt.nibble_path.NibblePath.consume"></a>

#### consume

```python
def consume(amount)
```

Cuts off nibbles at the beginning of the path.

Parameters
----------
amount : int
    Number of nibbles to cut off.

Returns
-------
NibblePath
    New path with cut off nibbles.

<a id="mpt.nibble_path.NibblePath._create_new"></a>

#### \_create\_new

```python
def _create_new(path, length)
```

Creates a new NibblePath from a given object with a certain length.

Parameters
----------
path : object
    Object to create a new NibblePath from.
length : int
    Length of the new NibblePath.

Returns
-------
NibblePath
    New NibblePath.

<a id="mpt.nibble_path.NibblePath.common_prefix"></a>

#### common\_prefix

```python
def common_prefix(other)
```

Returns common part at the beginning of both paths.

Parameters
----------
other : NibblePath
    Other path to compare with.

Returns
-------
NibblePath
    Common part at the beginning of both paths.

<a id="mpt.nibble_path.NibblePath.encode"></a>

#### encode

```python
def encode(is_leaf)
```

Encodes NibblePath into bytes.

Encoded path contains prefix with flags of type and length and also may contain a padding nibble
so the length of encoded path is always even.

Parameters
----------
is_leaf : bool
    True if the path is a leaf, False otherwise.

Returns
-------
bytes
    Encoded path.

<a id="mpt.nibble_path.NibblePath._Chained"></a>

## \_Chained Objects

```python
class _Chained()
```

Class that chains two paths.

<a id="mpt.nibble_path.NibblePath._Chained.__init__"></a>

#### \_\_init\_\_

```python
def __init__(first, second)
```

Initializes the chained paths.

Parameters
----------
first : NibblePath
    First path.
second : NibblePath
    Second path.

<a id="mpt.nibble_path.NibblePath._Chained.__len__"></a>

#### \_\_len\_\_

```python
def __len__()
```

Return the length of the chained paths.

<a id="mpt.nibble_path.NibblePath._Chained.at"></a>

#### at

```python
def at(idx)
```

Return the nibble at the certain position.

Parameters
----------
idx : int
    Position of the nibble.

Returns
-------
int
    Nibble at the certain position.

<a id="mpt.nibble_path.NibblePath.combine"></a>

#### combine

```python
def combine(other)
```

Merges two paths into one.

Parameters
----------
other : NibblePath
    Other path to merge with.

Returns
-------
NibblePath
    Merged path.

<a id="mpt.node.rlp"></a>

## rlp

<a id="mpt.node.NibblePath"></a>

## NibblePath

<a id="mpt.node.keccak_hash"></a>

## keccak\_hash

<a id="mpt.node._prepare_reference_for_usage"></a>

#### \_prepare\_reference\_for\_usage

```python
def _prepare_reference_for_usage(ref)
```

Encode the reference into RLP if needed so stored references will appear as bytes.

Parameters
----------
ref : bytes or bytearray
    Reference to encode.

Returns
-------
bytes or bytearray
    Encoded reference.

<a id="mpt.node._prepare_reference_for_encoding"></a>

#### \_prepare\_reference\_for\_encoding

```python
def _prepare_reference_for_encoding(ref)
```

Decode the RLP-encoded reference if needed so the full node will be encoded correctly.

Parameters
----------
ref : bytes or bytearray
    Reference to decode.

Returns
-------
bytes or bytearray
    Decoded reference.

<a id="mpt.node.Node"></a>

## Node Objects

```python
class Node()
```

Node class.

<a id="mpt.node.Node.EMPTY_HASH"></a>

#### EMPTY\_HASH

<a id="mpt.node.Node.decode"></a>

#### decode

```python
def decode(encoded_data)
```

Decode the node from RLP.

Parameters
----------
encoded_data : bytes or bytearray
    Encoded node.

Returns
-------
Node
    Decoded node.

<a id="mpt.node.Node.into_reference"></a>

#### into\_reference

```python
def into_reference(node)
```

Returns reference to the given node.

If length of encoded node is less than 32 bytes, the reference is encoded node itseld (In-place reference).
Otherwise reference is keccak hash of encoded node.

Parameters
----------
node : Node
    Node to get reference for.

Returns
-------
bytes or bytearray

<a id="mpt.node.Leaf"></a>

## Leaf Objects

```python
class Leaf(Node)
```

Leaf class for the mpt tree.

The leaf class is used to store data in the tree and is the end of a path.

Attributes
----------
path : NibblePath
    Path to the data.
data : bytes
    Data to store.

Methods
-------
encode()
    Encodes the leaf into RLP.

<a id="mpt.node.Leaf.__init__"></a>

#### \_\_init\_\_

```python
def __init__(path, data)
```

Initializes the leaf.

Parameters
----------
path : NibblePath
    Path to the data.
data : bytes
    Data to store.

<a id="mpt.node.Leaf.encode"></a>

#### encode

```python
def encode(include_data=True)
```

Encodes the leaf into RLP.

Returns
-------
bytes
    Encoded leaf.

<a id="mpt.node.Extension"></a>

## Extension Objects

```python
class Extension(Node)
```

Extension class for the mpt tree.

The extension class is used to store references to other nodes in the tree and is the middle of a path.

Attributes
----------
path : NibblePath
    Path to the node.
ref : bytes or bytearray
    Reference to the node.

Methods
-------
encode()
    Encodes the extension into RLP.

<a id="mpt.node.Extension.__init__"></a>

#### \_\_init\_\_

```python
def __init__(path, next_ref)
```

Initializes the extension.

Parameters
----------
path : NibblePath
    Path to the node.
next_ref : bytes or bytearray
    Reference to the next node.

<a id="mpt.node.Extension.encode"></a>

#### encode

```python
def encode(include_data=True)
```

Encodes the extension into RLP.

Parameters
----------
include_data : bool
    Include the reference to the next node.

Returns
-------
bytes
    Encoded extension.

<a id="mpt.node.Branch"></a>

## Branch Objects

```python
class Branch(Node)
```

Branch class for the mpt tree.

The branch class is used to store references to other nodes in the tree and is the middle of a path.
It is also used to store data in the tree.

<a id="mpt.node.Branch.__init__"></a>

#### \_\_init\_\_

```python
def __init__(branches, data=None)
```

Initializes the branch.

Parameters
----------
branches : list of bytes or bytearray
    References to the nodes.
data : bytes or bytearray
    Data to store.

<a id="mpt.node.Branch.encode"></a>

#### encode

```python
def encode(include_data=True)
```

Encodes the branch into RLP.

Returns
-------
bytes
    Encoded branch.

<a id="mpt.proof.Node"></a>

## Node

<a id="mpt.proof.Leaf"></a>

## Leaf

<a id="mpt.proof.Extension"></a>

## Extension

<a id="mpt.proof.MPT"></a>

## MPT

<a id="mpt.proof.NibblePath"></a>

## NibblePath

<a id="mpt.proof.Proof"></a>

## Proof Objects

```python
class Proof()
```

Child class for the mpt proof of inclusion.

This class only contains static methods.

Methods
-------
proof_of_inclusion(mpt, key)
    Returns the proof of inclusion for the key.
verify_proof_of_inclusion(mpt, key, proof)
    Verifies the proof of inclusion for the key.

<a id="mpt.proof.Proof.proof_of_inclusion"></a>

#### proof\_of\_inclusion

```python
@staticmethod
def proof_of_inclusion(trie, key)
```

Proof of inclusion for a key in the trie.

Parameters
----------
trie : MPT
    MPT to get the proof of inclusion from.
key : bytes
    Key to get the proof of inclusion for.

Returns
-------
list of bytes
    Proof of inclusion for the key.

<a id="mpt.proof.Proof.verify_proof_of_inclusion"></a>

#### verify\_proof\_of\_inclusion

```python
@staticmethod
def verify_proof_of_inclusion(trie,
                              key,
                              proof,
                              check_duplicates=True,
                              raise_on_error=False)
```

Verify the proof of inclusion for a key in the trie.

Parameters
----------
trie : MPT
    MPT to verify the proof of inclusion in.
key : bytes
    Key to verify the proof of inclusion for.
proof : list of bytes
    Proof of inclusion for the key.
check_duplicates : bool
    Check for duplicate nodes in the proof.
raise_on_error : bool
    Raise an exception if the proof is invalid.

Returns
-------
bool
    True if the proof is valid, False otherwise.

