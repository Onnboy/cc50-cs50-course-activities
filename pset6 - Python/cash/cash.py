from cs50 import get_float

while True:
    change = get_float("Change owed: ")
    if change >= 0:
        break

cents = round(change * 100)

coins = [25, 10, 5, 1]

count = 0
for coin in coins:
    count += cents // coin
    cents %= coin

print(count)
