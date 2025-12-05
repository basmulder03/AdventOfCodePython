def solve_part_1(input_data):
    """Turing machine - count checksum after 12,317,297 steps."""
    lines = input_data.strip().split('\n')

    # Parse the input to extract states and rules
    # This is a general parser for Turing machine descriptions

    # Find initial state
    initial_state = None
    steps = 0

    for line in lines:
        if "Begin in state" in line:
            initial_state = line.split()[-1].rstrip('.')
        elif "Perform a diagnostic checksum after" in line:
            steps = int(''.join(filter(str.isdigit, line)))

    # Parse states
    states = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("In state"):
            state_name = line.split()[-1].rstrip(':')
            states[state_name] = {}
            i += 1

            # Parse the two conditions (0 and 1)
            for value in [0, 1]:
                # Skip to "If the current value is X:"
                while i < len(lines) and f"If the current value is {value}" not in lines[i]:
                    i += 1
                i += 1  # Skip the condition line

                # Parse write value
                write_line = lines[i].strip()
                write_value = int(write_line.split()[-1].rstrip('.'))
                i += 1

                # Parse move direction
                move_line = lines[i].strip()
                move_dir = 1 if "right" in move_line else -1
                i += 1

                # Parse next state
                next_line = lines[i].strip()
                next_state = next_line.split()[-1].rstrip('.')
                i += 1

                states[state_name][value] = (write_value, move_dir, next_state)
        else:
            i += 1

    # Run the Turing machine
    tape = {}
    position = 0
    current_state = initial_state

    for step in range(steps):
        current_value = tape.get(position, 0)
        write_value, move_dir, next_state = states[current_state][current_value]

        tape[position] = write_value
        position += move_dir
        current_state = next_state

    # Count 1s on the tape
    return sum(1 for value in tape.values() if value == 1)


def solve_part_2(input_data):
    """Part 2 is usually just getting all 49 stars."""
    return "Congratulations! All 2017 puzzles completed!"

