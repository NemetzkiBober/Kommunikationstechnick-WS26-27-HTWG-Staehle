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
                    print(f"Zeichen: {current_sequence: <5} | Code: {code: <5} | Neues Wortbuch-Element: {combined} (Index: {len(CharL)-1})")
                    current_sequence = char
                    
            if current_sequence:
                if len(current_sequence) == 1:
                    code = current_sequence
                else:
                    code = f"<{CharL.index(current_sequence)}>"

                encoded_data.append(code)
                print(f"Zeichen: {current_sequence: <5} | Code: {code: <5} | (Ende der Nachricht)")
                
            return "".join(encoded_data)


        def decode(bitstring, CharL):
            decoded_data = ""
            tokens = []
            i = 0
            
            while i < len(bitstring):
                if bitstring[i] == '<':
                    end_idx = bitstring.find('>', i)
                    tokens.append(int(bitstring[i+1:end_idx]))
                    i = end_idx + 1
                else:
                    tokens.append(bitstring[i])
                    i += 1
            
            if not tokens:
                return ""
            
            token = tokens[0]
            if isinstance(token, int):
                current_sequence = CharL[token]
                code_str = f"<{token}>"
            else:
                current_sequence = token
                code_str = token
                
            decoded_data += current_sequence
            previous_sequence = current_sequence
            
            print(f"Code: {code_str: <5} | Decodiert: {current_sequence: <5} | (Initialisierung)")
            
            for token in tokens[1:]:
                if isinstance(token, int):
                    code_str = f"<{token}>"
                    if token < len(CharL):
                        current_sequence = CharL[token]
                    else:
                        current_sequence = previous_sequence + previous_sequence[0]
                else:
                    code_str = token
                    current_sequence = token
                    
                decoded_data += current_sequence
                
                new_entry = previous_sequence + current_sequence[0]
                CharL.append(new_entry)
                
                print(f"Code: {code_str: <5} | Decodiert: {current_sequence: <5} | Neues Wortbuch-Element: {new_entry} (Index: {len(CharL)-1})")
                
                previous_sequence = current_sequence
                
            return decoded_data

        
        print("--- LZW Encoding Trace ---")
        
        initial_charL = charL.copy()
        
        bitstring = encode(word, charL)
        print("--------------------------")
        print(f"\nFinaler Bitstring (Codierung): {bitstring}")
        print(f"Wörterbuchgröße am Ende (Encoder): {len(charL)}")
        
        print("\n--- LZW Decoding Trace ---")
        decoded_word = decode(bitstring, initial_charL)
        print("--------------------------")
        print(f"\nDecodierte Nachricht: {decoded_word}")
        print(f"Wörterbuchgröße am Ende (Decoder): {len(initial_charL)}")
        print(f"Erfolgreich decodiert: {word == decoded_word}")


def main() -> None:
   lempelZivWelch()
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
