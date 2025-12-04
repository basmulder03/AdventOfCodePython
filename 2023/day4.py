def solve_part_1(input_data):
    lines = [line for line in input_data.split("\n") if line.strip()]
    total_score = 0

    for line in lines:
        card_number, both_cards = line.strip().split(": ")
        winning_numbers_str, scratched_numbers_str = both_cards.split(" | ")
        winning_numbers = set(wn for wn in winning_numbers_str.split() if wn)
        scratched_numbers = set(sn for sn in scratched_numbers_str.split() if sn)

        matches = len(winning_numbers & scratched_numbers)
        if matches > 0:
            total_score += 2 ** (matches - 1)

    return total_score
   


def solve_part_2(input_data):
    lines = [line for line in input_data.split("\n") if line.strip()]

    # Calculate matches for each card
    matches_per_card = []
    for line in lines:
        card_number, both_cards = line.strip().split(": ")
        winning_numbers_str, scratched_numbers_str = both_cards.split(" | ")
        winning_numbers = set(wn for wn in winning_numbers_str.split() if wn)
        scratched_numbers = set(sn for sn in scratched_numbers_str.split() if sn)
        matches = len(winning_numbers & scratched_numbers)
        matches_per_card.append(matches)

    # Count total cards using iterative approach
    card_counts = [1] * len(matches_per_card)  # Each original card counts as 1

    for i, matches in enumerate(matches_per_card):
        # For each copy of card i, add copies of the next 'matches' cards
        for j in range(i + 1, min(i + 1 + matches, len(card_counts))):
            card_counts[j] += card_counts[i]

    return sum(card_counts)

    
    
    