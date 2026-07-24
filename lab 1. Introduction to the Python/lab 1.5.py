line = input()
virus = input().lower()
while virus in line:
    index = line.find(virus)
    line = line[:index] + line[index + len(virus):]
print(line)