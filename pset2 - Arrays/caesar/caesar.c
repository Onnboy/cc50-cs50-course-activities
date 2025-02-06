#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Function to encrypt the plaintext using Caesar cipher
void caesar_cipher(string plaintext, int key);

int main(int argc, string argv[])
{
    // Check if exactly one command-line argument is provided
    if (argc != 2)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }

    // Validate if the argument is a number
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Convert the argument to an integer key
    int key = atoi(argv[1]);

    // Get plaintext input from the user
    string plaintext = get_string("plaintext: ");

    // Encrypt the plaintext
    printf("ciphertext: ");
    caesar_cipher(plaintext, key);

    // Output the ciphertext
    // printf("ciphertext: %s\n", ciphertext);

    return 0;
}

void caesar_cipher(string plaintext, int key)
{
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            char base = isupper(plaintext[i]) ? 'A' : 'a';
            plaintext[i] = (plaintext[i] - base + key) % 26 + base;
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}
