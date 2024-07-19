from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I":"Income", "E":"Expense"}
MIN_DATE = datetime(1900, 1, 1)  # reasonable lower limit for dates
MAX_DATE = datetime(2100, 12, 31)  # reasonable upper limit for dates

def get_date(prompt, allow_default = False):
    date_str = input(prompt)

    #default allowed and no input -> current datetime
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str,date_format)
        # Validate date range
        if not (MIN_DATE <= valid_date <= MAX_DATE and MIN_DATE <= valid_date <= MAX_DATE):
            print(f"Date range should be between {MIN_DATE.strftime(date_format)} and {MAX_DATE.strftime(date_format)}")
            return get_date(prompt, allow_default)
        return valid_date.strftime(date_format)    
    except ValueError:
        print("Invalid date format")
        return get_date(prompt, allow_default)
    

def get_amount():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a positive non-negative value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()

    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid Category.")
    return get_category()    

def get_description():
    return input("Enter a description (optional): ")