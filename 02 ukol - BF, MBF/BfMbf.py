import math
import mmh3
from bitarray import bitarray
import random
import time

class BloomFilter:
    def __init__(self, n, f):
        self.n = n
        self.f = f

        self.m = self.calculateM()
        self.k = self.calculateK()

        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)
       # self.printParameters() # PRIPADNE ODKOMENTOVAT PRO TISK PARAMETRU

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

###############################################!

class MultiBandFilter:
    def __init__(self, n, f):
        self.n = n
        self.f = f

        self.m = self.calculateM()
        self.k = self.calculateK()
        self.bands = self.k
        self.band_size = self.m // self.bands # tady nevim, jestli bend_size má být self.m nebo self.m // self.bands (kdyztak to staci zakomentovat pred //)

        self.bit_arrays = [bitarray(self.band_size) for _ in range(self.bands)]
        for bit_array in self.bit_arrays:
            bit_array.setall(0)

       # self.printParameters() # PRIPADNE ODKOMENTOVAT PRO TISK PARAMETRU

    def calculateM(self):
        return int(-math.log(self.f)*self.n/(math.log(2)**2))

    def calculateK(self):
        return int(self.m*math.log(2)/self.n)

    def printParameters(self):
        print("MultiBandFilter parameters:")
        print(f"n = {self.n}, f = {self.f}, m = {self.m}, k = {self.k}, bands = {self.bands}, band size = {self.band_size}")

    def insert(self, item):
        for i in range(self.k):
            index = mmh3.hash(item, i) % self.band_size
            band_index = i 
            self.bit_arrays[band_index][index] = 1

    def lookup(self, item):
        for i in range(self.k):
            index = mmh3.hash(item, i) % self.band_size
            band_index = i 
            if self.bit_arrays[band_index][index] == 0:
                return False
        return True

###############################################!

if __name__ == "__main__":
    # Parametry
    num_elements = 10**7 # 10**7
    false_positive_rate = 0.02
    test_elements = 10**6 # 10**6
    max_value = 10**12

    # Nastavit parametry pro BloomFilter a MultiBandFilter
    bf = BloomFilter(num_elements, false_positive_rate)
    mbf = MultiBandFilter(num_elements, false_positive_rate)

    # Generovat random cisla jako stringy 
    random.seed(42)
    elements = [str(random.randint(0, max_value)) for _ in range(num_elements)]
    test_values = [str(random.randint(0, max_value)) for _ in range(test_elements)]

    # Vkladani do filtru
    for element in elements:
        bf.insert(element)
        mbf.insert(element)

    # Urceni falesne pozitivity a casu pro vyhledavani
    def evaluate_filter(filter):
        start_time = time.time()
        false_positives = 0
        for value in test_values:
            if filter.lookup(value): 
                false_positives += 1
        elapsed_time = time.time() - start_time
        fp_rate = false_positives / test_elements
        return fp_rate, elapsed_time

    #print("\nEvaluating Bloom Filter...")
    bf_fp_rate, bf_time = evaluate_filter(bf)

    #print("\nEvaluating MultiBand Filter...")
    mbf_fp_rate, mbf_time = evaluate_filter(mbf)

    
    print(f"Mira falesne pozitivity Bloomova Filtru je {bf_fp_rate:.4%}, coz {'odpovida' if bf_fp_rate <= false_positive_rate else 'neodpovida'} pozadovane mire max. {false_positive_rate:.4%}.")
    print(f"Mira falesne pozitivity MultiBand Filtru je {mbf_fp_rate:.4%}, coz {'odpovida' if mbf_fp_rate <= false_positive_rate else 'neodpovida'} pozadovane mire max. {false_positive_rate:.4%}.")
   
    if bf_fp_rate < mbf_fp_rate:
        print (f"Chybovost Bloomova filtru je o {mbf_fp_rate - bf_fp_rate:.4%} nizsi nez chybovost MultiBand filtru.")
    elif bf_fp_rate > mbf_fp_rate:
        print (f"Chybovost MultiBand filtru je o {bf_fp_rate - mbf_fp_rate:.4%} nizsi nez chybovost Bloomova filtru.")
    else: 
        print ("Chybovost obou filtru je stejna.")

    print(f"Celkova doba vyhledavani v BF byla {bf_time:.3f} sekund a v MBF {mbf_time:.3f} sekund.")  #{mbf_time:.2f}

