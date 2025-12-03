def solve_part_1(input_data):
    target = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    lines = input_data.strip().split('\n')

    for line in lines:
        parts = line.split(': ', 1)
        sue_num = int(parts[0].split()[1])

        properties_str = parts[1]
        properties = {}

        for prop_pair in properties_str.split(', '):
            prop_name, prop_value = prop_pair.split(': ')
            properties[prop_name] = int(prop_value)

        matches = True
        for prop, value in properties.items():
            if target[prop] != value:
                matches = False
                break

        if matches:
            return sue_num

    return None

def solve_part_2(input_data):
    target = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    lines = input_data.strip().split('\n')

    for line in lines:
        parts = line.split(': ', 1)
        sue_num = int(parts[0].split()[1])

        properties_str = parts[1]
        properties = {}

        for prop_pair in properties_str.split(', '):
            prop_name, prop_value = prop_pair.split(': ')
            properties[prop_name] = int(prop_value)

        matches = True
        for prop, value in properties.items():
            if prop in ['cats', 'trees']:
                if value <= target[prop]:
                    matches = False
                    break
            elif prop in ['pomeranians', 'goldfish']:
                if value >= target[prop]:
                    matches = False
                    break
            else:
                if target[prop] != value:
                    matches = False
                    break

        if matches:
            return sue_num

    return None
