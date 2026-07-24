numbers = list(map(int, input().split()))
target = int(input())
find = False
for index1 in range(len(numbers)):
    for index2 in range(len(numbers)):
        if numbers[index1] + numbers[index2]==target and index1 != index2:
            print(index1, index2)
            find = True
            break
    if find:
        break