#include <stdlib.h>
#include <stdio.h>

int main() {
    const char myString[] = "123 345";

    myString[0] = 'a';

    printf("%s\n", myString);
}