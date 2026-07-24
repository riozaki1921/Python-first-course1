import csv

with open("input.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=';')
    data = list(reader)

data.sort(key=lambda x: (-int(x[1]), -int(x[2])))

with open("output.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=';')
    current_place = 1
    for i in range(len(data)):
        if i > 0 and (int(data[i][1]) != int(data[i - 1][1]) or int(data[i][2]) != int(data[i - 1][2])):
            current_place = i + 1
        writer.writerow([data[i][0], current_place])