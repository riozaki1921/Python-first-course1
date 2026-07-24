n = int(input())
prices = {}
for i in range(n):
    row, seat, price = map(int, input().split())
    key = (row, seat)
    if key not in prices:
        prices[key] = set()
    prices[key].add(price)
for key, price_set in prices.items():
    print(f"{key[0]} {key[1]} {len(price_set)}")