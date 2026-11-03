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
                charL.insert(len(charL),word[i])
        print(charL)
        # def encode(message, CharL):
        #
        #
        #
        # def decode(bitstring,CharL):



def main() -> None:
   tmp = lempelZivWelch()
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
