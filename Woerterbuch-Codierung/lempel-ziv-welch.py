class lempelZivWelch:
    def __init__(self):
        TerminalInput = 0
        HardcodedWord = "FISCHERSFRITZFISCHTFRISCHEFISCHE"
        
        if TerminalInput:
            word = input("Wort eingeben: ")
        else:
            word = HardcodedWord

        charL = []
        
        for i in range(len(word)):
            if word[i] not in charL:
                charL.append(word[i])
        # print(charL)


        def encode(message, CharL):

            iterator = iter(range(len(message)-1))
            for i in iterator:
                Zeichen = message[i:]
                if Zeichen in CharL:
                    print("Vorhanden: ", Zeichen)
                    nextIndex=len(Zeichen)
                    CharL.append(Zeichen+message[i+nextIndex])
                    next(iterator,None)
                    print("I: ",i)
                    print("---------------------------")
                else:
                    message[i:-1]
                    CharL.append(Zeichen)
                    print("Appended: ", Zeichen)
                    print("I: ",i)
                    print("---------------------------")
                # print(CharL)
                # print("---------------------------")
        #
        #
        #
        # def decode(bitstring,CharL):
        encode(word,charL)



def main() -> None:
   tmp = lempelZivWelch()
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
