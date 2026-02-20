# Example: Simple Python Program

def calculate(x, y):
    __SNAPSHOT__("calculate:entry")

    result = x + y

    __SNAPSHOT__("calculate:before_return")
    return result

def main():
    __SNAPSHOT__("main:start")

    a = 10
    b = 20

    sum_result = calculate(a, b)

    __SNAPSHOT__("main:after_calculate")

    print(f"Result: {sum_result}")

    __SNAPSHOT__("main:end")

if __name__ == "__main__":
    main()
