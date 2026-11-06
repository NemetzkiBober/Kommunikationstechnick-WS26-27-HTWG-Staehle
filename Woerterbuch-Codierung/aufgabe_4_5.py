# Laborübung Wörterbuch-Codierung - Aufgabe 4 (Test) und Aufgabe 5 (Performance)

import contextlib
import io
import math

from LempelZiv import LempelZiv
from lempelZivWelch import lempelZivWelch


def ohne_ausgabe(funktion, *args):
    # Die Klassen geben viel mit print aus, das brauchen wir beim RFC nicht
    with contextlib.redirect_stdout(io.StringIO()):
        return funktion(*args)


def bits_fuer(zahl):
    # Wie viele Bits braucht man, um die Zahlen 0 bis zahl darzustellen?
    return max(1, math.ceil(math.log2(zahl + 1)))


# ---------------------------------------------------------------- Lempel-Ziv

def laengster_treffer(text, i, fenster, max_laenge):
    # Sucht ab Position i die längste Übereinstimmung im Fenster davor.
    # Wie im Original: bei gleicher Länge gewinnt die früheste Stelle,
    # und nach dem Treffer muss noch ein Zeichen übrig sein.
    start = max(0, i - fenster)
    grenze = min(max_laenge, len(text) - 1 - i)
    laenge = 0
    pos = -1
    while laenge < grenze:
        suche = text[i:i + laenge + 1]
        j = text.find(suche, start, i + laenge)   # j muss vor i liegen
        if j == -1:
            break
        laenge += 1
        pos = j
        start = j
    if laenge == 0:
        return 0, 0
    return i - pos, laenge


def lz_tripel(text, fenster, max_laenge):
    tripel = []
    i = 0
    while i < len(text):
        offset, laenge = laengster_treffer(text, i, fenster, max_laenge)
        tripel.append((offset, laenge, text[i + laenge]))
        i += laenge + 1
    return tripel


def lz_anzahl_bits(tripel, zeichen_bits, rueck_bits, laengen_bits):
    # Einzelnes Zeichen: 0 + Zeichencode
    # Referenz:         1 + Offset + Länge + Zeichencode
    summe = 0
    for offset, laenge, zeichen in tripel:
        if laenge == 0:
            summe += zeichen_bits
        else:
            summe += 1 + rueck_bits + laengen_bits + zeichen_bits
    return summe


class LempelZivMitFenster(LempelZiv):
    # Das Original sucht im ganzen bisherigen Text. Dann passen große Offsets
    # nicht mehr in rueck_bits Bits. Hier wird das Suchfenster begrenzt,
    # decode wird unverändert aus LempelZiv übernommen.

    def encode(self, message):
        buchstaben = sorted(set(message))
        n = max(1, math.ceil(math.log2(len(buchstaben))))
        charD = {c: f"{i:0{n + 1}b}" for i, c in enumerate(buchstaben)}

        fenster = 2 ** self.rueck_bits - 1
        max_laenge = 2 ** self.laengen_bits - 1

        bitstring = ""
        for offset, laenge, zeichen in lz_tripel(message, fenster, max_laenge):
            if laenge == 0:
                bitstring += charD[zeichen]
            else:
                bitstring += ("1" + f"{offset:0{self.rueck_bits}b}"
                              + f"{laenge:0{self.laengen_bits}b}" + charD[zeichen])
        return bitstring, charD


# ---------------------------------------------------------- Lempel-Ziv-Welch

# Die LZW-Klasse schreibt Wörterbuch-Einträge als "<12>" in den Ausgabetext.
# Der RFC enthält aber selbst '<' und '>' (bei den URLs), das würde der
# Decoder falsch verstehen. Deshalb tauschen wir die beiden Zeichen vorher
# gegen ungenutzte Zeichen aus und danach wieder zurück.

def spitze_klammern_ersetzen(text):
    return text.replace("<", "‹").replace(">", "›")


def spitze_klammern_zurueck(text):
    return text.replace("‹", "<").replace("›", ">")


def startwoerterbuch(text):
    charL = []
    for c in text:
        if c not in charL:
            charL.append(c)
    return charL


def lzw_indizes(ausgabe, charL):
    # Macht aus "BAN<6>E" die Liste der Wörterbuch-Indizes [0, 1, 2, 6, 3]
    indizes = []
    i = 0
    while i < len(ausgabe):
        if ausgabe[i] == "<":
            ende = ausgabe.index(">", i)
            indizes.append(int(ausgabe[i + 1:ende]))
            i = ende + 1
        else:
            indizes.append(charL.index(ausgabe[i]))
            i += 1
    return indizes


def lzw_anzahl_bits(indizes, start_groesse):
    # Beim k-ten Code hat das Wörterbuch höchstens start_groesse + k Einträge.
    # variabel: jeder Code bekommt nur so viele Bits wie gerade nötig
    # fest:     alle Codes bekommen die Bits für das Wörterbuch am Ende
    variabel = 0
    for k in range(len(indizes)):
        variabel += bits_fuer(start_groesse + k - 1)

    end_groesse = start_groesse + len(indizes) - 1
    fest = len(indizes) * bits_fuer(end_groesse - 1)
    return variabel, fest


def lzw_spezialfaelle(indizes, start_groesse):
    # Spezialfall: der Decoder bekommt einen Index, den er selbst noch gar
    # nicht im Wörterbuch hat (beim k-ten Code hat er start_groesse + k - 1).
    anzahl = 0
    for k in range(1, len(indizes)):
        if indizes[k] >= start_groesse + k - 1:
            anzahl += 1
    return anzahl


# ------------------------------------------------------------------ Aufgabe 4

