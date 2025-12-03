def solve_part_1(input_data):
    lines = input_data.strip().split('\n')

    replacements = []
    i = 0
    while i < len(lines) and lines[i].strip():
        if '=>' in lines[i]:
            from_elem, to_elem = lines[i].split(' => ')
            replacements.append((from_elem.strip(), to_elem.strip()))
        i += 1

    medicine = lines[-1].strip()

    possible_molecules = set()

    for from_elem, to_elem in replacements:
        start = 0
        while True:
            pos = medicine.find(from_elem, start)
            if pos == -1:
                break

            new_molecule = medicine[:pos] + to_elem + medicine[pos + len(from_elem):]
            possible_molecules.add(new_molecule)

            start = pos + 1

    return len(possible_molecules)

def solve_part_2(input_data):
    lines = input_data.strip().split('\n')

    replacements = []
    i = 0
    while i < len(lines) and lines[i].strip():
        if '=>' in lines[i]:
            from_elem, to_elem = lines[i].split(' => ')
            replacements.append((from_elem.strip(), to_elem.strip()))
        i += 1

    target_molecule = lines[-1].strip()

    reverse_replacements = [(to_elem, from_elem) for from_elem, to_elem in replacements]

    reverse_replacements.sort(key=lambda x: len(x[0]), reverse=True)

    current_molecule = target_molecule
    steps = 0

    while current_molecule != 'e':
        made_replacement = False
        for from_elem, to_elem in reverse_replacements:
            if from_elem in current_molecule:
                pos = current_molecule.find(from_elem)
                current_molecule = current_molecule[:pos] + to_elem + current_molecule[pos + len(from_elem):]
                steps += 1
                made_replacement = True
                break

        if not made_replacement:
            return -1

    return steps
