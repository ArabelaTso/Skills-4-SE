// Example: Simple Java Program

public class ExampleJava {
    public static int calculate(int x, int y) {
        __SNAPSHOT__("calculate:entry");

        int result = x + y;

        __SNAPSHOT__("calculate:before_return");
        return result;
    }

    public static void main(String[] args) {
        __SNAPSHOT__("main:start");

        int a = 10;
        int b = 20;

        int sum = calculate(a, b);

        __SNAPSHOT__("main:after_calculate");

        System.out.println("Result: " + sum);

        __SNAPSHOT__("main:end");
    }
}
