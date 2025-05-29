import os

# Patrones que NO se soportan
ILLEGAL_PATTERNS = [
    'f"', "f'", '>=', '<=', '!=', '**', '//', '#', '+=', '-=', 'print(', 'if ', 'else:'
]

def is_illegal_line(line):
    return any(p in line for p in ILLEGAL_PATTERNS)

def get_indent_level(line):
    return len(line) - len(line.lstrip(' '))

def preprocess_code(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    processed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        indent = get_indent_level(line)

        # Quitar comentarios inline
        comment_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]

        if is_illegal_line(line):
            print(f"Ignoring unsupported line {i+1}: {stripped}")
            if stripped.endswith(':'):
                block_indent = indent
                i += 1
                while i < len(lines) and get_indent_level(lines[i]) > block_indent:
                    print(f"Ignoring line {i+1} inside unsupported block: {lines[i].strip()}")
                    i += 1
            else:
                i += 1
            continue

        if stripped.startswith(('def ', 'class ')) and stripped.endswith(':'):
            lookahead = i + 1
            while lookahead < len(lines) and lines[lookahead].strip() == '':
                lookahead += 1

            if lookahead >= len(lines) or get_indent_level(lines[lookahead]) <= indent:
                print(f"Ignoring orphan definition on line {i+1}: {stripped}")
                i += 1
                continue
            else:
                block_indent = indent
                body_ok = False
                j = i + 1
                while j < len(lines) and get_indent_level(lines[j]) > block_indent:
                    if not is_illegal_line(lines[j]):
                        body_ok = True
                        break
                    j += 1
                if not body_ok:
                    print(f"Ignoring definition on line {i+1} due to unsupported body")
                    i = j
                    continue

        # Línea aceptada
        processed_lines.append(line)
        if stripped.startswith(('def ', 'class ')) and stripped.endswith(':'):
            processed_lines.append('\n')  # <-- Esto es lo nuevo
        i += 1

    # Eliminar líneas vacías finales
    processed_lines = [line for line in processed_lines if line.strip()]

    return processed_lines
