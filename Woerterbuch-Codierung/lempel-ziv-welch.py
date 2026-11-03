import sys

class lempelZivWelch:
    def __init__(self):
        TerminalInput = 1
        HardcodedWord = "FISCHERSFRITZFISCHTFRISCHEFISCHE"
        
        if TerminalInput:
            word = input("Wort eingeben: ")
        else:
            word = HardcodedWord

        charL = []
        
        for i in range(len(word)):
            if word[i] not in charL:
                charL.append(word[i])


        def encode(message, CharL):
            encoded_data = []
            current_sequence = ""
            
            for char in message:
                combined = current_sequence + char
                
                if combined in CharL:

                    current_sequence = combined
                else:

                    if len(current_sequence) == 1:
                        code = current_sequence
                    else:
                        code = f"<{CharL.index(current_sequence)}>"


                    encoded_data.append(code)
                    
                    CharL.append(combined) 
                    
                    print(f"Zeichen: {current_sequence: <5} | Code: {code: <3} | Neues Wortbuch-Element: {combined} (Index: {len(CharL)-1})")
                    
                    current_sequence = char
                    
            if current_sequence:
                if len(current_sequence) == 1:
                    code = current_sequence
                else:
                    code = f"<{CharL.index(current_sequence)}>"

                encoded_data.append(code)
                print(f"Zeichen: {current_sequence: <5} | Code: {code: <3} | (Ende der Nachricht)")
                
            return "".join(encoded_data)

        # def decode(bitstring,CharL):
        
        print("--- LZW Encoding Trace ---")
        bitstring = encode(word, charL)
        print("--------------------------")
        print(f"\nFinaler Bitstring (Codierung): {bitstring}")
        print(f"Wörterbuchgröße am Ende: {len(charL)}")


def main() -> None:
   tmp = lempelZivWelch()
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
