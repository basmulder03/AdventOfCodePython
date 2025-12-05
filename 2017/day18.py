from collections import defaultdict, deque


def solve_part_1(input_data):
    """Duet - find first recovered frequency."""
    lines = input_data.strip().split('\n')
    registers = defaultdict(int)
    last_sound = 0
    pc = 0

    def get_value(x):
        if x.lstrip('-').isdigit():
            return int(x)
        return registers[x]

    while 0 <= pc < len(lines):
        parts = lines[pc].split()
        cmd = parts[0]

        if cmd == 'snd':
            last_sound = get_value(parts[1])
        elif cmd == 'set':
            registers[parts[1]] = get_value(parts[2])
        elif cmd == 'add':
            registers[parts[1]] += get_value(parts[2])
        elif cmd == 'mul':
            registers[parts[1]] *= get_value(parts[2])
        elif cmd == 'mod':
            registers[parts[1]] %= get_value(parts[2])
        elif cmd == 'rcv':
            if get_value(parts[1]) != 0:
                return last_sound
        elif cmd == 'jgz':
            if get_value(parts[1]) > 0:
                pc += get_value(parts[2])
                continue

        pc += 1

    return last_sound


def solve_part_2(input_data):
    """Duet - count sends from program 1."""
    lines = [line.split() for line in input_data.strip().split('\n')]

    # Two programs
    registers = [defaultdict(int), defaultdict(int)]
    registers[0]['p'] = 0
    registers[1]['p'] = 1

    queues = [deque(), deque()]
    pcs = [0, 0]
    waiting = [False, False]
    send_count = 0

    def get_value(prog_id, x):
        if x.lstrip('-').isdigit():
            return int(x)
        return registers[prog_id][x]

    def run_program(prog_id):
        nonlocal send_count
        regs = registers[prog_id]
        queue = queues[prog_id]
        other_queue = queues[1 - prog_id]

        while 0 <= pcs[prog_id] < len(lines):
            parts = lines[pcs[prog_id]]
            cmd = parts[0]

            if cmd == 'snd':
                value = get_value(prog_id, parts[1])
                other_queue.append(value)
                if prog_id == 1:
                    send_count += 1
                waiting[1 - prog_id] = False  # Wake up other program
            elif cmd == 'set':
                regs[parts[1]] = get_value(prog_id, parts[2])
            elif cmd == 'add':
                regs[parts[1]] += get_value(prog_id, parts[2])
            elif cmd == 'mul':
                regs[parts[1]] *= get_value(prog_id, parts[2])
            elif cmd == 'mod':
                regs[parts[1]] %= get_value(prog_id, parts[2])
            elif cmd == 'rcv':
                if queue:
                    regs[parts[1]] = queue.popleft()
                else:
                    waiting[prog_id] = True
                    return  # Block this program
            elif cmd == 'jgz':
                if get_value(prog_id, parts[1]) > 0:
                    pcs[prog_id] += get_value(prog_id, parts[2])
                    continue

            pcs[prog_id] += 1

    # Run programs until both are waiting
    while True:
        old_waiting = waiting[:]

        if not waiting[0]:
            run_program(0)
        if not waiting[1]:
            run_program(1)

        # If both programs are waiting and no progress was made
        if waiting[0] and waiting[1] and waiting == old_waiting:
            break

    return send_count
