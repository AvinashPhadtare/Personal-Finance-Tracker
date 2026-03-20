from datetime import datetime

# Standard date format used across the project
date_format = "%d-%m-%Y"

# Category mapping
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    """
    Get valid date input from user.
    If allow_default is True and user presses Enter,
    today's date is returned.
    """
    date_str = input(prompt)

    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        # Convert string to datetime
        valid_date = datetime.strptime(date_str, date_format)
        # Convert back to string in same format
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)   # retry


def get_amount():
    """
    Get valid amount input (positive number only).
    """
    try:
        amount = float(input("Enter the amount: "))

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        return amount

    except ValueError as e:
        print(e)
        return get_amount()   # retry


def get_category():
    """
    Get valid category input (I/E).
    """
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()

    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()   # retry


def get_description():
    """
    Get optional description from user.
    """
    return input("Enter a description (optional): ")