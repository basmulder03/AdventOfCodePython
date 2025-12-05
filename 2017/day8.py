def solve_part_1(input_data):
    """Execute register instructions and find largest value."""
    lines = input_data.strip().split('\n')
    registers = {}

    for line in lines:
        parts = line.split()
        reg = parts[0]
        op = parts[1]
        amount = int(parts[2])
        cond_reg = parts[4]
        cond_op = parts[5]
        cond_val = int(parts[6])

        # Initialize registers
        if reg not in registers:
            registers[reg] = 0
        if cond_reg not in registers:
            registers[cond_reg] = 0

        # Check condition
        condition_met = False
        if cond_op == '>':
            condition_met = registers[cond_reg] > cond_val
        elif cond_op == '<':
            condition_met = registers[cond_reg] < cond_val
        elif cond_op == '>=':
            condition_met = registers[cond_reg] >= cond_val
        elif cond_op == '<=':
            condition_met = registers[cond_reg] <= cond_val
        elif cond_op == '==':
            condition_met = registers[cond_reg] == cond_val
        elif cond_op == '!=':
            condition_met = registers[cond_reg] != cond_val

        # Execute instruction if condition is met
        if condition_met:
            if op == 'inc':
                registers[reg] += amount
            elif op == 'dec':
                registers[reg] -= amount

    return max(registers.values())


def solve_part_2(input_data):
    """Find highest value held in any register during execution."""
    lines = input_data.strip().split('\n')
    registers = {}
    max_value = float('-inf')

    for line in lines:
        parts = line.split()
        reg = parts[0]
        op = parts[1]
        amount = int(parts[2])
        cond_reg = parts[4]
        cond_op = parts[5]
        cond_val = int(parts[6])

        # Initialize registers
        if reg not in registers:
            registers[reg] = 0
        if cond_reg not in registers:
            registers[cond_reg] = 0

        # Check condition
        condition_met = False
        if cond_op == '>':
            condition_met = registers[cond_reg] > cond_val
        elif cond_op == '<':
            condition_met = registers[cond_reg] < cond_val
        elif cond_op == '>=':
            condition_met = registers[cond_reg] >= cond_val
        elif cond_op == '<=':
            condition_met = registers[cond_reg] <= cond_val
        elif cond_op == '==':
            condition_met = registers[cond_reg] == cond_val
        elif cond_op == '!=':
            condition_met = registers[cond_reg] != cond_val

        # Execute instruction if condition is met
        if condition_met:
            if op == 'inc':
                registers[reg] += amount
            elif op == 'dec':
                registers[reg] -= amount

            # Track maximum value
            max_value = max(max_value, registers[reg])

    return max_value

