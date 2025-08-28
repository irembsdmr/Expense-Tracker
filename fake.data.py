from faker import Faker
import pandas as pd

fake = Faker()

# Number of expenses to generate
num_expenses = 1000

# Create an empty list to store generated data
data = []

# Generate random data for expenses
for _ in range(num_expenses):
    name = fake.word()  # Random expense name (e.g., "coffee", "lunch")
    amount = round(fake.random_number(2), 2)  # Random amount (e.g., 2.50)
    category = fake.random_element(elements=("Food", "Transport", "Entertainment"))  # Random category
    date = fake.date_this_year()
    detailedDate = date = fake.date_time_this_year() # Random date within the current year
    data.append([name, amount, category, date, detailedDate])

# Create DataFrame from the generated data
df = pd.DataFrame(data, columns=["Name", "Amount", "Category", "Date", "Detailed Date"])

# Save the DataFrame to a CSV file
df.to_csv("expenses.csv", index=False)

# Print the generated expenses data
print(df)