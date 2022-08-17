class NibblePath:
    """
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

    """
    ODD_FLAG = 0x10
    LEAF_FLAG = 0x20

    def __init__(self, data, offset=0):
        """
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

        """
        self._data = data
        self._offset = offset

    def __len__(self):
        """Return the length of the path."""
        return len(self._data) * 2 - self._offset

    def __repr__(self):
        """
        Return a string representation of the path.
        
        Returns the data in hex format and the offset.
        """
        return "<NibblePath: Data: 0x{}, Offset: {}>".format(self._data.hex(), self._offset)

    def __str__(self):
        """
        Return a string representation of the path.
        
        Returns the data in hex format and the raw data.
        """
        return '<Hex 0x{} | Raw {}>'.format(self._data.hex(), self._data)

    def __eq__(self, other):
        """ 
        Check if two paths are equal.
        
        Parameters
        ----------
        other : NibblePath
            Other path to compare with.

        Returns
        -------
        bool
            True if paths are equal, False otherwise.

        """
        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self.at(i) != other.at(i):
                return False

        return True

    def decode_with_type(data):
        """
        Decode the NibblePath and its type from raw bytes.
        
        Parameters
        ----------
        data : bytes
            Raw bytes of the path.

        Returns
        -------
        tuple
            Tuple of NibblePath and its type.

        """
        is_odd_len = data[0] & NibblePath.ODD_FLAG == NibblePath.ODD_FLAG
        is_leaf = data[0] & NibblePath.LEAF_FLAG == NibblePath.LEAF_FLAG

        if is_odd_len:
            offset = 1 
        else:
            offset = 2

        return NibblePath(data, offset), is_leaf

    def decode(data):
        """
        Decodes NibblePath without its type from raw bytes.
        
        Parameters
        ----------
        data : bytes
            Raw bytes of the path.
            
        Returns
        -------
        NibblePath
            Decoded path.
                
        """
        return NibblePath.decode_with_type(data)[0]

    def starts_with(self, other):
        """
        Checks if `other` is prefix of `self`.
        
        Parameters
        ----------
        other : NibblePath
            Prefix to check.
            
        Returns
        -------
        bool
            True if `other` is prefix of `self`, False otherwise.
        """
        if len(other) > len(self):
            return False

        for i in range(len(other)):
            if self.at(i) != other.at(i):
                return False

        return True

    def at(self, idx):
        """
        Returns nibble at the certain position.
        
        Parameters
        ----------
        idx : int
            Position of the nibble.
            
        Returns
        -------
        int
            Nibble at the certain position.
            
        """
        idx = idx + self._offset

        byte_idx = idx // 2
        nibble_idx = idx % 2

        byte = self._data[byte_idx]

        nibble = byte >> 4 if nibble_idx == 0 else byte & 0x0F

        return nibble

    def consume(self, amount):
        """
        Cuts off nibbles at the beginning of the path.
        
        Parameters
        ----------
        amount : int
            Number of nibbles to cut off.
            
        Returns
        -------
        NibblePath
            New path with cut off nibbles.
        
        """
        self._offset += amount
        return self

    def _create_new(path, length):
        """
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
        
        """
        # BUG: #4 bytes_len is not used, should it be? 
        # Hack to get the length of the path in bytes?
        bytes_len = (length + 1) / 2
        data = []

        is_odd_len = length % 2 == 1
        pos = 0

        if is_odd_len:
            data.append(path.at(pos))
            pos += 1

        while pos < length:
            data.append(path.at(pos) * 16 + path.at(pos + 1))
            pos += 2

        offset = 1 if is_odd_len else 0

        return NibblePath(data, offset)

    def common_prefix(self, other):
        """
        Returns common part at the beginning of both paths.
        
        Parameters
        ----------
        other : NibblePath
            Other path to compare with.
        
        Returns
        -------
        NibblePath
            Common part at the beginning of both paths.
        
        """
        least_len = min(len(self), len(other))
        common_len = 0
        for i in range(least_len):
            if self.at(i) != other.at(i):
                break
            common_len += 1

        return NibblePath._create_new(self, common_len)

    def encode(self, is_leaf):
        """
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

        """
        output = []

        nibbles_len = len(self)
        is_odd = nibbles_len % 2 == 1

        prefix = 0x00
        prefix += self.ODD_FLAG + self.at(0) if is_odd else 0x00
        prefix += self.LEAF_FLAG if is_leaf else 0x00

        output.append(prefix)

        pos = nibbles_len % 2

        while pos < nibbles_len:
            byte = self.at(pos) * 16 + self.at(pos + 1)
            output.append(byte)
            pos += 2

        return bytes(output)

    class _Chained:
        """
        Class that chains two paths.
        """

        def __init__(self, first, second):
            """
            Initializes the chained paths.

            Parameters
            ----------
            first : NibblePath
                First path.
            second : NibblePath
                Second path.

            """
            self.first = first
            self.second = second

        def __len__(self):
            """Return the length of the chained paths."""
            return len(self.first) + len(self.second)

        def at(self, idx):
            """
            Return the nibble at the certain position.
            
            Parameters
            ----------
            idx : int
                Position of the nibble.

            Returns
            -------
            int
                Nibble at the certain position.

            """
            if idx < len(self.first):
                return self.first.at(idx)
            else:
                return self.second.at(idx - len(self.first))

    def combine(self, other):
        """
        Merges two paths into one.
        
        Parameters
        ----------
        other : NibblePath
            Other path to merge with.
            
        Returns
        -------
        NibblePath
            Merged path.
        
        """
        chained = NibblePath._Chained(self, other)
        return NibblePath._create_new(chained, len(chained))
