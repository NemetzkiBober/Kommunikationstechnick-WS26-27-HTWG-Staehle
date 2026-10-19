def main() -> None:

    Terminal_Input = True
    Harcoded_Word = "hochschule"

    if Terminal_Input:
        word = input("Wort eingeben: ").upper()
    else:
        word = Harcoded_Word.upper()

    readDictionary = {}
    codeDictionary = {}
    
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
            #aaaaaaaaaaaabbbbbbcccccddddeeee


            
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
        add_Zero(left_dictionary)
        add_One(right_dictionary)

        print("Left: ",left_dictionary)
        print("Right: ",right_dictionary)
        if len(left_dictionary) > 1:
            break_dict(left_dictionary, sum(left_dictionary.values()))

        if len(right_dictionary) > 1:
            break_dict(right_dictionary, sum(right_dictionary.values()))
    

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

    def print_codes(codeDictionary):
        print("\n" + "=" * 30)
        print(f"{'Buchstabe':<12}{'Binärcode':<12}")
        print("-" * 30)

        for char, code in codeDictionary.items():
            print(f"{char:<12}{code:<12}")

        print("=" * 30)
        print("Code dictionary: ",codeDictionary)


    break_dict(probabilities, 1)
    print_codes(codeDictionary)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
