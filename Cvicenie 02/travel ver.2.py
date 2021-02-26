import math
import sys

FILE_NAME = 'cvicenie2data.txt'
# FILE_NAME = 'mydata2.txt'
DAILY_DISTANCE = 400

with open(FILE_NAME, 'r') as f:
    data = f.read()

cities = [0] + [int(i) for i in data.split()]
route_penalties = [0] + [sys.maxsize] * (len(cities) - 1)
city_stops = {}

# sucasne mesto
for i in range(1, len(cities)):
    # predchadzajuce mesta
    for j in range(i):
        if route_penalties[j] + math.pow(DAILY_DISTANCE - (cities[i] - cities[j]), 2) < route_penalties[i]:
            route_penalties[i] = route_penalties[j] + math.pow(DAILY_DISTANCE - (cities[i] - cities[j]), 2)
            city_stops[i] = j

print("Minimal penalty:", route_penalties[len(cities) - 1])


def print_stops(city_stops, index):
    if index > 0:
        print_stops(city_stops, city_stops[index])
        print(index, end=" ")


print("Stops:", end=" ")
print_stops(city_stops, len(cities) - 1)
