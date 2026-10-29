import sys
import math
import random
import matplotlib.pyplot as plt

def shannon(probabilities):
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

def main() -> None:
    with open("rfc2324.txt", "r", encoding="utf-8") as file:
        text = file.read()
        
    Hardcoded_Word = text
    readDictionary = {}
    
    for char in Hardcoded_Word:
        if char in readDictionary:
            readDictionary[char] += 1
        else:
            readDictionary[char] = 1
            
    sortedDictionary = dict(sorted(readDictionary.items(), key=lambda item:item[1], reverse=True))
    
    probabilities = {}
    for i in sortedDictionary:
        probabilities[i] = sortedDictionary[i] / len(Hardcoded_Word)

    shannon_code = Code(probabilities, shannon)

    shannon_lens = []

    # 10x Durchläufe analog zum Vorbild
    for i in range(10):
        wort = "".join(random.choices(text, k=1000))
        # shannon_code.encode(wort) gibt (code, av_char_length, redundancy) zurück; wir nehmen Element [0]
        shannon_lens.append(len(shannon_code.encode(wort)[0]))

    # Plot erstellen
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(range(1, 11), shannon_lens, color='skyblue')
    ax.set_title("Shannon-Fano")
    ax.set_xlabel("Durchlauf")
    ax.set_ylabel("Codierungslänge")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
