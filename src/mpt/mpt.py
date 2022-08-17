from enum import Enum
from .hash import keccak_hash
from .nibble_path import NibblePath
from .node import Node, Leaf, Extension, Branch


class MerklePatriciaTrie:
    """
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
    """

    def __init__(self, storage, root=None, secure=False):
        """
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
        """
        self._storage = storage
        self._root = root
        self._secure = secure

    def root(self):
        """
        Return a root node of the trie. 
        
        Returns
        -------
        Node
            Root node of the trie. Type is `bytes` if trie isn't empty and `None` otherwise. 
        """
        return self._root

    def root_hash(self):
        """
        Returns a hash of the trie's root node. 
        
        For empty trie it's the hash of the RLP-encoded empty string. 

        Returns
        -------
        bytes
            Hash of the trie's root node. 
        """

        if not self._root:
            return Node.EMPTY_HASH
        elif len(self._root) == 32:
            return self._root
        else:
            return keccak_hash(self._root)

    def get(self, encoded_key):
        """
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
        """
        if not self._root:
            raise KeyError

        if self._secure:
            encoded_key = keccak_hash(encoded_key)

        path = NibblePath(encoded_key)

        result_node = self._get(self._root, path)

        return result_node.data

    # Get a Node from the storage.
    def get_node(self, encoded_key):
        """
        This method gets a node from storage.
        
        Parameters
        ----------
        node_ref: bytes
            Reference to the node.
        
        Returns
        -------
        Node
            Node from storage.
        """
        if not self._root:
            raise KeyError

        if self._secure:
            encoded_key = keccak_hash(encoded_key)

        path = NibblePath(encoded_key)

        # result_node = self._get(self._root, path)
        # return result_node
        return self._get(self._root, path)

    def update(self, encoded_key, encoded_value):
        """
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
        """
        if self._secure:
            encoded_key = keccak_hash(encoded_key)

        path = NibblePath(encoded_key)

        result = self._update(self._root, path, encoded_value)

        self._root = result

    def delete(self, encoded_key):
        """
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
        """

        if self._root is None:
            return

        if self._secure:
            encoded_key = keccak_hash(encoded_key)

        path = NibblePath(encoded_key)

        action, info = self._delete(self._root, path)

        if action == MerklePatriciaTrie._DeleteAction.DELETED:
            # Trie is empty
            self._root = None
        elif action == MerklePatriciaTrie._DeleteAction.UPDATED:
            new_root = info
            self._root = new_root
        elif action == MerklePatriciaTrie._DeleteAction.USELESS_BRANCH:
            _, new_root = info
            self._root = new_root

    def _get_node(self, node_ref):
        """
        This method gets a node from storage.
        
        Parameters
        ----------
        node_ref: bytes
            Reference to the node.
        
        Returns
        -------
        Node
            Node from storage.
        """
        raw_node = None
        if len(node_ref) == 32:
            raw_node = self._storage[node_ref]
        else:
            raw_node = node_ref

        return Node.decode(raw_node)

    def _get(self, node_ref, path):
        """
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
        
        """
        node = self._get_node(node_ref)

        # If path is empty, our travel is over. Main `get` method 
        # will check if this node has a value.
        if len(path) == 0:
            return node

        if type(node) is Leaf:
            # If we've found a leaf, it's either the leaf we're 
            # looking for or wrong leaf.
            if node.path == path:
                return node

        elif type(node) is Extension:
            # If we've found an extension, we need to go deeper.
            if path.starts_with(node.path):
                rest_path = path.consume(len(node.path))
                return self._get(node.next_ref, rest_path)

        elif type(node) is Branch:
            # If we've found a branch node, go to the appropriate branch.
            branch = node.branches[path.at(0)]
            if len(branch) > 0:
                return self._get(branch, path.consume(1))

        # Raise error if it's a wrong node, extension with different 
        # path or branch node without appropriate branch.
        # TODO: #5 Raise errors with a proper message.
        raise KeyError

    def _update(self, node_ref, path, value):
        """
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
            
        """
        if not node_ref:
            return self._store_node(Leaf(path, value))

        node = self._get_node(node_ref)

        if type(node) == Leaf:
            # If we're updating the leaf there are 2 possible ways:
            # 1. Path is equals to the rest of the key. Then we should 
            #    just update value of this leaf.
            # 2. Path differs. Then we should split this node into several nodes.

            if node.path == path:
                # Path is the same. Just change the value.
                node.data = value
                return self._store_node(node)

            # If we are here, we have to split the node.

            # Find the common part of the key and leaf's path.
            common_prefix = path.common_prefix(node.path)

            # Cut off the common part.
            path.consume(len(common_prefix))
            node.path.consume(len(common_prefix))

            # Create branch node to split paths.
            branch_reference = self._create_branch_node(path, value, 
                                            node.path, node.data)

            # If common part isn't empty, we have to create an extension node before branch node.
            # Otherwise, we need just branch node.
            if len(common_prefix) != 0:
                return self._store_node(Extension(common_prefix, 
                                                       branch_reference))
            else:
                return branch_reference

        elif type(node) == Extension:
            # If we're updating an extenstion there are 2 possible ways:
            # 1. Key starts with the extension node's path. 
            #    Then we just go ahead and all the work will be done there.
            # 2. Key doesn't start with extension node's path. Then we have to split extension node.

            if path.starts_with(node.path):
                # Just go ahead.
                new_reference = self._update(node.next_ref, path.consume(len(node.path)), value)
                return self._store_node(Extension(node.path, new_reference))

            # Split extension node.

            # Find the common part of the key and extension's path.
            common_prefix = path.common_prefix(node.path)

            # Cut off the common part.
            path.consume(len(common_prefix))
            node.path.consume(len(common_prefix))

            # Create an empty branch node. It may have or have not the value depending on the length
            # of the rest of the key.
            branches = [b''] * 16
            branch_value = value if len(path) == 0 else b''

            # If needed, create leaf branch for the value we're inserting.
            self._create_branch_leaf(path, value, branches)
            # If needed, create an extension node for the rest of the extension's path.
            self._create_branch_extension(node.path, node.next_ref, branches)

            branch_reference = self._store_node(Branch(branches, branch_value))

            # If common part isn't empty, we have to create an extension node before branch node.
            # Otherwise, we need just branch node.
            if len(common_prefix) != 0:
                return self._store_node(Extension(common_prefix, branch_reference))
            else:
                return branch_reference

        elif type(node) == Branch:
            # For branch node things are easy.
            # 1. If key is empty, just store value in this node.
            # 2. If key isn't empty, just call `_update` with appropiate branch reference.

            if len(path) == 0:
                return self._store_node(Branch(node.branches, value))

            idx = path.at(0)
            new_reference = self._update(node.branches[idx], path.consume(1), value)

            node.branches[idx] = new_reference

            return self._store_node(node)

    def _create_branch_node(self, path_a, value_a, path_b, value_b):
        """ 
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
        """

        assert len(path_a) != 0 or len(path_b) != 0

        branches = [b''] * 16

        branch_value = b''
        if len(path_a) == 0:
            branch_value = value_a
        elif len(path_b) == 0:
            branch_value = value_b

        self._create_branch_leaf(path_a, value_a, branches)
        self._create_branch_leaf(path_b, value_b, branches)

        return self._store_node(Branch(branches, branch_value))

    def _create_branch_leaf(self, path, value, branches):
        """
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
        
        """
        if len(path) > 0:
            idx = path.at(0)

            leaf_ref = self._store_node(Leaf(path.consume(1), value))
            branches[idx] = leaf_ref

    def _create_branch_extension(self, path, next_ref, branches):
        """
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

        """
        assert len(path) >= 1, "Path for extension node should contain at least one nibble"

        if len(path) == 1:
            branches[path.at(0)] = next_ref
        else:
            idx = path.at(0)
            reference = self._store_node(Extension(path.consume(1), next_ref))
            branches[idx] = reference

    def _store_node(self, node):
        """
        Build the reference from the node and if needed saves node in the storage.
        
        Parameters
        ----------
        node: Node
            Node to be stored.
        
        Returns
        -------
        bytes
            Reference to the node.
        """
        reference = Node.into_reference(node)
        if len(reference) == 32:
            self._storage[reference] = node.encode()
        return reference

    class _DeleteAction(Enum):
        """
        Enum that shows which action was performed on the previous step of the deletion.
        """
        # Node was deleted. Returned value should be (_DeleteAction, None).
        DELETED = 1,
        # Node was updated. Returned value should be (_DeleteAction, new_node_reference)
        UPDATED = 2,
        # Branch became useless. Returned value should be 
        # (_DeleteAction, (path_to_new_reference, new_node_reference))
        USELESS_BRANCH = 3

    def _delete(self, node_ref, path):
        """
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
        
        """

        node = self._get_node(node_ref)

        if type(node) == Leaf:
            # If it's leaf node, then it's either node we need or incorrect key provided.
            if path == node.path:
                return MerklePatriciaTrie._DeleteAction.DELETED, None
            else:
                raise KeyError

        elif type(node) == Extension:
            # Extension node can't be removed directly, it passes delete request to the next node.
            # After that several options are possible:
            # 1. Next node was deleted. Then this node should be deleted too.
            # 2. Next node was updated. Then we should update stored reference.
            # 3. Next node was useless branch. Then we have to update our node depending on the next node type.

            if not path.starts_with(node.path):
                raise KeyError

            action, info = self._delete(node.next_ref, path.consume(len(node.path)))

            if action == MerklePatriciaTrie._DeleteAction.DELETED:
                # Next node was deleted. This node should be deleted also.
                return action, None
            elif action == MerklePatriciaTrie._DeleteAction.UPDATED:
                # Next node was updated. Update this node too.
                child_ref = info
                new_ref = self._store_node(Extension(node.path, child_ref))
                return action, new_ref
            elif action == MerklePatriciaTrie._DeleteAction.USELESS_BRANCH:
                # Next node was useless branch.
                stored_path, stored_ref = info

                child = self._get_node(stored_ref)

                new_node = None
                if type(child) == Leaf:
                    # If next node is the leaf, our node is unnecessary.
                    # Concat our path with leaf path and return reference to the leaf.
                    path = NibblePath.combine(node.path, child.path)
                    new_node = Leaf(path, child.data)
                elif type(child) == Extension:
                    # If next node is the extension, merge this and next node into one.
                    path = NibblePath.combine(node.path, child.path)
                    new_node = Extension(path, child.next_ref)
                elif type(child) == Branch:
                    # If next node is the branch, concatenate paths and update stored reference.
                    path = NibblePath.combine(node.path, stored_path)
                    new_node = Extension(path, stored_ref)

                new_reference = self._store_node(new_node)
                return MerklePatriciaTrie._DeleteAction.UPDATED, new_reference

        elif type(node) == Branch:
            # For branch node things are quite complicated.
            # If rest of the key is empty and there is stored value, just clear value field.
            # Otherwise call _delete for the appropriate branch.
            # At this step we will have delete action and (possibly) index of the branch we're working with.
            #
            # Then, if next node was updated or was useless branch, just update reference.
            # If `_DeleteAction` is `DELETED` then either the next node or value of this node was removed.
            # We have to check if there is at least 2 branches or 1 branch and value still persist in this node.
            # If there are no branches and no value left, delete this node completely.
            # If there is a value but no branches, create leaf node with value and empty path
            # and return `USELESS_BRANCH` action.
            # If there is an only branch and no value, merge nibble of this branch and path of the underlying node
            # and return `USELESS_BRANCH` action.
            # Otherwise our branch isn't useless and was updated.

            action = None
            idx = None
            info = None

            assert len(path) != 0 or len(node.data) != 0, "Empty path or empty branch node in _delete"

            # Decide if we need to remove value of this node or go deeper.
            if len(path) == 0 and len(node.data) == 0:
                # This branch node has no value thus we can't delete it.
                raise KeyError
            elif len(path) == 0 and len(node.data) != 0:
                node.data = b''
                action = MerklePatriciaTrie._DeleteAction.DELETED
            else:
                # Store idx of the branch we're working with.
                idx = path.at(0)

                if len(node.branches[idx]) == 0:
                    raise KeyError

                action, info = self._delete(node.branches[idx], path.consume(1))
                node.branches[idx] = b''

            if action == MerklePatriciaTrie._DeleteAction.DELETED:
                non_empty_count = sum(map(lambda x: 1 if len(x) > 0 else 0, node.branches))

                if non_empty_count == 0 and len(node.data) == 0:
                    # Branch node is empty, just delete it.
                    return MerklePatriciaTrie._DeleteAction.DELETED, None
                elif non_empty_count == 0 and len(node.data) != 0:
                    # No branches, just value.
                    path = NibblePath([])
                    reference = self._store_node(Leaf(path, node.data))

                    return MerklePatriciaTrie._DeleteAction.USELESS_BRANCH, (path, reference)
                elif non_empty_count == 1 and len(node.data) == 0:
                    # No value and one branch
                    return self._build_new_node_from_last_branch(node.branches)
                else:
                    # Branch has value and 1+ branches or no value and 2+ branches.
                    # It isn't useless, so action is `UPDATED`.
                    reference = self._store_node(node)
                    return MerklePatriciaTrie._DeleteAction.UPDATED, reference
            elif action == MerklePatriciaTrie._DeleteAction.UPDATED:
                # Just update reference.
                next_ref = info
                node.branches[idx] = next_ref
                reference = self._store_node(node)
                return MerklePatriciaTrie._DeleteAction.UPDATED, reference
            elif action == MerklePatriciaTrie._DeleteAction.USELESS_BRANCH:
                # Just update reference.
                _, next_ref = info
                node.branches[idx] = next_ref
                reference = self._store_node(node)
                return MerklePatriciaTrie._DeleteAction.UPDATED, reference

    def _build_new_node_from_last_branch(self, branches):
        """
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
        
        """

        # Find the index of the only stored branch.
        idx = 0
        for i in range(len(branches)):
            if len(branches[i]) > 0:
                idx = i
                break

        # Path in leaf will contain one nibble (at this step).
        prefix_nibble = NibblePath([idx], offset=1)

        child = self._get_node(branches[idx])

        path = None
        node = None

        # Build new node.
        # If next node is leaf or extension, merge it.
        # If next node is branch, create an extension node with one nibble in path.
        if type(child) == Leaf:
            path = NibblePath.combine(prefix_nibble, child.path)
            node = Leaf(path, child.data)
        elif type(child) == Extension:
            path = NibblePath.combine(prefix_nibble, child.path)
            node = Extension(path, child.next_ref)
        elif type(child) == Branch:
            path = prefix_nibble
            node = Extension(path, branches[idx])

        reference = self._store_node(node)

        return MerklePatriciaTrie._DeleteAction.USELESS_BRANCH, (path, reference)