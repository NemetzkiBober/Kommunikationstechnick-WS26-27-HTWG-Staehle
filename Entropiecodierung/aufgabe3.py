def main() -> None:

    Terminal_Input = False
    Harcoded_Word = "hochschule"

    if Terminal_Input:
        word = input("Wort eingeben: ").upper()
    else:
        word = Harcoded_Word.upper()

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
    
    fullprob = 1

    def break_dict(dictionary,fullprob):
        prob = 0
        pivot = 0
        for i in dictionary:
            prob = round(dictionary[i] + prob, 4)
            if prob == 0:
                break
            if prob >= fullprob/2:
                pivot = i
                break
        left_dictionary = {}
        right_dictionary = {}

        print("Pivot pre for: ",pivot)
        passed_pivot = False
        for i in dictionary:
            if not passed_pivot:
                left_dictionary[i] = dictionary[i]
                if i == pivot:
                    passed_pivot = True
            else:
                right_dictionary[i] = dictionary[i] 

        print("Left: ",left_dictionary)
        print("Right: ",right_dictionary)
    break_dict(sortedDictionary, 10)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
