import pandas as pd
import os
from datetime import timedelta
def load_expenses():
    # check if the file exists before reading
    if os.path.exists("expenses.csv"):
        # print("Previous expenses:")
        expense_df = pd.read_csv("expenses.csv")  # load existing data
    else:
        print("(No previous expenses)")
        expense_df = pd.DataFrame(columns=["Name", "Amount", "Category", "Date", "DateTime"])  # create new data frame
    # Convert date column to date format
    expense_df["Date"] = pd.to_datetime(expense_df["Date"], errors="coerce").dt.date  # dt.date ensures that only date
    # Convert date column to datetime format
    expense_df["DateTime"] = pd.to_datetime(expense_df["DateTime"], errors="coerce")
    return expense_df

def load_budgets():
    if os.path.exists("budget.csv"):
        budget_df = pd.read_csv("budget.csv")  # load existing data
    else:
        budget_df = pd.DataFrame(columns=["Year", "Month", "Amount"])  # create new data frame
    return budget_df

def filter_expenses_by_time(expense_df):
    # dataframes in special times
    today = pd.Timestamp.now()
    # today
    today_expenses_df = expense_df[expense_df['Date'] == pd.Timestamp.now().date()]
    # this week
    start_of_week = today.date() - timedelta(days=today.weekday())
    this_week_expenses_df = expense_df[(expense_df['Date'] >= start_of_week) & (expense_df['Date'] <= today.date())]
    # this month
    this_month_expenses_df = expense_df[
        (pd.to_datetime(expense_df['Date']).dt.year == today.year) & (pd.to_datetime(expense_df['Date']).dt.month == today.month)]
    # this year
    this_year_expenses_df = expense_df[(pd.to_datetime(expense_df['Date']).dt.year == today.year)]

    return today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df

def process_data():
    expense_df = load_expenses()
    budget_df = load_budgets()
    today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df = filter_expenses_by_time(expense_df)
    return expense_df, budget_df, today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df











