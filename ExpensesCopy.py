#group by in python
from collections import defaultdict

#import pandas
import pandas as pd

#list of expenses
expenseList = []
#previous expenses
print("Previous expenses:")
with (open("expenses.txt", "r") as file):
    for index, line in enumerate(file, start=1):
        parts=line.strip().split("-")
        if len(parts)<3 or len(parts)>3:
            continue
        name, amount, category = parts
        expenseList.append((name, amount, category))
        print(f"{index}. {name} - €{amount} [{category}]")
if not expenseList:
   print("(No previous expenses)")
#add a new expense
print("")
while True:
    name = input("What is the name of expense?")
    if name == "exit":
        break
    amount = int(input("What is the amount of the expense?"))
    category = input("Enter an expense category(Food, Transport..): ")
    expenseList.append((name, amount, category))
#write the expenses on a txt file
with open("expenses.txt", "w") as file:
    for name, amount, category in expenseList:
        file.write(f"{name}-{amount}-{category}\n")
#print expenses from list
print("\nYour expenses:")
for index, expense in enumerate(expenseList, start =1):
    print(f"{index}. {expense[0]} - €{expense[1]} [{expense[2]}]")

#calculate the total spent
total = sum(int(amount) for _, amount, _ in expenseList)
print(f"Total spent : €{total}")
#calculate the sum by category
total_category = defaultdict(int)
for name, amount, category in expenseList:
    total_category[category] += int(amount)
#print the sum of categories
print("\nCategory-wise breakdown")
for category, total_c in total_category.items():
    print(f"{category} : {total_c}")

#print expenses by filtering
category_expenses = input("\nFilter expenses by category?(Enter category name or 'all': ")
if category_expenses == 'all':
    print ("\nAll Expenses: ")
    for index, (name, amount, category) in enumerate(expenseList, start=1):
        print(f"{index}. {name} - €{amount} [{category}]")
    print(f"Total spent : €{total}")
else:
    filtered_expenses = []
    for cat in expenseList:
        if cat[2].lower() == category_expenses.lower():
            filtered_expenses.append(cat)
    if filtered_expenses:
        print(f"Expenses in category [{category_expenses}]:")
        for index, (name, amount,category) in enumerate (filtered_expenses, start=1):
            print(f"{index}. {name} - €{amount}")

        for category, total_c in total_category.items():
            if category_expenses == category:
                print(f"Total in {category} : €{total_c}")

