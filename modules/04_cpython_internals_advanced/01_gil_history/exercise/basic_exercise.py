"""
BASIC EXERCISE: Comparison Threading vs Multiprocessing

Objective:
Implement a program that finds prime numbers in a range using:
1. Sequential execution
2. Threading (multiple threads)
3. Multiprocessing (multiple processes)

Measure and compare the performance of each approach.

Tasks:
1. Implement an efficient is_prime(n) function
2. Implement the find_primes_in_range(start, end) function
3. Run with 1, 2, 4, 8 workers for threading and multiprocessing
4. Measure execution times
5. Calculate and display speedup
6. Create a results chart (optional: use matplotlib)

Test data:
- Range: 1,000,000 - 1,100,000
- Split into 4 equal chunks

Success criteria:
✅ is_prime() works correctly for all cases
✅ Finds the same primes in all approaches
✅ Multiprocessing shows speedup > 2x on a CPU with 4+ cores
✅ Threading shows speedup < 1.5x (limited by the GIL)
✅ Clear report with conclusions

Estimated time: 45-60 minutes
"""

import multiprocessing as mp


def is_prime(n: int) -> bool:
    """
    TODO: Implement an efficient function to check whether n is prime.

    Hints:
    - Numbers smaller than 2 are not prime
    - You only need to check up to sqrt(n)
    - Optimization: check only odd divisors after 2

    Args:
        n: Number to check

    Returns:
        True if n is prime, False otherwise
    """
    pass  # YOUR CODE HERE


def find_primes_in_range(start: int, end: int) -> list[int]:
    """
    TODO: Find all prime numbers in the range [start, end).

    Args:
        start: Start of the range (inclusive)
        end: End of the range (exclusive)

    Returns:
        List of prime numbers in the range
    """
    pass  # YOUR CODE HERE


def sequential_execution(ranges: list[tuple[int, int]]) -> tuple[list[int], float]:
    """
    TODO: Run prime searching sequentially.

    Args:
        ranges: List of tuples (start, end) to search for primes

    Returns:
        Tuple (list_of_primes, execution_time)
    """
    pass  # YOUR CODE HERE


def threading_execution(ranges: list[tuple[int, int]], num_threads: int) -> tuple[list[int], float]:
    """
    TODO: Run prime searching using threading.

    Hints:
    - Create one Thread per range
    - Use a shared list for results (with a lock if needed)
    - Join all threads before returning

    Args:
        ranges: List of tuples (start, end) to search for primes
        num_threads: Number of threads to use

    Returns:
        Tuple (list_of_primes, execution_time)
    """
    pass  # YOUR CODE HERE


def multiprocessing_execution(
    ranges: list[tuple[int, int]], num_processes: int
) -> tuple[list[int], float]:
    """
    TODO: Run prime searching using multiprocessing.

    Hints:
    - Use multiprocessing.Pool
    - Use pool.starmap() to pass multiple arguments
    - Do not forget to close and join the pool

    Args:
        ranges: List of tuples (start, end) to search for primes
        num_processes: Number of processes to use

    Returns:
        Tuple (list_of_primes, execution_time)
    """
    pass  # YOUR CODE HERE


def main():
    """
    TODO: Implement the main function that:
    1. Defines the search range (1,000,000 - 1,100,000)
    2. Splits the range into 4 chunks
    3. Runs sequential, threading (1,2,4,8), multiprocessing (1,2,4,8)
    4. Shows results in a formatted table
    5. Calculates and displays speedup
    6. Draws conclusions
    """
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    # Required for Windows
    mp.freeze_support()
    main()


# SELF-VERIFICATION SECTION
# Uncomment to verify your implementation:

# def test_is_prime():
#     assert is_prime(2) == True
#     assert is_prime(3) == True
#     assert is_prime(4) == False
#     assert is_prime(17) == True
#     assert is_prime(100) == False
#     assert is_prime(1009) == True
#     print("✅ test_is_prime passed")

# def test_find_primes():
#     primes = find_primes_in_range(10, 20)
#     expected = [11, 13, 17, 19]
#     assert primes == expected, f"Expected {expected}, got {primes}"
#     print("✅ test_find_primes passed")

# if __name__ == "__main__":
#     test_is_prime()
#     test_find_primes()
#     main()
