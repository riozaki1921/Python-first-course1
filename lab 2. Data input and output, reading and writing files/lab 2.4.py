import csv

with open("input.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=';')
    data = list(reader)
    data.pop(0)

dict1={}
for row in data:
    dict1[row[1]]=dict1.get(row[1],0) + float(row[2])

with open("output.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=';')
    print("Категория;Стоимость")
    writer.writerow(["Категория", "Стоимость"])
    for key, cost in sorted(dict1.items()):
        writer.writerow([key, f"{cost:.2f}"])
        print(f'{key}: {cost:.2f}')