import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    # File name where data is stored
    CSV_FILE = "finance_data.csv"

    # Column structure of CSV file
    COLUMNS = ["date", "amount", "category", "description"]

    # Date format used throughout the program
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """
        Ensure CSV file exists.
        If not, create it with column headers.
        """
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            with open(cls.CSV_FILE, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
                writer.writeheader()   # Write column names

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """
        Add a new transaction entry to the CSV file.
        """
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        # Append new row to CSV
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        Fetch and display transactions between given date range.
        Also calculates summary (income, expense, savings).
        """
        df = pd.read_csv(cls.CSV_FILE)

        # Handle empty file case
        if df.empty:
            print("No data available.")
            return df

        # Convert string dates to datetime objects
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)

        # Convert user input into datetime
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Filter data between date range
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )

            # Display filtered data in readable format
            print(
                filtered_df.to_string(
                    index=False,
                    formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            # Calculate totals
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            # Print summary
            print("\nSummary:")
            print(f"Total Income: ₹{total_income:.2f}")
            print(f"Total Expense: ₹{total_expense:.2f}")
            print(f"Net Savings: ₹{(total_income - total_expense):.2f}")

        return filtered_df


def add():
    """
    Collect user input and store transaction.
    """
    CSV.initialize_csv()

    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    """
    Plot income and expense trends over time.
    """
    if df.empty:
        print("No data to plot.")
        return

    # Convert date column and set as index
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    # Resample daily and calculate totals
    income_df = df[df["category"] == "Income"]["amount"].resample("D").sum()
    expense_df = df[df["category"] == "Expense"]["amount"].resample("D").sum()

    # Plot graph
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df, label="Income")
    plt.plot(expense_df.index, expense_df, label="Expense")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    """
    Main CLI loop for user interaction.
    """
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()

        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")

            df = CSV.get_transactions(start_date, end_date)

            # Ask user if they want visualization
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Enter 1, 2 or 3.")


# Entry point of program
if __name__ == "__main__":
    main()