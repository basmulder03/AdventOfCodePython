import hashlib

def solve_part_1(input_data):
    cleaned = input_data.strip()
    counter = 1
    while True:
        to_encode = cleaned + str(counter)
        encoded = hashlib.md5(to_encode.encode())
        # Check the first 3 bytes: first 2 must be 0, third must be < 16 (0x10)
        digest = encoded.digest()
        if digest[0] == 0 and digest[1] == 0 and digest[2] < 16:
            return counter
        counter += 1


def solve_part_2(input_data):
    cleaned = input_data.strip()
    counter = 1
    while True:
        to_encode = cleaned + str(counter)
        encoded = hashlib.md5(to_encode.encode())
        # Check the first 3 bytes: all must be 0
        digest = encoded.digest()
        if digest[0] == 0 and digest[1] == 0 and digest[2] == 0:
            return counter
        counter += 1
