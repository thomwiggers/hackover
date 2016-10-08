// Thom Wiggers <thom@thomwiggers.nl>
// Available under the New BSD licence
//
// Solution to Hackover 2016's 'guessr' challenge
// C version of the Python solution, because this is much, much faster.
//
#include <stdio.h>

const unsigned long m = 2147483648L;
//const unsigned long m = 65536;
const unsigned int a = 117649;
const unsigned int b = 5;


unsigned long step(unsigned long val, const unsigned int steps) {
    for (int i = 0; i < steps; ++i) {
        val = (a * val + b) % m;
    }
    return val;
}

unsigned int get_val(const unsigned long val) {
    return (val % 100) + 1;
}


int main(int argc, char** argv) {
    const unsigned int N_VALS = 8;
    const unsigned int vals[] = {6, 31, 28, 37, 42, 15, 56, 81};

    int guesses = 0;
    unsigned long last_guess = 0;

    for(unsigned long i = 0; i < m; ++i) {
        if (i % 100000000 == 0) {
            printf("We've checked %lu items\n", i);
        }
        for(int j = 0; j < N_VALS; ++j) {
            if (get_val(step(i, j)) != vals[j]) {
                break;
            }
            if (j == (N_VALS-1)) {
                printf("%lu may be a possibility!\n", i);
                last_guess = i;
                guesses++;
            }
        }
    }

    printf("Found %d possibilities\n", guesses);
    printf("Last guess %lu that seems viable\nIts sequence: \n", last_guess);
    for (int i = 0; i < 15+N_VALS; i++) {
        printf("%u\n", get_val(step(last_guess, i)));
    }

    return 0;
}
