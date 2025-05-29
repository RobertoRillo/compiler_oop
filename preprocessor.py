import os

# Lista de patrones que NO se soportan y deben filtrarse
ILLEGAL_PATTERNS = ['f"', "f'", '>=', '<=', '!=', '**', '//', '#']

def is_illegal_line(line):
    return any(p in line for p in ILLEGAL_PATTERNS)

def preprocess_code(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    processed_lines = []

    for lineno, line in enumerate(lines, start=1):
        # Remove comments
        comment_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]

        if not line.strip():
            continue
        if is_illegal_line(line):
            print(f"Ignoring unsupported line {lineno}: {line.strip()}")
            continue

        processed_lines.append(line)  # 👈 conserva indentación y \n

    return processed_lines
