
ints = []
for n in range(210):
    if n % 10 == 0 and n != 0:
        # print(str(n) + "\n")
        print(" ".join(ints))
        ints = []
    else:
        ints.append(str(n - 10))