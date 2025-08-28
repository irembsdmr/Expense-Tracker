expense_df, budget_df, today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df = process_data()


    if num == 1:
        add_expense(expense_df)

    elif num == 2:
        view_expense(today_expenses_df, this_month_expenses_df, this_year_expenses_df, expense_df)

    elif num == 3:
        total_expenses(today_expenses_df, this_week_expenses_df, this_month_expenses_df, this_year_expenses_df,
                       expense_df)

    elif num == 4:
        category_expenses(expense_df)

    elif num == 5:
        visualize_expenses(expense_df)

    elif num == 6:
        manage_budget(budget_df, expense_df)

    elif num == 7:
        print("Exiting program. Goodbye! :)")
        break



