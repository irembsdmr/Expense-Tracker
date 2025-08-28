import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def add_expense(expense_df):
    while True:
        name = input(
            "What is the name of expense?   (If none, type 'exit' to return to the menu)").strip().lower()  # removes leading-trailing space
        if name == "":
            print("Expense name cannot be empty. Please enter a valid name.")
            continue
        if name == "exit":
            break
        # User input loop for amount
        while True:
            try:
                amount = float(input("What is the amount of the expense?"))
                break
            except ValueError:
                print("That's not a valid number. Please enter a valid number.")
        # User input loop for category
        while True:
            category = input(
                "Enter an expense category(Food, Transport, Entertainment, Other): ").strip().capitalize()
            if category in ["Food", "Transport", "Entertainment", "Other"]:
                if category == "Other":
                    category = input("Enter your custom category: ").strip().capitalize()
                break
            else:
                print("Invalid category. Please choose from: Food, Transport, Entertainment")
        # Add the new expense to dataframe
        expense_df.loc[len(expense_df)] = [name, amount, category, pd.Timestamp.now().date(), pd.Timestamp.now()]
        # Save updated dataframe to csv
        expense_df.to_csv("expenses.csv", index=False)
        # Print the latest entries
        print(f"Added expenses: {name} - €{amount} [{category}]")


def view_expense(today_expenses_df, this_month_expenses_df, this_year_expenses_df, expense_df):
    while True:
        view_expenses = int(input("How would you like to view your expenses?: \n"
                                  "1. Today\n"
                                  "2. This month\n"
                                  "3. This Year\n"
                                  "4. All Expenses\n"
                                  "5. Enter a Special Date\n"
                                  "6. Return the Main Menu\n"))
        if view_expenses == 1:
            if not today_expenses_df.empty:
                print("Expenses for today:\n", today_expenses_df.to_string(index=False))
            else:
                print("No expenses recorded for today.")
        elif view_expenses == 2:

            if not this_month_expenses_df.empty:
                print("Expenses for this month:\n", this_month_expenses_df.to_string(index=False))
            else:
                print("No expenses recorded for this month.")
        elif view_expenses == 3:
            if not this_year_expenses_df.empty:
                print("Expenses for this year:\n", this_year_expenses_df.to_string(index=False))
            else:
                print("No expenses recorded for this year.")
        elif view_expenses == 4:
            print("All expenses: \n", expense_df.to_string(index=False))
        elif view_expenses == 5:
            start_date = input("Enter the start date (YYYY-MM-DD):").strip()
            end_date = input("Enter the end date (YYYY-MM-DD):").strip()
            # convert the datetime
            start_date = pd.to_datetime(start_date, errors='coerce').date()
            end_date = pd.to_datetime(end_date, errors='coerce').date()

            if pd.isna(start_date) or pd.isna(end_date):
                print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
            elif start_date > end_date:
                print("Start date cant be after end date")
            else:
                special_date_df = expense_df[(expense_df['Date'] >= start_date) & (expense_df['Date'] <= end_date)]
                if not special_date_df.empty:
                    print("Expenses for this date:\n", special_date_df.to_string(index=False))
                else:
                    print("No expenses recorded for this date.")
        elif view_expenses == 6:
            print("Returning to the main menu...")
            break


def total_expenses(today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df, expense_df):
    while True:
        total_expenses = int(input("How would you like to view your total expenses?: \n"
                                   "1. Today\n"
                                   "2. This Week\n"
                                   "3. This Month\n"
                                   "4. This Year\n"
                                   "5. All total spent \n"
                                   "6. Enter a Special Date\n"
                                   "7. Total spent by Categories\n"
                                   "8. Return to Main Menu\n"))

        if total_expenses == 1:
            today_total = today_expenses_df['Amount'].sum()
            print(f"\nToday's total spent : €{today_total}")

        elif total_expenses == 2:

            week_total = this_week_expenses_df['Amount'].sum()
            print(f"\nThis Week's total spent : €{week_total}")

        elif total_expenses == 3:
            month_total = this_month_expenses_df['Amount'].sum()
            print(f"\nThis Month's total spent : €{month_total}")

        elif total_expenses == 4:
            year_total = this_year_expenses_df['Amount'].sum()
            print(f"\nThis Year's total spent : €{year_total}")

        elif total_expenses == 5:
            all_total = expense_df['Amount'].sum()
            print(f"\nTotal spent : €{all_total}")

        elif total_expenses == 6:
            start_date = input("Enter the start date (YYYY-MM-DD):").strip()
            end_date = input("Enter the end date (YYYY-MM-DD):").strip()
            # convert the datetime
            start_date = pd.to_datetime(start_date, errors='coerce').date()
            end_date = pd.to_datetime(end_date, errors='coerce').date()

            if pd.isna(start_date) or pd.isna(end_date):
                print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
            elif start_date > end_date:
                print("Start date cant be after end date")
            else:
                special_date_df = expense_df[(expense_df['Date'] >= start_date) & (expense_df['Date'] <= end_date)]
                if not special_date_df.empty:
                    special_total = special_date_df['Amount'].sum()
                    print(f"\nTotal spent in these dates: €{special_total}")
                else:
                    print("No expenses recorded for this date.")
        elif total_expenses == 7:
            total_c = expense_df.groupby('Category')['Amount'].sum()
            print(total_c)
        elif total_expenses == 8:
            print("Returning to the main menu...")
            break


