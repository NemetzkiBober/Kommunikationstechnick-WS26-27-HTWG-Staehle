import sys
import math
import argparse
import numpy as np
import pandas as pd
import statistics as stats
import matplotlib.pyplot as plt 

def main() -> None:
    Aufgabe1 = False
    Aufgabe2 = False
    Aufgabe3 = True
    Direction = True
    Terminal_Input = True
    Hardcoded_Word = "Xylofon"

    if Terminal_Input:
        word = input("Wort eingeben: ")
    else:
        word = Hardcoded_Word

    if Direction:
        answer = input("Forward (True or False): ").strip().lower()
        forward = answer == "true"
    else:
        forward = True

    df = pd.read_csv("wortliste.txt", sep=" ", names=["Wort"], header=None)
    df["char_count"] = df["Wort"].astype(str).str.len()
    count = df["char_count"].value_counts().sort_index()
    num_lines = len(df)

    WordDataSet = df.loc[df["char_count"] == len(word), ["Wort"]]
    WordDataSet_lines = len(WordDataSet)

    if Aufgabe1:

        calculation1 = num_lines/count
        log_cal = np.log2(calculation1)
        
        plt.figure(1)
        x = plt.plot(log_cal)
        plt.xlabel("Wortlänge")
        plt.ylabel("Information")

    if Aufgabe2:

        x_labels = []
        y_values = []

        for i in range (len(word)):
            print("pos ",i+1,"(",word[i],")",":")
            char_at_pos = WordDataSet["Wort"].str[i]
            pos_counts = char_at_pos.value_counts()
            target_char = word[i]
            target_count = pos_counts.get(target_char, 0)
            
            if target_count == 0:
                log_cal2 = 0
            else:
                calculation2 = num_lines/target_count
                log_cal2 = np.log2(calculation2)
                
            print(log_cal2)

            x_labels.append(target_char)
            y_values.append(log_cal2)

            # print(target_count)
            # print(f"--- Position {i+1} ---")
            # print(f"Most common letters:\n{pos_counts.head(3).to_string()}")
            # print(f"Occurrences of '{target_char}': {target_count} ({(target_count/WordDataSet_lines)*100:.2f}%)\n")
            
        plt.figure(2)
        plt.bar(range(len(x_labels)), y_values, tick_label=x_labels)
        plt.xlabel("Buchstaben")
        plt.ylabel("Information")
        
    if Aufgabe3:
        if forward:
            x_labels = []
            y_values = []
            for i in range(len(word)):
                if i == 0:

                    char_at_pos = WordDataSet["Wort"].str[i]
                    pos_counts = char_at_pos.value_counts()
                    target_char = word[i]
                    target_count = pos_counts.get(target_char, 0)
                    # print("Char at Position i: ",char_at_pos)
                    # print("Pos Counts: ", pos_counts)
                    # print("Target Char: ",target_char)
                    # print("Target Count:",target_count)
                    OrakelXyl = WordDataSet.loc[WordDataSet["Wort"].str[i] == target_char]
                    # OrakelXyl = df.loc[pos_counts["char_count"] == target_char, ["Wort"]]
                    # print("ORAKEL:", OrakelXyl)
                    OrakelXylLen = len(OrakelXyl)
                    LogOrakelXylLen = np.log2(len(WordDataSet)/OrakelXylLen)
                    x_labels.append(target_char)
                    y_values.append(LogOrakelXylLen)
                    print("Orakel Länge: ", OrakelXylLen)
                    print("Informations Gewinn: ", LogOrakelXylLen)

                if i >= 1:
                    print("ORAKEL NACH I:", i, OrakelXyl)
                    char_at_pos = OrakelXyl["Wort"].str[i]
                    pos_counts = char_at_pos.value_counts()
                    target_char = word[i]
                    target_count = pos_counts.get(target_char, 0)

                    OrakelXyl = OrakelXyl.loc[WordDataSet["Wort"].str[i] == target_char]
                    OldXylLen = OrakelXylLen
                    OrakelXylLen = len(OrakelXyl)
                    if OrakelXylLen == 0:
                        print("Orakel wurde nicht fündig")
                        break
                    LogOrakelXylLen = np.log2(OldXylLen/OrakelXylLen)
                    x_labels.append(target_char)
                    y_values.append(LogOrakelXylLen)
                    print("Infromationsgewinn : ",LogOrakelXylLen)
                    if OrakelXylLen == 1:
                        print(OrakelXyl)
                        break
        else:
            x_labels = []
            y_values = []
            for i in range(len(word)-1,-1,-1):
                if i == len(word)-1:

                    char_at_pos = WordDataSet["Wort"].str[i]
                    pos_counts = char_at_pos.value_counts()
                    target_char = word[i]
                    target_count = pos_counts.get(target_char, 0)
                    # print("Char at Position i: ",char_at_pos)
                    # print("Pos Counts: ", pos_counts)
                    # print("Target Char: ",target_char)
                    # print("Target Count:",target_count)
                    OrakelXyl = WordDataSet.loc[WordDataSet["Wort"].str[i] == target_char]
                    # OrakelXyl = df.loc[pos_counts["char_count"] == target_char, ["Wort"]]
                    # print("ORAKEL:", OrakelXyl)
                    OrakelXylLen = len(OrakelXyl)
                    LogOrakelXylLen = np.log2(len(WordDataSet)/OrakelXylLen)
                    x_labels.append(target_char)
                    y_values.append(LogOrakelXylLen)
                    print("Orakel Länge: ", OrakelXylLen)
                    print("Informations Gewinn: ", LogOrakelXylLen)
                    print("#--------------------#")

                if i < len(word)-1:
                    char_at_pos = OrakelXyl["Wort"].str[i]
                    pos_counts = char_at_pos.value_counts()
                    target_char = word[i]
                    target_count = pos_counts.get(target_char, 0)
                    print("ORAKEL AN STELLE I:", i, OrakelXyl)
                    print("Target Character: ", target_char)

                    OrakelXyl = OrakelXyl.loc[WordDataSet["Wort"].str[i] == target_char]
                    OldXylLen = OrakelXylLen
                    OrakelXylLen = len(OrakelXyl)
                    if OrakelXylLen == 0:
                        print("Orakel wurde nicht fündig")
                        break
                    LogOrakelXylLen = np.log2(OldXylLen/OrakelXylLen)
                    x_labels.append(target_char)
                    y_values.append(LogOrakelXylLen)
                    print("Infromationsgewinn : ",LogOrakelXylLen)
                    print("#--------------------#")
                    if OrakelXylLen == 1:
                        print("Orakel wurde fündig")
                        print(OrakelXyl)
                        break
                    if OrakelXylLen < 1:
                        print("Orakel wurde nicht fündig")
                        break

        plt.figure(3)
        plt.bar(range(len(x_labels)), y_values, tick_label=x_labels)
        plt.xlabel("Buchstaben")
        plt.ylabel("Information")


    plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)