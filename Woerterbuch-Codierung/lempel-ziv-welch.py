import sys

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


        def encode(message, CharL):
            """
            Implements LZW encoding strictly using the provided CharL list.
            Includes a simple, readable print trace without complex formatting logic.
            """
            encoded_data = []
            current_sequence = ""
            
            for char in message:
                combined = current_sequence + char
                
                if combined in CharL:
                    # Sequence exists in the list, extend it
                    current_sequence = combined
                else:
                    # Output the list index for the known sequence
                    code = CharL.index(current_sequence)
                    encoded_data.append(code)
                    
                    # Add new combined sequence to the external state list
                    CharL.append(combined) 
                    
                    # Simple trace output
                    print(f"Zeichen: {current_sequence: <5} | Code: {code: <3} | Neues Wortbuch-Element: {combined} (Index: {len(CharL)-1})")
                    
                    # Reset the current sequence to the unmatched character
                    current_sequence = char
                    
            # Flush the final remaining sequence buffer
            if current_sequence:
                code = CharL.index(current_sequence)
                encoded_data.append(code)
                print(f"Zeichen: {current_sequence: <5} | Code: {code: <3} | (Ende der Nachricht)")
                
            return encoded_data

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