def category_expenses(expense_df):

    filter_expenses = input("\nFilter expenses by category?(Enter category name or 'all': ").strip().lower()
    if filter_expenses == 'all':
        sorted_df = expense_df.sort_values(by="DateTime", ascending=True)
        print(sorted_df.to_string(index=False))
    elif filter_expenses in expense_df['Category'].str.lower().values:
        filtered_df = expense_df[expense_df['Category'].str.lower() == filter_expenses.lower()]
        sorted_filtered_df = filtered_df.sort_values(by="DateTime", ascending=True)
        print(sorted_filtered_df.to_string(index=False))
    else:
        print("No expenses found for the category")


def visualize_expenses(expense_df):
    while True:
        visualize_expenses = int(input("What would you like to visualize?: \n"
                                       "1. Daily Spending Over Time (Line Chart)\n"
                                       "2. Spending by Categories (Pie Chart)\n"
                                       "3. Weekly Spending (Line Chart)\n"
                                       "4. Monthly Spending (Bar Chart)\n"
                                       "5. Compare Categories Over Time (Multiple Bar)\n"
                                       "6. Return to Main Menu\n"))
        expense_df["Date"] = pd.to_datetime(expense_df["Date"], errors="coerce")

        if visualize_expenses == 1:
            # Calculate the sum of amount each day
            daily_total = expense_df.groupby('Date')['Amount'].sum()
            # Create a linechart
            plt.figure(figsize=(10, 5))  # adjust size
            sns.lineplot(x=daily_total.index, y=daily_total.values)
            plt.xlabel("Date")
            plt.ylabel("Total Expenses (€)")
            plt.title("Daily Expenses Over Time")
            plt.xticks(rotation=45)  # dates rotated for better readability
            plt.show()

        elif visualize_expenses == 2:
            # Calculate the sum of categories
            total_category = expense_df.groupby('Category')['Amount'].sum()
            # Turn it a format that matplotlib can use
            labels = list(total_category.keys())
            values = list(total_category.values)
            # Create a pie chart
            sns.set_style("darkgrid")
            plt.figure(figsize=(6, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.show()

        elif visualize_expenses == 3:
            expense_df = expense_df.set_index('Date')  # resample function needs index in datetime
            weekly_total = expense_df.resample('W-Mon').sum(numeric_only=True)
            # Create a linechart
            plt.figure(figsize=(10, 5))
            sns.lineplot(x=weekly_total.index, y=weekly_total['Amount'])
            plt.xlabel("Week")
            plt.ylabel("Total Expenses (€)")
            plt.title("Weekly Spending Over Time")
            plt.xticks(rotation=45)  # dates rotated for better readability
            plt.show()

        elif visualize_expenses == 4:
            expense_df = expense_df.set_index("Date")  # resample function works only for dateTimeIndex
            monthly_total = expense_df.resample('ME').sum(numeric_only=True)

            # Create a linechart
            plt.figure(figsize=(10, 5))
            sns.barplot(x=monthly_total.index, y=monthly_total['Amount'])
            plt.xlabel("Month")
            plt.ylabel("Total Expenses (€)")
            plt.title("Monthly Spending Over Time")
            plt.xticks(rotation=45)  # dates rotated for better readability
            plt.show()

        elif visualize_expenses == 5:
            # Group by month and Category
            expense_df = expense_df.set_index("Date")
            monthly_category = expense_df.groupby([expense_df.index.to_period('M'), 'Category'])[
                'Amount'].sum().unstack()  # unstack function converts multi indexes into columns
            # Create a multiple bar chart
            monthly_category.plot(kind='bar', figsize=(10, 5), width=0.8)
            plt.xlabel("Month")
            plt.ylabel("Total Expenses (€)")
            plt.title("Monthly Spending by Category")
            plt.xticks(rotation=45)  # dates rotated for better readability
            plt.tight_layout()
            plt.show()
        elif visualize_expenses == 6:
            print("Returning to the main menu...")
            break
