N = int(input())
simple = [2]
for i in range(3, N + 1):
    is_prime = True
    for j in range(2, i):
        if i % j == 0:
            is_prime = False
            break
    if is_prime:
        simple.append(i)

print(*(simple))