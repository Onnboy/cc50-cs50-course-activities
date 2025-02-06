#include <cs50.h>
#include <stdio.h>

bool luhn_algorithm(long number);
int get_first_digits(long number);
int count_digits(long number);

int main(void)
{
    long number = get_long("Número: "); // Obtém o número do usuário

    // Verifica se o número é válido pelo Algoritmo de Luhn
    if (!luhn_algorithm(number))
    {
        printf("INVALID\n");
        return 0;
    }

    int length = count_digits(number);
    int first_digits = get_first_digits(number);

    // Verifica a bandeira do cartão
    if ((length == 15) && (first_digits == 34 || first_digits == 37))
    {
        printf("AMEX\n");
    }
    else if ((length == 16) && (first_digits >= 51 && first_digits <= 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && (first_digits / 10 == 4))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

// Implementação do Algoritmo de Luhn
bool luhn_algorithm(long number)
{
    int sum = 0;
    int position = 0;

    while (number > 0)
    {
        int digit = number % 10;

        // Multiplica por 2 os dígitos em posição par (da direita para a esquerda)
        if (position % 2 == 1)
        {
            int doubled = digit * 2;
            sum += (doubled / 10) + (doubled % 10);
        }
        else
        {
            sum += digit;
        }

        number /= 10;
        position++;
    }

    return (sum % 10 == 0);
}

// Conta o número de dígitos do cartão
int count_digits(long number)
{
    int count = 0;
    while (number > 0)
    {
        number /= 10;
        count++;
    }
    return count;
}

// Obtém os dois primeiros dígitos do cartão
int get_first_digits(long number)
{
    while (number >= 100)
    {
        number /= 10;
    }
    return number;
}
