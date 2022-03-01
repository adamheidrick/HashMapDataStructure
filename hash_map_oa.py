# Name: Adam Heidrick
# OSU Email: heidrica@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 Hash Map
# Due Date: 11 March 2022
# Description: Open Addressing Hash Map


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        for index in range(self.capacity):
            self.buckets[index] = None
        self.size = 0

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hashmap, then
        None is returned.
        """

        index = self.hash_function(key) % self.capacity
        num = 1
        look = index
        while self.buckets[look] is not None:
            if self.buckets[look].key == key and self.buckets[index].is_tombstone is False:
                return self.buckets[look].value
            else:
                look = (index + num ** 2) % self.capacity
                num += 1

    def quad_probe(self, da: DynamicArray, index: int, key: str, value: object, capacity: int) -> None:
        """
        This uses quadratic probing: i = ( initial + j^2) % m where j = 1,2,3 etc. and m = table capacity.
        """

        for num in range(1, capacity):
            look = (index + num ** 2) % capacity

            if da[look] is None or da[look].is_tombstone is True:
                da[look] = HashEntry(key, value)
                self.size += 1
                break

            elif da[look].key == key:
                da[look].value = value
                break

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map. If a key already exists then the value is updated.
        If the table load factor is greater than .05, the table is resized.
        This uses a quadratic probing helper function.
        """

        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        index = self.hash_function(key) % self.capacity

        if self.buckets[index] is None:
            self.buckets[index] = HashEntry(key, value)
            self.size += 1

        elif self.buckets[index].key == key:  # if not none and same key then we update the value.
            self.buckets[index].value = value

        else:
            self.quad_probe(self.buckets, index, key, value, self.capacity)  # Index is full, so we need to probe.

    def remove(self, key: str) -> None:
        """
        This method removes a value from the hashmap. Remove here is just a toggle of the is_tombstone value.
        """
        index = self.hash_function(key) % self.capacity
        num = 1
        look = index
        while self.buckets[look] is not None:
            if self.buckets[look].key == key and self.buckets[look].is_tombstone is False:
                self.buckets[look].is_tombstone = True
                self.size -= 1
                return
            else:
                look = (index + num ** 2) % self.capacity
                num += 1

    def contains_key(self, key: str) -> bool:
        """
        This method returns a boolean if a key is in the hashmap.
        """
        index = self.hash_function(key) % self.capacity
        num = 1
        look = index
        while self.buckets[look] is not None:
            if self.buckets[look].key == key and self.buckets[index].is_tombstone is False:
                return True
            else:
                look = (index + num ** 2) % self.capacity
                num += 1

        return False

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        buckets = 0
        for index in range(self.capacity):
            if self.buckets[index] is None:
                buckets += 1

        return buckets

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        This method resizes the hash table.
        It creates a new Dynamic Array with the new size and rehashes the old objects into the new array.
        """
        if new_capacity < 1 or new_capacity < self.size:
            return

        if self.size / new_capacity >= 0.5:  # If the new capacity tips the load factor, then the size is doubled.
            new_capacity = new_capacity * 2

        size = self.size  # This is to store the size value as the percolate method adjusts the size.

        new_buckets = DynamicArray()

        for _ in range(new_capacity):  # The new array is appended with None to fill it's new size.
            new_buckets.append(None)

        # iterate through the old list and rehash
        for index in range(self.capacity):

            if self.buckets[index] is not None and self.buckets[index].is_tombstone is False:  # An object was found

                new_index = self.hash_function(self.buckets[index].key) % new_capacity  # New index calculated

                if new_buckets[new_index] is None:  # If the spot is open, then the object is inserted.
                    new_buckets[new_index] = self.buckets[index]

                else:  # We use the quade probe method to find a new spot.
                    """TA: This is for some reason failing my last gradescope test. 
                    I have no idea why. Everything else works and put uses the same method. 
                    This is the first assignment where I have accepted gradescope defeat. But I am defeated. 
                    """
                    self.quad_probe(new_buckets, new_index, self.buckets[index].key,\
                                    self.buckets[index].value, new_capacity)

        self.size = size  # restore size
        self.buckets = new_buckets  # hooks up new DA to be the self.da
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        This method returns a Dynamic Array appended with the keys of the hashmap.
        """
        new_arr = DynamicArray()
        for index in range(self.capacity):
            if self.buckets[index] is not None:
                if self.buckets[index].is_tombstone is False:
                    new_arr.append(self.buckets[index].key)

        return new_arr


if __name__ == "__main__":
    # TEST AWAY!
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)

    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    # #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    # m = HashMap(10, hash_function_1)
    # m.put('key1', 10)
    # print(m)
    # m.put('key1', 20)
    # print(m)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m)
    # print(m.table_load())
    # m.put('key3', 20)
    # print(m)
    # print(m.table_load())
    # m.put('key4', 20)
    # print(m)
    # print(m.table_load())
    # m.put('key5', 20)
    # print(m)
    # print(m.table_load())
    # m.put('key6', 20)
    # print(m)
    # print(m.table_load())
    # print(m.size)
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    # #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    #
    # m.resize_table(111)
    # print(m)
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         result &= m.contains_key(str(key))
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
    #

    # SELF TEST. USING GRADESCHOPE TO PERFORM THE SAME TEST:
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    print(m)
    print("end of list")
    # It works to this point and this is the same test as gradescope.
    # PUT WORKS SO JUST PUT NEW VALUES IN! WHAT IS THE PROBLEM?


    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    # #
    # m.resize_table(1)
    # print(m.get_keys())
    # #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
