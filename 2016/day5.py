from typing import Any
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools


def solve_part_1(input_data: str) -> Any:
    d = input_data.strip().encode()
    pw = []

    def check_batch(start_idx, batch_size=10000):
        """Check a batch of indices for valid hashes"""
        results = []
        for i in range(start_idx, start_idx + batch_size):
            h = hashlib.md5(d + str(i).encode()).hexdigest()
            if h[:5] == '00000':
                results.append((i, h[5]))
        return results

    batch_size = 50000
    start_idx = 0

    with ThreadPoolExecutor(max_workers=4) as executor:
        while len(pw) < 8:
            # Submit multiple batches for parallel processing
            futures = []
            for batch_start in range(start_idx, start_idx + batch_size * 4, batch_size):
                future = executor.submit(check_batch, batch_start, batch_size)
                futures.append(future)

            # Collect results as they complete
            all_results = []
            for future in as_completed(futures):
                all_results.extend(future.result())

            # Sort by index and take the first valid hashes
            all_results.sort()
            for idx, char in all_results:
                if len(pw) < 8:
                    pw.append(char)
                    if len(pw) == 8:
                        break

            start_idx += batch_size * 4

    return ''.join(pw)


def solve_part_2(input_data: str) -> Any:
    d = input_data.strip().encode()
    pw = [''] * 8
    filled = 0

    def check_batch_part2(start_idx, batch_size=10000):
        """Check a batch of indices for valid positional hashes"""
        results = []
        for i in range(start_idx, start_idx + batch_size):
            h = hashlib.md5(d + str(i).encode()).hexdigest()
            if h[:5] == '00000':
                pos_char = h[5]
                if '0' <= pos_char <= '7':
                    pos = int(pos_char)
                    results.append((i, pos, h[6]))
        return results

    batch_size = 50000
    start_idx = 0

    with ThreadPoolExecutor(max_workers=4) as executor:
        while filled < 8:
            # Submit multiple batches for parallel processing
            futures = []
            for batch_start in range(start_idx, start_idx + batch_size * 4, batch_size):
                future = executor.submit(check_batch_part2, batch_start, batch_size)
                futures.append(future)

            # Collect results as they complete
            all_results = []
            for future in as_completed(futures):
                all_results.extend(future.result())

            # Sort by index and fill positions in order
            all_results.sort()
            for idx, pos, char in all_results:
                if pw[pos] == '':
                    pw[pos] = char
                    filled += 1
                    if filled == 8:
                        break

            start_idx += batch_size * 4

    return ''.join(pw)

