def solve_part_1(input_data):
    instructions = parse_instructions(input_data)
    wires = {}

    def get_signal(wire_or_value):
        if wire_or_value.isdigit():
            return int(wire_or_value)
        else:
            if wire_or_value not in wires:
                evaluate_wire(wire_or_value, instructions, wires)
            return wires[wire_or_value]

    def evaluate_wire(target_wire, instructions, wires):
        if target_wire in wires:
            return wires[target_wire]

        instruction = instructions[target_wire]

        if instruction['type'] == 'ASSIGN':
            wires[target_wire] = get_signal(instruction['input'])
        elif instruction['type'] == 'AND':
            wires[target_wire] = get_signal(instruction['left']) & get_signal(instruction['right'])
        elif instruction['type'] == 'OR':
            wires[target_wire] = get_signal(instruction['left']) | get_signal(instruction['right'])
        elif instruction['type'] == 'LSHIFT':
            wires[target_wire] = get_signal(instruction['input']) << instruction['shift']
        elif instruction['type'] == 'RSHIFT':
            wires[target_wire] = get_signal(instruction['input']) >> instruction['shift']
        elif instruction['type'] == 'NOT':
            wires[target_wire] = (~get_signal(instruction['input'])) & 0xFFFF  # 16-bit complement

        return wires[target_wire]

    return get_signal('a')

def solve_part_2(input_data):
    """
    Override wire b with the signal from wire a from part 1, then recalculate wire a
    """
    # First, get the signal from wire a in part 1
    signal_a = solve_part_1(input_data)

    # Parse instructions again
    instructions = parse_instructions(input_data)

    # Override wire b with the signal from part 1
    instructions['b'] = {'type': 'ASSIGN', 'input': str(signal_a)}

    # Reset and recalculate
    wires = {}

    def get_signal(wire_or_value):
        if wire_or_value.isdigit():
            return int(wire_or_value)
        else:
            if wire_or_value not in wires:
                evaluate_wire(wire_or_value, instructions, wires)
            return wires[wire_or_value]

    def evaluate_wire(target_wire, instructions, wires):
        if target_wire in wires:
            return wires[target_wire]

        instruction = instructions[target_wire]

        if instruction['type'] == 'ASSIGN':
            wires[target_wire] = get_signal(instruction['input'])
        elif instruction['type'] == 'AND':
            wires[target_wire] = get_signal(instruction['left']) & get_signal(instruction['right'])
        elif instruction['type'] == 'OR':
            wires[target_wire] = get_signal(instruction['left']) | get_signal(instruction['right'])
        elif instruction['type'] == 'LSHIFT':
            wires[target_wire] = get_signal(instruction['input']) << instruction['shift']
        elif instruction['type'] == 'RSHIFT':
            wires[target_wire] = get_signal(instruction['input']) >> instruction['shift']
        elif instruction['type'] == 'NOT':
            wires[target_wire] = (~get_signal(instruction['input'])) & 0xFFFF  # 16-bit complement

        return wires[target_wire]

    return get_signal('a')

def parse_instructions(input_data):
    instructions = {}

    for line in input_data.strip().split('\n'):
        parts = line.split(' -> ')
        output_wire = parts[1]
        instruction_part = parts[0]

        if ' AND ' in instruction_part:
            left, right = instruction_part.split(' AND ')
            instructions[output_wire] = {'type': 'AND', 'left': left, 'right': right}
        elif ' OR ' in instruction_part:
            left, right = instruction_part.split(' OR ')
            instructions[output_wire] = {'type': 'OR', 'left': left, 'right': right}
        elif ' LSHIFT ' in instruction_part:
            input_wire, shift_amount = instruction_part.split(' LSHIFT ')
            instructions[output_wire] = {'type': 'LSHIFT', 'input': input_wire, 'shift': int(shift_amount)}
        elif ' RSHIFT ' in instruction_part:
            input_wire, shift_amount = instruction_part.split(' RSHIFT ')
            instructions[output_wire] = {'type': 'RSHIFT', 'input': input_wire, 'shift': int(shift_amount)}
        elif instruction_part.startswith('NOT '):
            input_wire = instruction_part[4:]  # Remove "NOT "
            instructions[output_wire] = {'type': 'NOT', 'input': input_wire}
        else:
            # Simple assignment
            instructions[output_wire] = {'type': 'ASSIGN', 'input': instruction_part}

    return instructions