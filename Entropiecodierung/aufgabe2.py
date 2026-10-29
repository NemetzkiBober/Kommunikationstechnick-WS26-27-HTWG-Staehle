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

    # --- Grafische Darstellung ---
    labels = list(sortedDictionary.keys())
    freqs = list(sortedDictionary.values())
    infos = [informationsgehalt[k] for k in labels]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color1 = 'tab:blue'
    ax1.set_xlabel('Zeichen (absteigende Wahrscheinlichkeit)')
    ax1.set_ylabel('Häufigkeit (Anzahl)', color=color1)
    ax1.bar(x - width/2, freqs, width, label='Häufigkeit', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Informationsgehalt (Bit)', color=color2)
    ax2.bar(x + width/2, infos, width, label='Informationsgehalt', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.title('Häufigkeit und Informationsgehalt der Zeichen')
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
