import pandas as pd
from data_processor import process_data
from expense_functions import add_expense, view_expense, total_expenses, category_expenses, visualize_expenses
from budget_functions import manage_budget
import tkinter as tk
from tkinter import messagebox
from datetime import timedelta, datetime


def main_window():
    root = tk.Tk() #create a window
    root.geometry("500x500") #size of window
    root.title("ExpenseTracker")

    label = tk.Label(root, text="Expense Tracker Menu ", font=('Arial', 18))
    label.pack(pady=10)

    tk.Button(root, text="Add Expense", width=30, command=add_expense_gui).pack(pady=5)
    tk.Button(root, text="View All Expenses", width=30, command=view_expense_gui).pack(pady=5)
    tk.Button(root, text="View Expenses by Category", width=30, command=filter_expense_gui).pack(pady=5)
    tk.Button(root, text="Total Spending", width=30, command=total_expense_gui).pack(pady=5)
    tk.Button(root, text="Visualize Spending", width=30, command=visualize_expense_gui).pack(pady=5)
    tk.Button(root, text="Monthly Budget", width=30, command=budget_gui).pack(pady=5)
    tk.Button(root, text="Exit", width=10, command=root.destroy).pack(pady=5)

    root.mainloop() #this will keep the window running
def add_expense_gui():

    add_root = tk.Toplevel()
    add_root.geometry("500x500")
    add_root.title("Add Expense")

    tk.Label(add_root, text="Expense Name:", font=('Arial', 15)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    name_entry = tk.Entry(add_root, width= 30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)  # single line text box

    tk.Label(add_root, text="Amount (€):", font=('Arial', 15)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    amount_entry = tk.Entry(add_root, width=30)
    amount_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(add_root, text="Category:", font=('Arial', 15)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    category_var = tk.StringVar(add_root) # a container for string value
    category_var.set("Food")  # default value
    category_options = ["Food", "Transport", "Personal Care", "Rent", "Entertainment", "Other"]
    category_menu = tk.OptionMenu(add_root, category_var, *category_options)
    category_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    custom_category_label = tk.Label(add_root, text="", fg="red", font=('Arial', 12))
    custom_category_entry = tk.Entry(add_root)

    error_label = tk.Label(add_root, text="", fg="red", font=('Arial', 8))
    error_label.grid(row=6, column=1, pady=10, sticky='e')

    def clear_error(event):
        error_label.config(text="")

    name_entry.bind("<KeyRelease>", clear_error)
    amount_entry.bind("<KeyRelease>", clear_error)
    custom_category_entry.bind("<KeyRelease>", clear_error)

    # Function to show/hide custom category
    def update_custom_category_entry(*args):
        if category_var.get() == "Other":
            custom_category_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
            custom_category_entry.grid(row=3, column=1, padx=10, pady=10)
        else:
            custom_category_label.pack_forget()  # Hide the custom category entry
            custom_category_entry.pack_forget()
    # Update the custom category field when category changes
    category_var.trace("w", update_custom_category_entry)


    def save_expense():
        name = name_entry.get().strip().capitalize()  # get() is to grab what is typed
        amount = amount_entry.get().strip().capitalize()
        category = category_var.get()

        # validation
        if not name:
            error_label.config(text="Warning! Expense name cannot be empty.", fg="red")
            return
        try:
            amount = float(amount)
        except ValueError:
            error_label.config(text="Warning! Amount must be a number (e.g. 10.5)", fg="red")
            return

        if category == "Other":
            category = custom_category_entry.get().strip().capitalize()
            if not category:
                error_label.config(text="Please enter a custom category", fg="red")
                return

        # load existing expenses
        expense_df, _, _, _, _, _ = process_data()  # process_data() returns 6 values and _ means ignoring the value
        error_label.config(text="Expense saved successfully!", fg="green")
        print(f"Added expenses: {name} - €{amount} [{category}]")

        #Create new expense row
        new_expense = {
            "Name": name,
            "Amount": amount,
            "Category": category,
            "Date": datetime.now().date(),
            "DateTime": datetime.now()
        }
        # pd.DataFrame converts to one-row df, pd.concat merges both
        expense_df = pd.concat([expense_df, pd.DataFrame([new_expense])], ignore_index=True)
        expense_df.to_csv("expenses.csv", index=False)

    tk.Button(add_root, text="Save", width=10, command=save_expense).grid(row=5, column=0)
    tk.Button(add_root, text="Exit", width=10, command=add_root.destroy).grid(row=5, column=1)


def filter_by_date(start_date_entry, end_date_entry, expense_df, text):
    text.delete(1.0, tk.END)
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()

    start_date = pd.to_datetime(start_date, errors='coerce').date()
    end_date = pd.to_datetime(end_date, errors='coerce').date()

    if pd.isna(start_date) or pd.isna(end_date):
        text.insert(tk.END, "Invalid date format. Please enter dates in YYYY-MM-DD format.")

    elif start_date > end_date:
        text.insert(tk.END, "Start date cant be after end date")
    else:
        special_date_df = expense_df[(expense_df['Date'] >= start_date) & (expense_df['Date'] <= end_date)]
        if not special_date_df.empty:
            df = special_date_df
            title = f"Expenses from {start_date} to {end_date}"
            output = special_date_df.to_string(index=False)
            text.insert(tk.END, title + output + "\n")


def view_expense_gui():
    expense_df, _, _, _, _, _ = process_data()
    view_root = tk.Toplevel()  # toplevel creates a child window
    view_root.title("View Expenses")
    view_root.geometry("500x500")
    label = tk.Label(view_root, text="Select the time period to view your expenses", font=('Arial', 12))
    label.pack(pady=10)

    def show_expenses(option):
        (_, _, today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df) = process_data()
        display_view = tk.Toplevel()  # toplevel creates a child window
        display_view.title("View Expenses")
        display_view.geometry("550x500")
        text = tk.Text(display_view, font=('Arial', 10))
        text.pack(fill="both", expand=True)  # to have enough space to fit window

        if option == 1:
            df = today_expenses_df
            title = "Today's Expenses"
        elif option == 2:
            df = this_week_expenses_df
            title = "This Week's Expenses"
        elif option == 3:
            df = this_month_expenses_df
            title = "This Month's Expenses"
        elif option == 4:
            df = this_year_expenses_df
            title = "This Year's Expenses"
        elif option == 5:
            df = expense_df
            title = "All Expenses"
        elif option == 6:
            filter_frame = tk.Frame(display_view)
            filter_frame.pack(side="top", fill="x", padx=10, pady=10)

            tk.Label(filter_frame, text="Start Date (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            start_date_entry = tk.Entry(filter_frame)
            start_date_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(filter_frame, text="End Date (YYYY-MM-DD)").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            end_date_entry = tk.Entry(filter_frame)
            end_date_entry.grid(row=1, column=1, padx=5, pady=5)


            text = tk.Text(display_view, font=('Arial', 10))
            text.pack(fill="both", expand=True)

            submit_button = tk.Button(filter_frame, text="Submit",
                                      command=lambda: filter_by_date(start_date_entry, end_date_entry, expense_df,
                                                                     text))
            submit_button.grid(row=2, column=0, columnspan=2, pady=10)



            return


        else:
            df = pd.DataFrame()
            title= "No data"

        output = f"{title}:\n\n"
        output += f"{'Name'.ljust(14)}{'Amount'.ljust(16)}{'Category'.ljust(18)}{'Date'.ljust(14)}{'DateTime'}\n"
        output += "-" * 90 + "\n"

        for _, row in df.iterrows():
            output += f"{row['Name'].ljust(14)}"
            output += f"€{str(row['Amount']).ljust(16)}"
            output += f"{row['Category'].ljust(18)}"
            output += f"{str(row['Date']).ljust(14)}"
            output += f"{str(row['DateTime'])}\n"

        text.insert(tk.END, output)
        text.config(state="disabled")

    tk.Button(view_root, text="Today's Expenses ", command=lambda: show_expenses(1)).pack(pady=20)
    tk.Button(view_root, text="This Week's Expenses ", command=lambda: show_expenses(2)).pack(pady=20)
    tk.Button(view_root, text="This Month's Expenses", command=lambda: show_expenses(3)).pack(pady=20)
    tk.Button(view_root, text="This Year's Expenses ", command=lambda: show_expenses(4)).pack(pady=20)
    tk.Button(view_root, text="All Expenses ", command=lambda: show_expenses(5)).pack(pady=20)
    tk.Button(view_root, text="Enter a Special Date ", command=lambda: show_expenses(6)).pack(pady=20)
    tk.Button(view_root, text="Exit ", command=lambda: view_root.destroy()).pack(pady=20)
def filter_expense_gui():
    expense_df, _, _, _, _, _ = process_data()

    def filter_expense():
        display_total = tk.Toplevel()  # toplevel creates a child window
        display_total.title("View Expenses by Category")
        display_total.geometry("550x500")
        text = tk.Text(display_total, font=('Arial', 10))
        text.pack(fill="both", expand=True)  # to have enough space to fit window

        option = category_entry.get().strip().lower()

        if option == "all":
            sorted_df = expense_df.sort_values(by="DateTime", ascending=True)
            text.delete(1.0, tk.END)
            text.insert(tk.END, sorted_df.to_string(index=False))

    filter_root = tk.Toplevel()
    filter_root.geometry("500x500")
    filter_root.title("Filter Expenses By Category")

    tk.Label(filter_root, text="\nEnter category name or 'all' to view your expenses: ", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    category_entry = tk.Entry(filter_root, width=30)
    category_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # single line text box

    submit_button = tk.Button(filter_root, text="Submit", width=10,
                              command=filter_expense)
    submit_button.grid(row=2, column=0, padx=10, pady=10, )

    tk.Button(filter_root, text="Exit", width=10, command=filter_root.destroy).grid(row=2, column=1, padx=10, pady=10)



def total_expense_gui():
    expense_df, _, _, _, _, _ = process_data()
    total_root= tk.Toplevel()
    total_root.geometry("500x500")
    total_root.title("Total Spending")

    label = tk.Label(total_root, text="Select a time period to view your total expenses", font=('Arial', 10))
    label.pack(pady=10)


    def total_expense(option):
        (_, _, today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df) = process_data()
        display_total = tk.Toplevel()  # toplevel creates a child window
        display_total.title("View Expenses")
        display_total.geometry("250x200")
        text = tk.Text(display_total, font=('Arial', 10))
        text.pack(fill="both", expand=True)  # to have enough space to fit window

        if option == 1:
            total = today_expenses_df['Amount'].sum()
            title = "Today"
        elif option == 2:
            total = this_week_expenses_df['Amount'].sum()
            title = "This Week"
        elif option == 3:
            total = this_month_expenses_df['Amount'].sum()
            title = "This Month"
        elif option == 4:
            total = this_year_expenses_df['Amount'].sum()
            title = "This Year"
        elif option == 5:
            total = expense_df['Amount'].sum()
            title = "All Total Spent"
        elif option == 6:
            total = expense_df.groupby('Category')['Amount'].sum()
            output = ""
            output += total.to_string()
            text.insert(tk.END, output)
        if option != 6:
            text.insert(tk.END, f"{title}:\n\n€{total}")
            text.config(state="disabled")


    tk.Button(total_root, text="Today ", command=lambda: total_expense(1)).pack(pady=20)
    tk.Button(total_root, text="This Week ", command=lambda: total_expense(2)).pack(pady=20)
    tk.Button(total_root, text="This Month", command=lambda: total_expense(3)).pack(pady=20)
    tk.Button(total_root, text="This Year", command=lambda: total_expense(4)).pack(pady=20)
    tk.Button(total_root, text="All Total Spent ", command=lambda: total_expense(5)).pack(pady=20)
    tk.Button(total_root, text="Total spent by Categories", command=lambda: total_expense(6)).pack(pady=20)
    tk.Button(total_root, text="Exit ", command=lambda: total_root.destroy()).pack(pady=20)






def visualize_expense_gui():
    expense_df,_,_,_,_,_ = process_data()






def budget_gui():
    print("Clicked X")
def exit_gui():
    print("Clicked X")

if __name__ == "__main__":
    main_window()
