import heapq
import math
import random
import matplotlib.pyplot as plt
from collections import Counter
from static_model import StaticModel
from arithmetic_compressor import AECompressor


def aufg1_1():
    with open("wortliste.txt", "r", encoding="utf-8") as file:
        woerter = [zeile.strip() for zeile in file if zeile.strip()]

    # Wortlängen zählen
    anzahl_woerter = len(woerter)
    haeufigkeiten = Counter(len(wort) for wort in woerter)

    # Information für jede Wortlänge berechnen
    wortlaengen = sorted(haeufigkeiten.keys())
    information = []

    for laenge in wortlaengen:
        p = haeufigkeiten[laenge] / anzahl_woerter
        I = -math.log2(p)
        information.append(I)

    plt.plot(wortlaengen, information, marker="o")
    plt.xlabel("Wortlänge")
    plt.ylabel("Information (Bit)")
    plt.title("Information in Abhängigkeit von der Wortlänge")
    plt.grid(True)
    plt.show()

def aufg1_2():
    with open("wortliste.txt", "r", encoding="utf-8") as file:
        woerter = [zeile.strip() for zeile in file if zeile.strip()]

    woerter = list(filter(lambda x: len(x) == 7, woerter))     # Liste mit Wörtern der Länge 7)
    xylofon = ['X', 'y', 'l', 'o', 'f', 'o', 'n']
    haeufigkeiten = {'X': 0, 'y': 0, 'l': 0, 'o': 0, 'f': 0, 'n': 0}

    print(len(woerter))
    print(len([w for w in woerter if w[6] == 'n']))

    for wort in woerter:
        for i in range(len(xylofon)):
            if wort[i] == xylofon[i]:
                haeufigkeiten[xylofon[i]] += 1

    chars = sorted(haeufigkeiten.keys())
    information = []

    for char in chars:
        print(haeufigkeiten[char])
        res = math.log2(len(woerter)/haeufigkeiten[char])
        information.append(res)

    plt.bar(chars, information, color='skyblue')
    plt.title("Information eines einzelnen Buchstabens")
    plt.xlabel('Buchstabe')
    plt.ylabel('Information')
    plt.show()

def aufg1_3():
    xylofon = "Xylofon"
    with open("wortliste.txt", "r", encoding="utf-8") as file:
        woerter = [zeile.strip() for zeile in file if zeile.strip()]
    #woerter = list(filter(lambda x: len(x) == 7, woerter))     # Liste mit Wörtern der Länge 7
    woerter_len = len(woerter)
    substr = {}

    for i in range(1, len(xylofon)+1):
        prefix = xylofon[:i]
        for wort in woerter:
            if wort[:i] == prefix:        # Char-Array-To-String
                substr[prefix] = substr.get(prefix, 0) + 1
    info_front = []
    chars = sorted(substr.keys())
    for char in chars:
        I = math.log2(woerter_len/substr[char])
        info_front.append(I)

    xylofon_rev = xylofon[::-1]  # "nofolyX"
    substr_rev = {}

    info_back = []
    for i in range(1, len(xylofon_rev) + 1):
        suffix = xylofon_rev[:i]
        substr_rev[suffix[::-1]] = 0

        for wort in woerter:
            if wort[::-1][:i] == suffix:
                substr_rev[suffix[::-1]] += 1

    chars_rev = substr_rev.keys()
    for char in chars_rev:
        I = math.log2(woerter_len/substr_rev[char])
        info_back.append(I)

    print(substr)
    print(substr_rev)
    print(info_front)
    print(info_back)

    plt.bar(chars, info_front, color='skyblue')
    plt.title("Xyolofon")
    plt.xlabel('Buchstabe')
    plt.ylabel('Information')
    plt.show()

    plt.bar(chars_rev, info_back, color='skyblue')
    plt.title("nofolyX")
    plt.xlabel('Buchstabe')
    plt.ylabel('Information')
    plt.show()

