import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_amount,get_category,get_description
import matplotlib.pyplot as plt

def donothing():
   x = 0


#Handle CSV file
class CSV:
   CSV_FILE = "finance_data.csv"
   COLUMNS = ["date", "amount", "category", "description"]
   FORMAT = "%d-%m-%Y"

   @classmethod
   def initialize_csv(cls):
      try:
         pd.read_csv(cls.CSV_FILE)
      except FileNotFoundError:
         #specify file format using dataframe 
         df = pd.DataFrame(columns= cls.COLUMNS)
         df.to_csv(cls.CSV_FILE, index=False)


   @classmethod
   def add_entry(cls, date, amount, category, desc):
      new_entry = {
         "date": date,
         "amount": amount,
         "category": category,
         "description": desc
      }

      #open file in append mode for writing  
      with open(cls.CSV_FILE, "a", newline="") as csvfile:
         #write dictionary to CSV file
         writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
         writer.writerow(new_entry)

      print("Entry added succesfully") 

   @classmethod
   def get_transactions(cls, start_date, end_date):
      df = pd.read_csv(cls.CSV_FILE)

      #convert date string from data frame (CSV) to datetime object
      df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, errors='coerce')
      df.dropna(subset=["date"], inplace=True)  # Drop rows with invalid dates

      #convert start/end time to datetime obj
      start_date = datetime.strptime(start_date, CSV.FORMAT)
      end_date = datetime.strptime(end_date, CSV.FORMAT)
      
      #create mask to determine which rows are in the target range
      mask = (df["date"] >= start_date) & (df["date"] <= end_date)
      filtered_df = df.loc[mask]

      if filtered_df.empty:
         print("No transactions found in given date range")
      else:
         print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
         print( #format date column
            filtered_df.to_string(
               index=False, formatters={"date":lambda x: x.strftime(CSV.FORMAT)}
            )      
         )

         #get all rows where category == income/expense, get their amount and sum of all
         total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
         total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

         print("\nSummary:")
         print(f"Total Income: ${total_income:.2f}\nTotal Expenses: ${total_expense:.2f}\nNet Savings: ${(total_income - total_expense):.2f}")
      
      filtered_df = filtered_df.sort_values(by=["date"], ascending=True)
      return filtered_df


      
def add():
   CSV.initialize_csv()
   date = get_date("Enter the date of the transaction (dd-mm-yyyy): ", allow_default=True)
   amount = get_amount()
   category = get_category()
   description = get_description()
   CSV.add_entry(date,amount,category,description)


def plot_transactions(df):
   df.set_index("date",inplace=True)
   
   #create two separate data frames for income/expense with daily frequency
   income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index,fill_value=0)
   expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index,fill_value=0)

   plt.figure(figsize=(10,5))
   plt.plot(income_df.index, income_df["amount"], label = "Income", color = "b" )
   plt.plot(expense_df.index, expense_df["amount"], label="Expense", color = "r")
   plt.xlabel("Date")
   plt.ylabel("Amount")
   plt.title("Income and Expenses over time")
   plt.legend()
   plt.grid(True)
   plt.show()


def main():
   while True:
      print("\n1. Add a new transaction")
      print("2. View transactions and summary within a date range")
      print("3. Exit")
      choice = input("Enter your choice (1-3): ")
           
      if choice == "1":
         add()
      elif choice == "2":
         start_date = get_date("Enter the start date: ")
         end_date = get_date("Enter the end date: ")

         #pass dates to file
         df = CSV.get_transactions(start_date,end_date)
         if not df.empty:
            plot_transactions(df)
      elif choice == "3":
         print("Exiting...")
         break
      else:
         print("Invalid input, enter 1,2,3:")


if __name__ == "__main__":
#if we run this file directly then main will run
#otherwise if it is imported eg it won't run
   main()         