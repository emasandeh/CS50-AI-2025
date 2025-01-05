#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Function prototypes
bool validate_key(string key);
string encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    // Check for a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    // Validate the key
    if (!validate_key(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");

    // Encrypt the plaintext
    string ciphertext = encrypt(plaintext, key);

    // Output the ciphertext
    printf("ciphertext: %s\n", ciphertext);

    return 0;
}

// Function to validate the substitution key
bool validate_key(string key)
{
    // Check if key has 26 characters
    if (strlen(key) != 26)
    {
        return false;
    }

    // Check if all characters are alphabetic and unique
    bool seen[26] = {false}; // Array to track seen letters
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        // Normalize to uppercase for uniqueness check
        char upper = toupper(key[i]);
        int index = upper - 'A';

        if (seen[index])
        {
            return false; // Duplicate character found
        }
        seen[index] = true;
    }

    return true;
}

// Function to encrypt plaintext using the substitution cipher
string encrypt(string plaintext, string key)
{
    // Create the ciphertext string
    string ciphertext = plaintext;

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            // Preserve case and substitute character
            if (isupper(plaintext[i]))
            {
                ciphertext[i] = toupper(key[plaintext[i] - 'A']);
            }
            else
            {
                ciphertext[i] = tolower(key[plaintext[i] - 'a']);
            }
        }
        else
        {
            // Non-alphabetic characters remain unchanged
            ciphertext[i] = plaintext[i];
        }
    }

    return ciphertext;
}