class Source:
    p = {}
    I = {}
    H = 0
    def __init__(self, wort, show_plot=True):
        self.wort_dict = {}
        self.p = {}
        self.I = {}
        self.H = 0
        if isinstance(wort, str):
            for char in wort:
                self.wort_dict[char] = self.wort_dict.get(char, 0) + 1

        wort_len = len(wort)

        # Auftrittwahrscheinlichkeiten
        for char in self.wort_dict:
            self.p[char] = self.wort_dict[char] / wort_len

        # Informationsgehalt
        #I = ld(1/p)
        for char in self.p:
            self.I[char] = math.log2(1/self.p[char])

        # Entropie
        for char in self.I:
            self.H += self.p[char] * self.I[char]

        print("Anzahl: ")
        print(self.wort_dict)
        print("Auftrittswahrscheinlichkeiten: ")
        print(self.p)
        print("Informationsgehalt: ")
        print(self.I)
        print("Entropie: ")
        print(self.H)

        if show_plot:
            plt.bar(self.p.keys(), self.p.values(), color='skyblue')
            plt.title("Auftrittswahrscheinlichkeiten")
            plt.xlabel('Buchstabe')
            plt.ylabel('Information')
            plt.show()

            plt.bar(self.I.keys(), self.I.values(), color='skyblue')
            plt.title("Informationsgehalt pro Zeichen")
            plt.xlabel('Buchstabe')
            plt.ylabel('Information')
            plt.show()


def aufg2():
    #Source("Hochschule")
    with open("rfc_2324.txt", "r", encoding="utf-8") as file:
        wort = "".join(file.read())
    Source(wort)


class Huffmann:
    code_dict = {}
    def __init__(self, wort):
        self.wort = wort
        self.wort_heap = [(wort.count(char) / len(wort), char) for char in set(wort)]

        heapq.heapify(self.wort_heap)
        self.p = self.wort_heap.copy()
        if len(self.wort_heap) == 1:
            self.code_dict[self.wort_heap[0][1]] = "0"

        while len(self.wort_heap) > 1:
            a = heapq.heappop(self.wort_heap)
            b = heapq.heappop(self.wort_heap)
            c = a[1] + b[1]
            heapq.heappush(self.wort_heap, (a[0] + b[0], c))
            for char in a[1]:
                self.code_dict[char] = "1" + self.code_dict.get(char, "")

            for char in b[1]:
                self.code_dict[char] = "0" + self.code_dict.get(char, "")


        self.source = Source(wort, False)

    def encode(self, wort):
        res = ""
        if isinstance(wort, str):
            for char in wort:
                res += self.code_dict[char]

        # mittlere Codewortlänge
        # sum(p*l)
        length = len(res) / len(wort)

        # Redundanz
        # L_c - H_c
        R = length - self.source.H

        return res, length, R

    def decode(self, code):
        word = ""
        tmp = ""
        for char in code:
            tmp += char
            if tmp in self.code_dict.values():
                word += (list(self.code_dict.keys())[list(self.code_dict.values()).index(tmp)])
                tmp = ""

        return word

    
def aufg3():
    wort = "Hochschule"
    #wort = "HHHHH"
    # wort = "EEEEE"
    code = Huffmann(wort)
    res, av_len, red = code.encode("EEEEE")
    print(res)
    print(av_len)
    print(red)
    print(code.decode(res))


def aufg4():
    with open("rfc_2324.txt", "r", encoding="utf-8") as file:
        text = file.read()

    def arith(woerter):
        p = Source(woerter, False).p
        # create the model
        model = StaticModel(p)
        # create an arithmetic coder
        coder = AECompressor(model)
        # encode some data
        compressed = coder.compress(woerter)
        print("".join(map(str, compressed)))
        return "".join(map(str, compressed))

    code = Huffmann(text)

    huf_lens = []
    arit_lens = []

    # 10x
    for i in range(10):
        wort = "".join(random.choices(text, k=1000))
        huf_lens.append(len(code.encode(wort)[0]))
        arit_lens.append(len(arith(wort)))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.bar(range(1, 11), huf_lens, color='skyblue')
    ax1.set_title("Huffman")
    ax1.set_xlabel("Durchlauf")
    ax1.set_ylabel("Codierungslänge")

    ax2.bar(range(1, 11), arit_lens, color='skyblue')
    ax2.set_title("Arithmetisch")
    ax2.set_xlabel("Durchlauf")
    ax2.set_ylabel("Codierungslänge")

    plt.tight_layout()
    plt.show()

def __main__():
    # aufg1_1()
    # aufg1_2()
    # aufg1_3()
    # aufg2()
    # aufg3()
    aufg4()

if __name__ == "__main__":
    __main__()
