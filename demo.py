from functools import cache

@cache
def factorial(n):
    if n < 2:
        return 1

    return n * factorial(n - 1)


def main():
    print(factorial(5))
    print(factorial(10))
    print(factorial(7))
    print(factorial(70))
    print(factorial(50))
    print(factorial(491))
    print(factorial(700))
    print(factorial(999))


if __name__ == '__main__':
    main()