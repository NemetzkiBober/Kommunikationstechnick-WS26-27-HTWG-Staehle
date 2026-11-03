import math


class LempelZiv:
    charD = {}              # enthält die verwendete Codierung der Buchstaben zu Bits

    def __init__(self, rueck_bits=4, laengen_bits=3):
        self.rueck_bits = rueck_bits
        self.laengen_bits = laengen_bits
    # set(message) liefert Ihnen die buchstaben
    # • f‘{i:0{n}b}‘ stellt die Zahl i als Bitstring mit n Stellen dar
    def encode(self, message):
        zeichen = sorted(set(message))
        anzahl_bits = max(1, math.ceil(math.log2(len(zeichen)))) if zeichen else 1

        charD = {
            c: f"{i:0{anzahl_bits+1}b}"     # +1 wegen 0-Präfix
            for i, c in enumerate(zeichen)
        }

        t = []
        i = 0
        bit_string = ""
        max_off = 0
        max_len = 0
        while i < len(message):
            best_len = 0
            best_off = 0
            for j in range(i):
                length = 0
                while i + length < len(message)-1 and message[j + length] == message[i + length]:
                    length += 1
                if length > best_len:
                    best_len, best_off = length, i - j
            nxt = message[i + best_len] if i + best_len < len(message) else ''
            t.append((best_off, best_len, nxt))
            if best_off > max_off:
                max_off = best_off
            if best_len > max_len:
                max_len = best_len
            i += best_len + 1

        print("größter Offset + größte Länge: ")
        print(max_off)
        print(max_len)
        # TODO: mybe error geben wenn off oder len nicht passen, weil wenn zu klein lässt sich zwar encoden aber nicht decode und code ist eh falsch

        for off, length, nxt in t:
            if off == 0 and length == 0:
                bit_string += charD[nxt]
            else:
                bit_string += (
                        "1"
                        + f"{off:0{self.rueck_bits}b}"
                        + f"{length:0{self.laengen_bits}b}"
                        + charD[nxt]
                )

        print(charD)
        #print(bit_string)

        return bit_string, charD

    def decode(self, bitstring, charD):
        # • int(bin_str,2) wandelt einen binären String in eine Dezimalzahl um
        len_word = len(next(iter(charD.values())))  # get length of first value in charD
        i = 0
        message = ""
        while i < len(bitstring):
            if bitstring[i] == '0':
                s = list(charD.keys())[list(charD.values()).index(bitstring[i: i+len_word])]
                message += s
                i += len_word
            elif bitstring[i] == '1':
                off = int(bitstring[i+1:i+1+self.rueck_bits], 2)
                length = int(bitstring[i+1+self.rueck_bits:i+1+self.rueck_bits+self.laengen_bits], 2)
                nxt = list(charD.keys())[list(charD.values()).index(bitstring[i+1+self.rueck_bits+self.laengen_bits:i+1+self.rueck_bits+self.laengen_bits+len_word])]
                start = len(message) - off

                for j in range(length):
                    message += message[start + j]

                message += nxt
                i += 1 + len_word + self.laengen_bits + self.rueck_bits

        return message

def main():
    with open("rfc_2324.txt", "r", encoding="utf-8") as file:
        wort = "".join(file.read())

    lz = LempelZiv(15,7)

    #bit_string, charD = lz.encode("hallo hallo")
    # wort = "FISCHERSFRITZFISCHTFRISCHEFISCHE"
    #wort = "BANANENANBAU"
    bit_string, charD = lz.encode(wort)
    print("länge bitstring")

    message = lz.decode(bit_string, charD)

    print("Längen:", len(wort), len(message))
    #print(message)
    print(wort == message)



if __name__ == '__main__':
    main()