def aufgabe_4():
    print("=" * 70)
    print("Aufgabe 4: Test mit den Beispielen aus der Vorlesung")
    print("=" * 70)

    for wort in ["FISCHERSFRITZFISCHTFRISCHEFISCHE", "BANANENANBAU"]:
        print(f"\n### {wort} ({len(wort)} Zeichen)\n")

        # Lempel-Ziv: Bitbreiten so wählen, dass Offset und Länge hineinpassen
        tripel = lz_tripel(wort, len(wort), len(wort))
        rueck_bits = bits_fuer(max(t[0] for t in tripel))
        laengen_bits = bits_fuer(max(t[1] for t in tripel))

        lz = LempelZiv(rueck_bits, laengen_bits)
        bitstring, charD = ohne_ausgabe(lz.encode, wort)
        ergebnis = lz.decode(bitstring, charD)

        print(f"Lempel-Ziv ({rueck_bits} Bit Offset, {laengen_bits} Bit Länge)")
        print("Tripel:", tripel)
        print(f"Bitstring ({len(bitstring)} Bit): {bitstring}")
        print("Decodiert:", ergebnis, "->", ergebnis == wort)

        # Lempel-Ziv-Welch
        charL = startwoerterbuch(wort)
        lzw = lempelZivWelch()
        print("\nLempel-Ziv-Welch, Startwörterbuch:", charL)
        ausgabe = lzw.encode(wort, charL)
        ergebnis = lzw.decode(ausgabe, charL)

        indizes = lzw_indizes(ausgabe, charL)
        variabel, fest = lzw_anzahl_bits(indizes, len(charL))
        print("Ausgabe:", ausgabe)
        print("Indizes:", indizes)
        print(f"Bits: {variabel} (variable Breite), {fest} (feste Breite)")
        print("Decodiert:", ergebnis, "->", ergebnis == wort)

        print(f"\nUnkomprimiert: {len(wort) * bits_fuer(len(set(wort)) - 1)} Bit")


# ---------------------------------------------------------------- Aufgabe 5.1

def aufgabe_5_1(text):
    print("\n" + "=" * 70)
    print("Aufgabe 5.1: Beste Bitbreiten für Lempel-Ziv beim RFC 2324")
    print("=" * 70)

    # gleiche Zeichencodierung wie in LempelZiv.encode (mit führender 0)
    zeichen_bits = bits_fuer(len(set(text)) - 1) + 1

    print("\nAnzahl Bits gesamt (Zeilen: Bits Offset, Spalten: Bits Länge)\n")
    print("Offset" + "".join(f"{lb:>9}" for lb in range(1, 9)))

    bestes = None
    for rueck_bits in range(1, 16):
        zeile = f"{rueck_bits:>6}"
        for laengen_bits in range(1, 9):
            tripel = lz_tripel(text, 2 ** rueck_bits - 1, 2 ** laengen_bits - 1)
            bits = lz_anzahl_bits(tripel, zeichen_bits, rueck_bits, laengen_bits)
            zeile += f"{bits:>9}"
            if bestes is None or bits < bestes[0]:
                bestes = (bits, rueck_bits, laengen_bits)
        print(zeile)

    bits, rueck_bits, laengen_bits = bestes
    print(f"\nOptimum: {rueck_bits} Bit Offset, {laengen_bits} Bit Länge -> {bits} Bit")

    # Gegenprobe mit dem decode aus LempelZiv.py
    lz = LempelZivMitFenster(rueck_bits, laengen_bits)
    bitstring, charD = lz.encode(text)
    print("Decodierung korrekt:", lz.decode(bitstring, charD) == text)

    return bits, rueck_bits, laengen_bits


# ---------------------------------------------------------------- Aufgabe 5.2

def aufgabe_5_2(text, lz_bits, rueck_bits, laengen_bits):
    print("\n" + "=" * 70)
    print("Aufgabe 5.2: Vergleich Lempel-Ziv / Lempel-Ziv-Welch beim RFC 2324")
    print("=" * 70)

    text_lzw = spitze_klammern_ersetzen(text)
    charL = startwoerterbuch(text_lzw)
    lzw = lempelZivWelch()
    ausgabe = ohne_ausgabe(lzw.encode, text_lzw, charL)
    ergebnis = spitze_klammern_zurueck(ohne_ausgabe(lzw.decode, ausgabe, charL))

    indizes = lzw_indizes(ausgabe, charL)
    variabel, fest = lzw_anzahl_bits(indizes, len(charL))
    print(f"\nLZW: {len(indizes)} Codes, "
          f"Spezialfall {lzw_spezialfaelle(indizes, len(charL))}x, "
          f"Decodierung korrekt: {ergebnis == text}")

    ascii_bits = 8 * len(text)
    ergebnisse = [
        ("ASCII (8 Bit pro Zeichen)", ascii_bits),
        (f"Lempel-Ziv ({rueck_bits}/{laengen_bits} Bit)", lz_bits),
        ("LZW, feste Codebreite", fest),
        ("LZW, variable Codebreite", variabel),
    ]
    print()
    for name, bits in ergebnisse:
        print(f"{name:<30}{bits:>8} Bit  {bits / len(text):.2f} Bit/Zeichen"
              f"  {100 * bits / ascii_bits:5.1f} %")

    if min(variabel, fest) < lz_bits:
        print("\n-> Lempel-Ziv-Welch ist besser")
    else:
        print("\n-> Lempel-Ziv ist besser")


if __name__ == "__main__":
    aufgabe_4()

    with open("rfc2324.txt", encoding="utf-8") as datei:
        rfc = datei.read()

    bits, rueck_bits, laengen_bits = aufgabe_5_1(rfc)
    aufgabe_5_2(rfc, bits, rueck_bits, laengen_bits)
