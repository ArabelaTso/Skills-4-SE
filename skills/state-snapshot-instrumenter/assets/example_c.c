// Example: Simple C Program

#include <stdio.h>

int calculate(int x, int y) {
    __SNAPSHOT__("calculate:entry");

    int result = x + y;

    __SNAPSHOT__("calculate:before_return");
    return result;
}

int main() {
    __SNAPSHOT__("main:start");

    int a = 10;
    int b = 20;

    int sum = calculate(a, b);

    __SNAPSHOT__("main:after_calculate");

    printf("Result: %d\n", sum);

    __SNAPSHOT__("main:end");

    return 0;
}
