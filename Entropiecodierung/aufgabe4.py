import sys
import os
import math
import random
import matplotlib.pyplot as plt

# Inject the 'partner' directory into sys.path to allow aufg1.py to resolve its internal flat imports
current_dir = os.path.dirname(os.path.abspath(__file__))
partner_dir = os.path.join(current_dir, "partner")
if partner_dir not in sys.path:
    sys.path.append(partner_dir)

from aufg1 import Huffmann, Source
from static_model import StaticModel
from arithmetic_compressor import AECompressor


def shannon(probabilities: dict) -> dict:
    codeDictionary = {}

    def add_Zero(dictionary):
        for i in dictionary:
            if i in codeDictionary:
                codeDictionary[i] += "0"
            else:
                codeDictionary[i] = "0"

    def add_One(dictionary):
        for i in dictionary:
            if i in codeDictionary:
                codeDictionary[i] += "1"
            else:
                codeDictionary[i] = "1"

    def break_dict(dictionary, fullprob):
        if len(dictionary) <= 1:
            return
        prob = 0
        lastprob = 0
        pivot = None
        lastpivot = None
        for i in dictionary:
            prob = round(dictionary[i] + prob, 4)
            if prob == 0:
                break
            if prob >= fullprob / 2:
                if abs(prob - fullprob / 2) <= abs(lastprob - fullprob / 2):
                    pivot = i
                else:
                    pivot = lastpivot
                break

            lastprob = prob
            lastpivot = i 
            
        left_dictionary = {}
        right_dictionary = {}

        passed_pivot = False
        for i in dictionary:
            if not passed_pivot:
                left_dictionary[i] = dictionary[i]
                if i == pivot:
                    passed_pivot = True
            else:
                right_dictionary[i] = dictionary[i] 
                
        add_Zero(left_dictionary)
        add_One(right_dictionary)

        if len(left_dictionary) > 1:
            break_dict(left_dictionary, sum(left_dictionary.values()))

        if len(right_dictionary) > 1:
            break_dict(right_dictionary, sum(right_dictionary.values()))

    break_dict(probabilities, sum(probabilities.values()))
    return codeDictionary


class Code:
    def __init__(self, nachrichtenquelle, coder_func):
        self.nachrichtenquelle = nachrichtenquelle
        self.codeDictionary = coder_func(self.nachrichtenquelle)
        self.decodeDictionary = {v: k for k, v in self.codeDictionary.items()}

        self.entropie = 0
        for p in self.nachrichtenquelle.values():
            if p > 0:
                self.entropie -= p * math.log2(p)

        self.mittlere_codewortlaenge = 0
        for zeichen, p in self.nachrichtenquelle.items():
            self.mittlere_codewortlaenge += p * len(self.codeDictionary[zeichen])

        self.redundanz = self.mittlere_codewortlaenge - self.entropie

    def encode(self, word):
        code = ""
        for char in word:
            code += self.codeDictionary[char]

        if len(word) > 0:
            av_char_length = len(code) / len(word)
            
            freqs = {}
            for char in word:
                freqs[char] = freqs.get(char, 0) + 1
                
            wort_entropie = 0
            for count in freqs.values():
                p = count / len(word)
                wort_entropie -= p * math.log2(p)
                
            redundancy = av_char_length - wort_entropie
        else:
            av_char_length = 0
            redundancy = 0

        return code, av_char_length, redundancy

    def decode(self, code):
        word = ""
        current_code = ""
        for bit in code:
            current_code += bit
            if current_code in self.decodeDictionary:
                word += self.decodeDictionary[current_code]
                current_code = ""
        return word


def arith(woerter: str) -> str:
    p = Source(woerter, False).p
    model = StaticModel(p)
    coder = AECompressor(model)
    compressed = coder.compress(woerter)
    return "".join(map(str, compressed))


def main() -> None:
    # with open("rfc2324.txt", "r", encoding="utf-8") as file:
    #     text = file.read()
    text = "Hochschule"
        
    readDictionary = {}
    for char in text:
        if char in readDictionary:
            readDictionary[char] += 1
        else:
            readDictionary[char] = 1
            
    sortedDictionary = dict(sorted(readDictionary.items(), key=lambda item:item[1], reverse=True))
    
    probabilities = {}
    for i in sortedDictionary:
        probabilities[i] = sortedDictionary[i] / len(text)

    # Initialize Encoders
    shannon_code = Code(probabilities, shannon)
    code_huff = Huffmann(text)

    shannon_lens = []
    huf_lens = []
    arit_lens = []

    # 10x Random Sampling & Encoding
    for _ in range(10):
        wort = "".join(random.choices(text, k=1000))
        
        shannon_lens.append(len(shannon_code.encode(wort)[0]))
        huf_lens.append(len(code_huff.encode(wort)[0]))
        arit_lens.append(len(arith(wort)))

    # Visualization
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.bar(range(1, 11), shannon_lens, color='skyblue')
    ax1.set_title("Shannon-Fano")
    ax1.set_xlabel("Durchlauf")
    ax1.set_ylabel("Codierungslänge (Bits)")

    ax2.bar(range(1, 11), huf_lens, color='lightgreen')
    ax2.set_title("Huffman")
    ax2.set_xlabel("Durchlauf")
    ax2.set_ylabel("Codierungslänge (Bits)")

    ax3.bar(range(1, 11), arit_lens, color='salmon')
    ax3.set_title("Arithmetisch")
    ax3.set_xlabel("Durchlauf")
    ax3.set_ylabel("Codierungslänge (Bits/Bytes)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
