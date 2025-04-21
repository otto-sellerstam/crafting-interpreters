#include <stdio.h>
#include <time.h>

int fibonacci(int n);

int main() {

    clock_t start = clock();
    int fib_result = fibonacci(40);
    clock_t end = clock();
    printf("Time to compute fib 40: %g", (double) (end - start) / CLOCKS_PER_SEC);
}

int fibonacci(int n) {
    if (n < 2) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}