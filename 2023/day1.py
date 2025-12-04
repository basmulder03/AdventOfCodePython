DIGITSMAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def solve_part_1(input_data):
    lines = input_data.split("\n")
    total_value = 0
    for line in lines:
        digits = [char for char in line.strip() if char.isdigit()] 
        if (len(digits) != 0):         
            total_value += int(digits[0] + digits[-1])
    return total_value

def solve_part_2(input_data):
    lines = input_data.split("\n")
    total_value = 0
    for line in lines:
        digits = []
        for index, char in enumerate(line):
            if char.isdigit():
                digits.append(int(char))
            for word, digit in DIGITSMAP.items():
                if line[index:].startswith(word):
                    digits.append(digit)
                    break
        if (len(digits) != 0):
            total_value += int(digits[0] + digits[-1])
    return total_value
    pass
                
            
            
        