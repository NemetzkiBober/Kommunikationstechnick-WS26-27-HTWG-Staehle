import sys

class lempelZivWelch:
    def encode(self, message: str, CharL: list) -> str:
        local_CharL = CharL.copy()
        encoded_data = []
        current_sequence = ""
        
        for char in message:
            combined = current_sequence + char
            
            if combined in local_CharL:
                current_sequence = combined
            else:
                if len(current_sequence) == 1:
                    code = current_sequence
                else:
                    code = f"<{local_CharL.index(current_sequence)}>"

                encoded_data.append(code)
                local_CharL.append(combined) 
                print(f"Zeichen: {current_sequence: <5} | Code: {code: <5} | Neues Wortbuch-Element: {combined} (Index: {len(local_CharL)-1})")
                current_sequence = char
                
        if current_sequence:
            if len(current_sequence) == 1:
                code = current_sequence
            else:
                code = f"<{local_CharL.index(current_sequence)}>"

            encoded_data.append(code)
            print(f"Zeichen: {current_sequence: <5} | Code: {code: <5} | (Ende der Nachricht)")
            
        return "".join(encoded_data)

    def decode(self, bitstring: str, CharL: list) -> str:
        local_CharL = CharL.copy()
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
            current_sequence = local_CharL[token]
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
                if token < len(local_CharL):
                    current_sequence = local_CharL[token]
                else:
                    current_sequence = previous_sequence + previous_sequence[0]
            else:
                code_str = token
                current_sequence = token
                
            decoded_data += current_sequence
            
            new_entry = previous_sequence + current_sequence[0]
            local_CharL.append(new_entry)
            
            print(f"Code: {code_str: <5} | Decodiert: {current_sequence: <5} | Neues Wortbuch-Element: {new_entry} (Index: {len(local_CharL)-1})")
            
            previous_sequence = current_sequence
            
        return decoded_data


def main() -> None:
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

    # Instanziierung der Klasse (Punkt 1 behoben)
    lzw = lempelZivWelch()

    print("--- LZW Encoding Trace ---")
    
    # Methodenaufruf über die Instanz
    bitstring = lzw.encode(word, charL)
    print("--------------------------")
    print(f"\nFinaler Bitstring (Codierung): {bitstring}")
    
    print("\n--- LZW Decoding Trace ---")
    
    # Decodierung verwendet das initiale charL ohne erneutes `.copy()` vor dem Methodenaufruf, 
    # da die Methode selbst die Kopie erzeugt (Punkt 3 behoben)
    decoded_word = lzw.decode(bitstring, charL)
    print("--------------------------")
    print(f"\nDecodierte Nachricht: {decoded_word}")
    print(f"Erfolgreich decodiert: {word == decoded_word}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ausführung abgebrochen (SIGINT). Beende Prozess...")
        sys.exit(130)
