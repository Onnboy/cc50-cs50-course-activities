#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int start_size, end_size;

    // Solicita o tamanho inicial (deve ser pelo menos 9)
    do
    {
        start_size = get_int("Start size: ");
    }
    while (start_size < 9);

    // Solicita o tamanho final (deve ser pelo menos o tamanho inicial)
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < start_size);

    // Contador de anos
    int years = 0;
    int population = start_size;

    // Calcula os anos necessários até atingir ou superar o tamanho final
    while (population < end_size)
    {
        int born = population / 3; // Lhamas nascem
        int died = population / 4; // Lhamas morrem
        population += (born - died);
        years++;
    }

    // Imprime o número de anos necessários
    printf("Years: %i\n", years);
}
