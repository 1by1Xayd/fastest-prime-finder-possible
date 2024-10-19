import math
import os
from concurrent.futures import ProcessPoolExecutor
import time
# read more https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
def sieve_of_eratosthenes(start, end):
    if start < 2:
        start = 2
    is_prime = [True] * ((end - start) // 2 + 1)
    primes = []

    for i in range(3, int(math.sqrt(end)) + 1, 2):
        if i * i > end:
            break
        first_multiple = max(i * i, start + (i - start % i) % i)
        if first_multiple % 2 == 0:
            first_multiple += i

        for j in range(first_multiple, end + 1, i * 2):
            is_prime[(j - start) // 2] = False

    if start <= 2 <= end:
        primes.append(2)

    for i in range(len(is_prime)):
        if is_prime[i]:
            prime_number = 2 * i + start
            primes.append(prime_number)

    return primes

def process_range(r):
    return sieve_of_eratosthenes(r[0], r[1])

def find_primes(limit):
    num_processes = os.cpu_count()  # Get the number of CPU cores
    chunk_size = (limit - 2) // num_processes
    ranges = [(2 + i * chunk_size, min(2 + (i + 1) * chunk_size, limit)) for i in range(num_processes)]

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = executor.map(process_range, ranges)

    all_primes = []
    for prime_list in results:
        all_primes.extend(prime_list)

    return sorted(all_primes)

if __name__ == "__main__":
    limit = 500000000 # set as many as you want

    start_time = time.time()

    primes = find_primes(limit)

    end_time = time.time()
    # this shit can take up gigabytes of space, be careful
    with open("primes.txt", "w") as file:
        for prime in primes:
            file.write(f"{prime}\n")

    print(f"\nFound {len(primes)} prime numbers up to {limit}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
