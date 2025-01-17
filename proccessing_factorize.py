from multiprocessing import cpu_count, Pool, current_process
from time import time
import logging


def factorize(number: int):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    numbers = (128, 255, 99999, 10651060)

    start_time = time()

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(factorize, numbers)
        logging.info(f"{current_process().name} get Factorized numbers: {results}")

    a, b, c, d = results

    finish_time = time()
    logging.info(f"Factorization took {finish_time - start_time:.2f} seconds")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
