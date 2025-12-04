def increment_password(password):
    """Increment password like counting: xx, xy, xz, ya, yb, etc."""
    password = list(password)
    i = len(password) - 1

    while i >= 0:
        if password[i] == 'z':
            password[i] = 'a'
            i -= 1
        else:
            password[i] = chr(ord(password[i]) + 1)
            # Skip forbidden letters
            if password[i] in 'iol':
                password[i] = chr(ord(password[i]) + 1)
                # Set all following characters to 'a'
                for j in range(i + 1, len(password)):
                    password[j] = 'a'
            break

    return ''.join(password)

def has_straight(password):
    """Check if password has increasing straight of at least 3 letters."""
    for i in range(len(password) - 2):
        if (ord(password[i+1]) == ord(password[i]) + 1 and
            ord(password[i+2]) == ord(password[i]) + 2):
            return True
    return False

def has_forbidden_letters(password):
    """Check if password contains forbidden letters i, o, or l."""
    return any(letter in password for letter in 'iol')

def has_two_pairs(password):
    """Check if password has at least two different, non-overlapping pairs."""
    pairs = []
    i = 0
    while i < len(password) - 1:
        if password[i] == password[i+1]:
            pairs.append(password[i])
            i += 2  # Skip the pair to ensure non-overlapping
        else:
            i += 1

    return len(set(pairs)) >= 2

def is_valid_password(password):
    """Check if password meets all requirements."""
    # Check forbidden letters first (fastest check)
    if has_forbidden_letters(password):
        return False
    # Check pairs next (relatively fast)
    if not has_two_pairs(password):
        return False
    # Check straight last (most expensive)
    return has_straight(password)

def find_next_valid_password(password):
    """Find the next valid password after the given password."""
    password = increment_password(password)
    while not is_valid_password(password):
        password = increment_password(password)
    return password

def solve_part_1(input_data):
    current_password = input_data.strip()
    next_password = find_next_valid_password(current_password)
    return next_password

def solve_part_2(input_data):
    current_password = input_data.strip()
    # First, find the next valid password (Part 1 answer)
    first_next = find_next_valid_password(current_password)
    # Then find the next valid password after that
    second_next = find_next_valid_password(first_next)
    return second_next
