import os
from preprocessor import preprocess_code
from parser import parser
from lexer import lexer

def main():
    filename = 'test2.py'  # Cambia aquí si quieres otro archivo
    test_path = os.path.join('tests', filename)

    if not os.path.isfile(test_path):
        print(f"Archivo {test_path} no encontrado.")
        return

    preprocessed_code = preprocess_code(test_path)
    print("=== Preprocessed Code ===")
    for i, line in enumerate(preprocessed_code):
        print(f"{i+1:02d}: {repr(line)}")
    

    result = parser.parse(''.join(preprocessed_code), lexer=lexer)
    print("\n=== Resultado del parser ===")
    print(result)

if __name__ == '__main__':
    main()
