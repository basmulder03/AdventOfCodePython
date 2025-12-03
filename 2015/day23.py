from typing import Any, Dict, List


def execute_program(instructions: List[str], registers: Dict[str, int]) -> Dict[str, int]:
    """Execute the assembly-like program and return final register values."""
    pc = 0  # program counter

    while pc < len(instructions):
        instruction = instructions[pc].strip()
        parts = instruction.split()
        cmd = parts[0]

        if cmd == "hlf":
            # hlf r: sets register r to half its current value
            reg = parts[1]
            registers[reg] = registers[reg] // 2
            pc += 1

        elif cmd == "tpl":
            # tpl r: sets register r to triple its current value
            reg = parts[1]
            registers[reg] = registers[reg] * 3
            pc += 1

        elif cmd == "inc":
            # inc r: increments register r, adding 1 to it
            reg = parts[1]
            registers[reg] = registers[reg] + 1
            pc += 1

        elif cmd == "jmp":
            # jmp offset: jump offset instructions
            offset = int(parts[1])
            pc += offset

        elif cmd == "jie":
            # jie r, offset: jump if register r is even
            reg = parts[1].rstrip(',')
            offset = int(parts[2])
            if registers[reg] % 2 == 0:
                pc += offset
            else:
                pc += 1

        elif cmd == "jio":
            # jio r, offset: jump if register r is 1
            reg = parts[1].rstrip(',')
            offset = int(parts[2])
            if registers[reg] == 1:
                pc += offset
            else:
                pc += 1
        else:
            # Unknown instruction, skip
            pc += 1

    return registers


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    instructions = [line.strip() for line in input_data.strip().split('\n') if line.strip()]

    # Initialize registers
    registers = {'a': 0, 'b': 0}

    # Execute the program
    final_registers = execute_program(instructions, registers)

    # Return the value in register b
    return final_registers['b']


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    instructions = [line.strip() for line in input_data.strip().split('\n') if line.strip()]

    # For part 2, register a starts with value 1 instead of 0
    registers = {'a': 1, 'b': 0}

    # Execute the program
    final_registers = execute_program(instructions, registers)

    # Return the value in register b
    return final_registers['b']
