"""System module."""
import json
import requests

response = requests.get('https://api.covid19api.com/live/country/united-states/status/confirmed')
ash = json.loads(response.content)

cc = 0
count = 0
state = []
ccps = []

#   Loops through the data and appends all provinces to state array
for json_objects in ash:
    if json_objects["Province"] not in state:
        state.append(json_objects["Province"])

#   Loops through the data in provinces to get confirmed cases per state
for states in state:
    for json_objects in ash:
        if json_objects["Province"] == states:
            count += 1
            cc += json_objects["Confirmed"]

    ccps.append(cc // count)
    count = 0

results = []
length = len(state)
length2 = length
count = 0

print("\n---Exercise #2---\n")

#   Loop through arrays to build data table
print("Data Table:")
print("#  State:         Confirmed:")
for i in range(length):
    results.append(str(state[i]) + ": " + str(ccps[i]))
    count += 1
    print(str(count) + ": " + str(state[i]) + ": " + str(ccps[i]))

print("\n---Exercise #1---\n")

#   Prints out average cases
print("Average: ")
avg = 0
for i in range(length):
    avg += ccps[i]

print(avg // length)

#   Prints least confirmed cases
print("\nLeast Confirmed: ")
count = 0
for i in range(5):
    count += 1
    print(str(count) + ". " + results[i])

#   Prints most confirmed cases
print("\nMost Confirmed: ")
count = 0
for i in range(5):
    length2 -= 1
    count += 1
    print(str(count) + ". " + results[length2])
