from csv import DictReader
from sys import argv
import math


# -- CONSTANTS --
# Sales tax and other taxes
SALES_TAX = 0.0625
# Name of file with list of what people are willing to pay for
WILLINGNESS_TO_PAY_FILE = "willingness_to_pay.csv"

# What do we need to do
# -- DATA STORAGE --
# First, need a map of objects to people
# Can also read this map from a csv for now
# More efficient --> dict , key : item --> value : array of people
willingness_to_pay = {}

try:
    f = open(WILLINGNESS_TO_PAY_FILE, 'r', newline='')
except FileNotFoundError:
    print("Invalid willingess to pay file name")
    exit()
with f:
    reader = DictReader(f)
    for row in reader:
        willingness_to_pay[row["Item"].lower().strip()] = [
            key for key in row if key != "Item" and row[key] == "TRUE"]


# -- Receipt Reading / input --
# Temp - Person uploads a csv with items and prices
# Script reads this csv and converts it into a data structure, a dict with item and price,
# Duplicate items should be merged, and their prices should also be merged (added together)

# receipt = {"fish": 10, "onions": 5.00}
if len(argv) != 2:
    print(f"Usage : python3 {argv[0]} <receipt_file_name>")
    exit()
receipt_file = argv[1]

receipt = {}

try:
    f = open(receipt_file, 'r', newline='')
except FileNotFoundError:
    print("Invalid receipt file name")
    exit()
with f:
    reader = DictReader(f)
    for row in reader:
        # Merge duplicate items
        item = row["Item"].lower().strip()
        start_index = 0
        # TODO: make this a better system of checking
        if row["Item"][start_index] == "$":
            start_index += 1

        if item in receipt:
            receipt[item] += float(row["Price"][start_index:])
        else:
            receipt[item] = float(row["Price"][start_index:])

# for key in receipt:
#     print(f"{key} : {receipt[key]}")

# -- Distribution --
# Read from data structure created by receipt
# For each entry in the receipt, find the corresponding entry in the master dict
# Multiply the price to account for tax, and then divide by the length of the corresponding array of people
# Have a list of people with how much they owe, this is what gets outputted at the end
# If a person whose name is not already in the list is encountered, create a new person and add them to the list
# Then add that person to the list with an initial value of 0 and then add what they owe (or use what they owe for the item as an initial value)
# For each person, in the corresponding master list, add what they owe
people = {}

for item in receipt:
    if item not in willingness_to_pay:
        print(f"{item} not registered, cannot be properly distributed")
        exit()

    # Calculate price per person

    # price_with_tax = receipt[item] * (1 + SALES_TAX)


    price_per_person = receipt[item] / float(len(willingness_to_pay[item]))

    for person in willingness_to_pay[item]:
        # Create a new person in the people dict if they are not mapped yet
        if person not in people:
            people[person] = 0

        people[person] += price_per_person

# -- Output --
# For now, can just be a list of people with how much they owe based on the receipt
# Start here

# people = {"Isaac": 0, "Alec": 0, "Nathaniel": 0, "Ben": 0, "Artem": 0}

for person in people:
    print(f"{person} owes {people[person]: 0.2f}")

# -- Testing --
people_total = 0
for person in people:
    people_total += people[person]

# people_total *= (1 + SALES_TAX)

receipt_total = 0
for item in receipt:
    receipt_total += receipt[item]

# receipt_total *= (1 + SALES_TAX)

# print(people_total)
# print(receipt_total)
print("Total Added Correctly" if math.isclose(people_total, receipt_total, abs_tol= 0.005) else "Something went wrong, results invalid")
