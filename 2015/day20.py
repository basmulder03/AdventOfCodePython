def solve_part_1(input_data):
    target = int(input_data.strip())

    max_house = min(target // 20, 800000)

    presents = [0] * (max_house + 1)
    min_answer = max_house + 1

    batch_size = 5000
    for batch_start in range(1, max_house + 1, batch_size):
        batch_end = min(batch_start + batch_size, max_house + 1)

        for elf in range(batch_start, batch_end):
            if elf >= min_answer:
                break

            for house in range(elf, min(min_answer, max_house + 1), elf):
                presents[house] += 10 * elf

        check_end = min(batch_end * 2, min_answer, max_house + 1)
        for house in range(batch_start, check_end):
            if presents[house] >= target:
                min_answer = min(min_answer, house)
                break

        if min_answer < batch_end:
            return min_answer

    return min_answer if min_answer <= max_house else None

def solve_part_2(input_data):
    target = int(input_data.strip())

    max_house = min(target // 11, 1000000)

    presents = [0] * (max_house + 1)

    for elf in range(1, max_house + 1):
        visits = 0
        for house in range(elf, max_house + 1, elf):
            if visits >= 50:
                break
            presents[house] += 11 * elf
            visits += 1

        if elf % 5000 == 0:
            for house in range(1, min(elf * 60, max_house + 1)):
                if presents[house] >= target:
                    return house

    for house in range(1, max_house + 1):
        if presents[house] >= target:
            return house

    return None
