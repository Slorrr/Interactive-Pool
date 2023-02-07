def check_divisibility(n):
    return n % 17 == 0

def match_mask(n):
    return str(n).startswith("123456") and len(str(n)) == 6

results = []
for i in range(100000):
    if match_mask(i) and check_divisibility(i):
        results.append((i, i//17))

print(results)
