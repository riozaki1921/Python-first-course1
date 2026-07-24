from datetime import time

def nearest_time(t, *n):
    nearest = None
    time_01 = int(t[:2])*3600 + int(t[3:5])*60 + int(t[6:])
    difference=float('inf')

    for i in n:
        h=int(i[:2])
        m=int(i[3:5])
        s=int(i[6:])
        time_for_comparison = h*3600 + m*60 + s

        diff1=abs(time_for_comparison-time_01)
        diff2=24*3600-diff1
        diff=min(diff1,diff2)

        if diff < difference:
            nearest=time(hour=h, minute=m, second=s)
            difference = diff

    return nearest

time_0=input()
k = int(input())
data_time=[input() for _ in range(k)]
print(nearest_time(time_0, *data_time))