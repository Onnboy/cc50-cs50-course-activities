from cs50 import get_string


def luhn_check(card_number):
    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


def get_card_type(card_number):
    length = len(card_number)
    first_two = int(card_number[:2])
    first_one = int(card_number[:1])

    if length == 15 and first_two in {34, 37}:
        return "AMEX"
    elif length == 16 and 51 <= first_two <= 55:
        return "MASTERCARD"
    elif length in {13, 16} and first_one == 4:
        return "VISA"
    else:
        return "INVALID"


card_number = get_string("Number: ")

if luhn_check(card_number):
    print(get_card_type(card_number))
else:
    print("INVALID")
