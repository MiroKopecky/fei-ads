import math
import sys

FILE_NAME = 'cvicenie2data.txt'
# FILE_NAME = 'mydata2.txt'
DAILY_DISTANCE = 400

with open(FILE_NAME, 'r') as f:
    data = f.read()

cities = [0] + [int(i) for i in data.split()]
route_penalties = [0] + [sys.maxsize] * (len(cities) - 1)

# sucasne mesto
for i in range(1, len(cities)):
    # predchadzajuce mesta
    for j in range(i):
        route_penalties[i] = min(route_penalties[i],
                                 route_penalties[j] + math.pow(DAILY_DISTANCE - (cities[i] - cities[j]), 2))

print("Minimal penalty:", route_penalties[len(cities) - 1])
