def solve_part_1(input_data):
    """Count valid passphrases (no duplicate words)."""
    lines = input_data.strip().split('\n')
    valid_count = 0

    for line in lines:
        words = line.split()
        if len(words) == len(set(words)):
            valid_count += 1

    return valid_count


def solve_part_2(input_data):
    """Count valid passphrases (no anagrams)."""
    lines = input_data.strip().split('\n')
    valid_count = 0

    for line in lines:
        words = line.split()
        # Sort letters in each word to check for anagrams
        sorted_words = [''.join(sorted(word)) for word in words]
        if len(sorted_words) == len(set(sorted_words)):
            valid_count += 1

    return valid_count
