from typing import Any
import hashlib
import re
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

TRIPLET_PATTERN = re.compile(r'(.)\1\1')

def solve_part_1(input_data: str) -> Any:
    s = input_data.strip().encode()
    hash_cache = {}

    def compute_hash_batch(start, count):
        """Compute a batch of hashes"""
        batch = {}
        for n in range(start, start + count):
            batch[n] = hashlib.md5(s + str(n).encode()).hexdigest()
        return batch

    def get_hash(n):
        if n not in hash_cache:
            # Compute in batches when cache miss
            batch_start = (n // 1000) * 1000
            batch = compute_hash_batch(batch_start, 1000)
            hash_cache.update(batch)
        return hash_cache[n]

    keys = []
    i = 0

    # Pre-populate cache for efficiency
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Start with initial batches
        futures = []
        for batch_start in range(0, 10000, 1000):
            future = executor.submit(compute_hash_batch, batch_start, 1000)
            futures.append((batch_start, future))

        for batch_start, future in futures:
            hash_cache.update(future.result())

    while len(keys) < 64:
        # Ensure we have enough cached hashes ahead
        max_needed = i + 1000
        if max_needed > max(hash_cache.keys(), default=0):
            with ThreadPoolExecutor(max_workers=2) as executor:
                batch_start = max(hash_cache.keys(), default=0) + 1
                future = executor.submit(compute_hash_batch, batch_start, 2000)
                hash_cache.update(future.result())

        h = get_hash(i)
        m = TRIPLET_PATTERN.search(h)
        if m:
            c = m.group(1)
            quintuple = c * 5
            for j in range(i+1, i+1001):
                if quintuple in get_hash(j):
                    keys.append(i)
                    break
        i += 1

    return keys[63]


def solve_part_2(input_data: str) -> Any:
    s = input_data.strip()
    cache = {}

    def compute_stretched_hash_batch(start, count):
        """Compute a batch of stretched hashes"""
        batch = {}
        for n in range(start, start + count):
            h = (s + str(n)).encode()
            for _ in range(2017):
                h = hashlib.md5(h).hexdigest().encode()
            batch[n] = h.decode()
        return batch

    def get_stretched_hash(n):
        if n not in cache:
            # Compute in batches
            batch_start = (n // 100) * 100
            batch = compute_stretched_hash_batch(batch_start, 100)
            cache.update(batch)
        return cache[n]

    keys = []
    i = 0

    # Pre-populate initial cache
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for batch_start in range(0, 2000, 100):
            future = executor.submit(compute_stretched_hash_batch, batch_start, 100)
            futures.append(future)

        for future in futures:
            cache.update(future.result())

    while len(keys) < 64:
        # Ensure we have enough cached hashes ahead
        max_needed = i + 1000
        if max_needed > max(cache.keys(), default=0):
            with ThreadPoolExecutor(max_workers=2) as executor:
                batch_start = max(cache.keys(), default=0) + 1
                future = executor.submit(compute_stretched_hash_batch, batch_start, 500)
                cache.update(future.result())

        h = get_stretched_hash(i)
        m = TRIPLET_PATTERN.search(h)
        if m:
            c = m.group(1)
            quintuple = c * 5
            for j in range(i+1, i+1001):
                if quintuple in get_stretched_hash(j):
                    keys.append(i)
                    break
        i += 1

    return keys[63]

