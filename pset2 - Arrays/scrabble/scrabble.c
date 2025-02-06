#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Solicitar ao usuário duas palavras
    string word1 = get_string("Primeira palavra: ");
    string word2 = get_string("Segunda palavra: ");

    // Calcular os pontos de cada palavra
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Imprimir o vencedor
    if (score1 > score2)
    {
        printf("\nPrimeira palavra WINS!\n");
    }
    else if (score1 < score2)
    {
        printf("\nSegunda palavra WINS!\n");
    }
    else
    {
        printf("\nEmpate!\n");
    }
}

int compute_score(string word)
{
    // Computa e devolve os pontos de cada palavra
    int score = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        char c = toupper(word[i]);

        if (c >= 'A' && c <= 'Z')
        {
            score += POINTS[c - 'A'];
        }
    }

    return score;
}
