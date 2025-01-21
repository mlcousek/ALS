import math
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, n, f):
        self.n = n
        self.f = f

        # Removed parameters
        self.m = self.calculateM()
        self.k = self.calculateK()

        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)
        self.printParameters()

    def calculateM(self):
        return int(-math.log(self.f)*self.n/(math.log(2)**2))

    def calculateK(self):
        return int(self.m*math.log(2)/self.n)

    def printParameters(self):
        print("Init parameters:")
        print(f"n = {self.n}, f = {self.f}, m = {self.m}, k = {self.k}")

    def insert(self, item):
        for i in range(self.k):
            index = mmh3.hash(item, i) % self.m
            self.bit_array[index] = 1

    def lookup(self, item):
        for i in range(self.k):
            index = mmh3.hash(item, i) % self.m
            if self.bit_array[index] == 0:
                return False
        return True


if __name__ == "__main__":
    bf = BloomFilter(10, 0.01)

    bf.insert("1")
    bf.insert("2")
    bf.insert("42")

    print("1 {}".format(bf.lookup("1")))
    print("2 {}".format(bf.lookup("2")))
    print("3 {}".format(bf.lookup("3")))
    print("42 {}".format(bf.lookup("42")))
    print("43 {}".format(bf.lookup("43")))
