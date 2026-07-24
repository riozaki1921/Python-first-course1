def reducer(*fraction):
    a,b = fraction[0], fraction[1]
    for i in range(a, 1, -1):
        while not a%i and not b%i:
            a//=i
            b//=i

    my_tuple = (a,b)
    return my_tuple

a, b = map(int, input().split())
print(*reducer(a, b))