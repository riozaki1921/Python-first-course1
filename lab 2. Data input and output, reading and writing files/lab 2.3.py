inpt = open("input.txt")
out = open("output.txt", "w")
mask = list(map(int, inpt.readline().strip().split(".")))
print(mask)
ips = [list(map(int, ip.strip().split("."))) for ip in inpt]
print(ips)
for ip in ips:
    ans = ""
    for i in range(4):
        ans += str(mask[i]&ip[i])
        ans += "."
    out.write(f"{ans[:-1]}\n")