"""An Array module for homework 2."""


class ArrayMagicPrototype(object):
    """The prototype for an Array class which implements all magic methods."""

    def __init__(self, *args):
        """
        Create tuple from the given values.

        Args:
            args : values to construct Array.
        """
        self._stored_data = tuple(args)

    def get_data(self):
        """
        Get stored data.

        Returns:
            Stored data.
        """
        return self._stored_data

    def __add__(self, other):
        """
        Concatenate two Arrays.

        Args:
            other: An Array to add.

        Returns:
            Array where data equals concatenation of Arrays data.

        Raises:
            ValueError: if other is not an instance of Array
        """
        if isinstance(other, Array):
            result_data = self._stored_data + other.get_data()
            return Array(*result_data)
        raise ValueError

    def __len__(self):
        """
        Get length of an Array.

        Returns:
            Length of an Array.
        """
        return len(self._stored_data)

    def __iter__(self):
        """
        Get an Array iter.

        Returns:
             Array iter.
        """
        return iter(self._stored_data)

    def __getitem__(self, index):
        """
        Get item by index.

        Args:
            index: The index of a method.

        Returns:
            Element by index.

        Raises:
            IndexError: If index is out of range.
        """
        if index < 0 or index >= len(self._stored_data):
            raise IndexError
        return self._stored_data[index]


class Array(ArrayMagicPrototype):
    """An Array class over tuple."""

    def append(self, value_to_add):
        """
        Add an element to the end of Array.

        Args:
            value_to_add: The value to add.
        """
        self._stored_data += (value_to_add,)

    def index(self, search_value):
        """
        Get index of a value.

        Args:
            search_value: The value to search for.

        Returns:
            Index of first occurrence of searched value if found, -1 otherwise.
        """
        try:
            return self._stored_data.index(search_value)
        except ValueError:
            return -1

    def pop(self, index):
        """
        Erases element from Array by index.

        Args:
            index: The index to erase element by.

        Returns:
            Erased element.

        Raises:
            IndexError: If index is out of range.
        """
        if index < 0 or index >= len(self._stored_data):
            raise IndexError
        poped = self._stored_data[index]
        before_elem = self._stored_data[:index]
        after_elem = self._stored_data[index + 1:]
        self._stored_data = before_elem + after_elem
        return poped

    def remove(self, remove_value):
        """
        Remove first occurrence of the value from the Array.

        If there is no such value, nothing happens.

        Args:
            remove_value: The value to remove.
        """
        index = self.index(remove_value)
        if index != -1:
            self.pop(index)
