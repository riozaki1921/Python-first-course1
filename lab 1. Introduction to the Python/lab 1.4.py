str1 = input().lower()
str2 = input().lower()
dict_1 = {}
dict_2 = {}
clean_line1 = [i for i in str1 if i.isalpha()]
clean_line2 = [i for i in str2 if i.isalpha()]
for key in clean_line1:
    dict_1[key] = clean_line1.count(key)
for key in clean_line2:
    dict_2[key] = clean_line2.count(key)
if dict_1==dict_2:
    print("YES")
else:
    print("NO")