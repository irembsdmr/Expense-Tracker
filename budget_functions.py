import pandas as pd
import calendar

def manage_budget(budget_df, expense_df):
    while True:
        budgetControl = int(input("\n1. Set a budget for a month\n"
                                  "2. Update the existing budget\n"
                                  "3. View month's budget and progress\n"
                                  "4. Return the Main Menu\n"))
        if budgetControl == 1:
            while True:
                try:
                    set_budget_year = int(input("Enter the year: "))
                    if 2025 <= set_budget_year <= 2100:
                        break
                    else:
                        print("Please enter a year between 2025-2100.")
                except ValueError:
                    print("That's not a valid number. Please enter a year in numeric form.")
            while True:
                try:
                    set_budget_month = int(input("Enter the month:  (1-12)"))
                    if 1 <= set_budget_month <= 12:
                        break
                    else:
                        print("Please enter a number between 1-12.")
                except ValueError:
                    print("That's not a valid number. Please enter a month in numeric form.")
            while True:
                try:
                    set_budget = int(input("What is your budget amount (€) for this date? : "))
                    break
                except ValueError:
                    print("That's not a valid number. Please enter a valid number.")
            if not budget_df[(budget_df["Year"] == set_budget_year) & (budget_df["Month"] == set_budget_month)].empty:
                print("The budget is exist for this month and year. Please try for another date")
            else:
                # Add the new budget to dataframe
                budget_df.loc[len(budget_df)] = [set_budget_year, set_budget_month, set_budget]
                # Save updated dataframe to csv
                budget_df.to_csv("budget.csv", index=False)
                # Print the latest entries
                month_name = calendar.month_name[set_budget_month]
                print(f"Added budget: {month_name}.{set_budget_year} - €{set_budget}")

        elif budgetControl == 2:
            while True:
                try:
                    set_budget_year = int(input("Enter the year: "))
                    if 2025 <= set_budget_year <= 2100:
                        break
                    else:
                        print("Please enter a year between 2025-2100.")
                except ValueError:
                    print("That's not a valid number. Please enter a year in numeric form.")
            while True:
                try:
                    set_budget_month = int(input("Enter the month:  (1-12)"))
                    if 1 <= set_budget_month <= 12:
                        break
                    else:
                        print("Please enter a number between 1-12.")
                except ValueError:
                    print("That's not a valid number. Please enter a month in numeric form.")
            while True:
                try:
                    set_budget = int(input("What is your budget amount (€) for this date? : "))
                    if not budget_df[
                        (budget_df["Year"] == set_budget_year) & (budget_df["Month"] == set_budget_month)].empty:
                        # Add the new budget to dataframe
                        budget_df.loc[
                            (budget_df["Year"] == set_budget_year) & (budget_df["Month"] == set_budget_month), "Amount"] = set_budget
                        # Save updated dataframe to csv
                        budget_df.to_csv("budget.csv", index=False)
                        # Print the latest entries
                        month_name = calendar.month_name[set_budget_month]
                        print(f"Updated budget: {month_name}.{set_budget_year} - €{set_budget}")
                        break
                    else:
                        print("There is no existing budget to update for this date ")

                except ValueError:
                    print("That's not a valid number. Please enter a valid number.")

        elif budgetControl == 3:
            while True:
                try:
                    set_budget_year = int(input("Enter the year: "))
                    if 2025 <= set_budget_year <= 2100:
                        break
                    else:
                        print("Please enter a year between 2025-2100.")
                except ValueError:
                    print("That's not a valid number. Please enter a year in numeric form.")
            while True:
                try:
                    set_budget_month = int(input("Enter the month:  (1-12)"))
                    if 1 <= set_budget_month <= 12:
                        break
                    else:
                        print("Please enter a number between 1-12.")
                except ValueError:
                    print("That's not a valid number. Please enter a month in numeric form.")
            while True:
                filtered_budget = budget_df[
                    (budget_df["Year"] == set_budget_year) & (budget_df["Month"] == set_budget_month)]
                expense_df["DateTime"] = pd.to_datetime(expense_df["DateTime"])
                filtered_month = expense_df[(expense_df["DateTime"].dt.year == set_budget_year) & (expense_df["DateTime"].dt.month == set_budget_month)]
                if not filtered_budget.empty:
                    monthly_budget = filtered_budget.iloc[-1]["Amount"]
                    monthly_spent = filtered_month["Amount"].sum()
                    monthly_remaining = round(monthly_budget - monthly_spent, 2)
                    monthly_used = monthly_spent * 100 / monthly_budget
                    month_name = calendar.month_name[set_budget_month]
                    print(f"\n{month_name} {set_budget_year} Budget Overview: \n"
                          f"Monthly Budget: {monthly_budget}\n"
                          f"Total Spent: {monthly_spent}\n"
                          f"Remaining: {monthly_remaining}\n"
                          f"%{monthly_used}")
                    if monthly_used > 90:
                        print("Warning: You are close to your budget!")
                    break
        elif budgetControl == 4:
            print("Returning to the main menu...")
            break


