with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    line = text.lower()
clean_line = ''.join(i for i in line if ('а' <= i <= 'я') or i == 'ё')
dict1={}
all_symbol=0
for char in clean_line:
        dict1[char]=dict1.get(char,0) +1
        all_symbol +=1
for key in dict1:
    dict1[key]=round(dict1[key] /all_symbol, 4)
sorted_letters = sorted(dict1.items(), key=lambda x: (-x[1], x[0]))
with open('output.txt', 'w', encoding='utf-8') as f:
    for letter, frequency in sorted_letters:
        f.write(f'{letter}: {frequency}\n')