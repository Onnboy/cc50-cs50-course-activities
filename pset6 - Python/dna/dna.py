import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Read database file into a variable
    rows = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], encoding="utf-8") as f:
        read_data = f.read()

    # Find longest match of each STR in DNA sequence
    STR_list = reader.fieldnames[1:]  # Ignorar a primeira coluna ("name")
    DNA_info = {STR: longest_match(read_data, STR) for STR in STR_list}

    # Check database for matching profiles
    found_match = False
    for people in rows:
        match = all(int(people[STR]) == DNA_info[STR] for STR in STR_list)
        if match:
            print(people["name"])
            found_match = True
            break  # Não precisa verificar mais

    # Se não encontrar nenhuma correspondência, imprimir "No match"
    if not found_match:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while sequence[i + count * subsequence_length: i + (count + 1) * subsequence_length] == subsequence:
            count += 1
        longest_run = max(longest_run, count)

    return longest_run


main()
