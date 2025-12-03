def solve_part_1(input_data):
    lines = input_data.strip().split('\n')
    total_code_chars = 0
    total_memory_chars = 0

    for line in lines:
        # Count characters in code representation
        code_chars = len(line)
        total_code_chars += code_chars

        # Count characters in memory representation
        # Remove surrounding quotes and process escape sequences
        memory_string = line[1:-1]  # Remove outer quotes

        i = 0
        memory_chars = 0
        while i < len(memory_string):
            if memory_string[i] == '\\':
                if i + 1 < len(memory_string):
                    next_char = memory_string[i + 1]
                    if next_char == '\\' or next_char == '"':
                        # \\ or \" - represents one character
                        memory_chars += 1
                        i += 2
                    elif next_char == 'x':
                        # \xHH - hexadecimal escape sequence
                        memory_chars += 1
                        i += 4  # Skip \x and two hex digits
                    else:
                        # Just a backslash (shouldn't happen in valid input)
                        memory_chars += 1
                        i += 1
                else:
                    memory_chars += 1
                    i += 1
            else:
                memory_chars += 1
                i += 1

        total_memory_chars += memory_chars

    return total_code_chars - total_memory_chars

def solve_part_2(input_data):
    lines = input_data.strip().split('\n')
    total_original_chars = 0
    total_encoded_chars = 0

    for line in lines:
        # Count original characters
        original_chars = len(line)
        total_original_chars += original_chars

        # Count encoded characters
        # Start with surrounding quotes
        encoded_chars = 2  # Opening and closing quotes

        # Process each character in the original string
        for char in line:
            if char == '"':
                encoded_chars += 2  # " becomes \"
            elif char == '\\':
                encoded_chars += 2  # \ becomes \\
            else:
                encoded_chars += 1  # Regular character stays the same

        total_encoded_chars += encoded_chars

    return total_encoded_chars - total_original_chars
