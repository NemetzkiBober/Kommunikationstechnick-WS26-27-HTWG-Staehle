import sys
import math
import argparse
import numpy as np
import pandas as pd
import statistics as stats
import matplotlib.pyplot as plt 

def main() -> None:
    Terminal_Input = False
    Hardcoded_Word = "Hochschule"
    
    with open("rfc2324.txt", "r", encoding="utf-8") as f:
        rfc = f.read()
    ##print(rfc)

    if Terminal_Input:
        word = input("Wort eingeben: ").upper()
    else:
        word = rfc.upper()

    readDictionary = {}
    
    for i in range (len(word)):
        if word[i] in readDictionary:
            readDictionary[word[i]] = readDictionary[word[i]]+1
        else:
            readDictionary[word[i]] = 1
            
    sortedDictionary = dict(sorted(readDictionary.items(), key=lambda item:item[1], reverse=True))
    print("Count:", sortedDictionary)

    probabilities = {}
    
    for i in sortedDictionary:
        probabilities[i] = sortedDictionary[i]/len(word)

    print("Probabilities:", {k: round(v, 4) for k, v in probabilities.items()})

    informationsgehalt = {}
    
    for i in probabilities:
        # Cast np.float64 to native Python float to strip the wrapper
        informationsgehalt[i] = float(np.log2(1/probabilities[i]))
        

    print("Information Content:", {k: round(v, 4) for k, v in informationsgehalt.items()})

    entropie = {}
    for i in sortedDictionary:
        entropie[i] = probabilities[i]*informationsgehalt[i]
        
    print("Entropy:", {k: round(v, 4) for k, v in entropie.items()})

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] AusfÃ¼hrung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)