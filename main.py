#!/usr/bin/env python
# coding: utf-8



from Person import Person
from Expense import Expense 
from Funds import Funds
import numpy as np
import re
import sqlite3
import bcrypt




# ==========================================
# 1. DATABASE SETUP
# ==========================================

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE NOT NULL,
    password_hash BLOB NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
)
""")
conn.commit()




# ==========================================
# 2. HELPER VALIDATION & AUTHENTICATION
# ==========================================




# to check for ANY number or symbol. 
def has_numbers_or_symbols(text):
    # [^a-zA-Z\s] matches anything that is NOT a letter or whitespace
    return bool(re.search(r'[^a-zA-Z\s]', text))




def asking_first_or_last_name(name_type):
    keep_asking = True 

    if name_type.lower() == "first":
        while keep_asking:
            first_name = input("Enter your first name (no numbers or symbols): ")
            if not has_numbers_or_symbols(first_name):
                keep_asking = False
        return first_name
        
    else:
        while keep_asking:
            last_name = input("Enter your last name (no numbers or symbols): ")
            if not has_numbers_or_symbols(last_name):
                keep_asking = False
    
    return last_name 




# to check if input has at least one number AND at least one symbol.     
def check_numbers_and_symbols(text):
    # (?=.*\d) checks for a digit
    # (?=.*[^\w\s]) checks for a symbol (any character that is NOT alphanumeric or whitespace)
    pattern = r'^(?=.*\d)(?=.*[^\w\s])'
        
    if re.search(pattern, text):
        return True
    return False




# to check if input has uppercase AND lowercase letters. 
def check_upper_and_lower_case(text):
    has_upper = bool(re.search(r'[A-Z]', text))
    has_lower = bool(re.search(r'[a-z]', text))
    
    return has_upper and has_lower




# to check password input.  
def check_password():
    keep_asking = True

    while keep_asking:
        password = input("Create a password (the password must be"
                  + "\n at least 8 characters long, contain at least one number, one symbol,"
                  + "\n one uppercase letter, and one lowercase letter): ")
        if not len(password) < 8 and check_numbers_and_symbols(password) and check_upper_and_lower_case(password):
            keep_asking = False 
            
    return password 




def check_if_valid_number(user_input):
    try:
        number = float(user_input)
        return number 
    except ValueError:
        return -1




def asking_amount_or_cost(num_type):
    keep_asking = True 

    if num_type.lower() == "cost":
        while keep_asking:
            cost = input("Enter an amount (such as 1, 20, 300, etc., or 12.90): ")
            if check_if_valid_number(cost) != -1:
                keep_asking = False
        return float(cost)
        
    else:
        while keep_asking:
            amount = input("Enter an amount (such as 1, 20, 300, etc., or 12.90): ")
            if check_if_valid_number(amount) != -1:
                keep_asking = False
        
    return float(amount)




def register_user(username, password, first_name, last_name):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute(
            """INSERT INTO users (username, password_hash, first_name, last_name) 
               VALUES (?, ?, ?, ?)""", 
            (username, password_hash, first_name.strip(), last_name.strip())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username taken




def login_user(username, password):
    # 1. Fetch the stored hash and user details in one O(log N) lookup
    cursor.execute(
        "SELECT password_hash, first_name, last_name FROM users WHERE username = ?", 
        (username.strip(),)
    )
    user_record = cursor.fetchone()
    
    # 2. Check if user exists
    if not user_record:
        return None  # User not found
    
    stored_hash, first_name, last_name = user_record
    
    # 3. Verify the entered password against the stored bcrypt hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return {
            "username": username,
            "first_name": first_name,
            "last_name": last_name
        }
    
    return None  # Invalid password




# ==========================================
# 4. OBJECT STORAGE & OPERATIONS
# ==========================================
expense_hashmap = {}
funds_hashmap = {}




# to organize the objects smallest -> largest expense/funds or reverse (by cost/amount) 
def smallest_to_largest(d):
    return dict(sorted(d.items(), key=lambda item: item[1]))




def largest_to_smallest(d):
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))




# to delete an object (expense/fund)
def delete_object(title):
    if title in expense_hashmap:
        del expense_hashmap[title]
    elif title in funds_hashmap:
        del funds_hashmap[title]
    else: 
        return "No such title exists :("




# to be able to search for a specific object (expense/fund) 
def search_for_object(title):
    if title in expense_hashmap: 
        return expense_hashmap.get(title) 
    elif title in funds_hasmap:
        return funds_hashmap.get(title)  
    return "Unable to find " + title + " :("




# to calculate the sum based on user selected objects (funds/expenses)
# NOTE: must prompt user to select which objects they want to calculate sum off of. 
def calculate_sum_selected_items(data_map, requested_keys):
    return sum(data_map[key] for key in requested_keys)




# to calculate the difference based on user selected objects (funds/expenses)
# NOTE: must prompt user to select which objects they want to calculate difference off of. 
def calculate_difference_selected_items(data_map, requested_keys):
    # Filter for valid keys while preserving the requested order
    valid_keys = [k for k in requested_keys if k in data_map]
    
    if not valid_keys:
        return 0.0
    
    first_value = data_map[valid_keys[0]]
    subsequent_sum = sum(data_map[k] for k in valid_keys[1:])
    
    return first_value - subsequent_sum




# ==========================================
# 5. INTERACTIVE CLI RUNNER
# ==========================================

def main():
    print("Welcome to the Money Management System!")
    action = input("Would you like to (1) Register or (2) Login? ").strip()
    
    current_user = None
    if action == "1":
        first_name = asking_first_or_last_name("first")
        last_name = asking_first_or_last_name("last")
        print(f"Hello, {first_name}!")
        username = input("Create a username: ").strip()
        password = check_password()
        
        if register_user(username, password, first_name, last_name):
            print("Registered successfully! Proceeding to app...")
            current_user = {"first_name": first_name, "last_name": last_name}
        else:
            print("Username is already taken. Exiting...")
            return
    elif action == "2":
        entered_username = input("Username: ").strip()
        entered_password = input("Password: ").strip()
        current_user = login_user(entered_username, entered_password)
        if current_user:
            print(f"Login successful! Welcome back, {current_user['first_name']} {current_user['last_name']}.")
        else:
            print("Invalid username or password.")
            return
    else:
        print("Invalid choice.")
        return

    # Application Dashboard Loop
    while True:
        print("\n--- Options Menu ---")
        print("1. Add Expense/Fund")
        print("2. Display Sorted Items")
        print("3. Search Object")
        print("4. Delete Object")
        print("5. Calculate Sum/Difference")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "1":
            while True:
                request = input("Would you like to add an expense or fund? Press E for expense or F for fund: ").strip().lower()
                if request in ("e", "f"):
                    break
                print("Invalid choice. Please enter 'E' or 'F'.")

            if request == "e":
                expense_title = input("Enter a title: ").strip()
                cost = asking_amount_or_cost("cost")
                expense_object = Expense(expense_title, cost)
                expense_hashmap[expense_title] = cost
                print(f"Added expense '{expense_title}' of ${cost:.2f}")
            elif request == "f":
                fund_title = input("Enter a title: ").strip()
                amount = asking_amount_or_cost("amount")
                fund_object = Funds(fund_title, amount)
                funds_hashmap[fund_title] = amount
                print(f"Added fund '{fund_title}' of ${amount:.2f}")

        elif choice == "2":
            target = input("Sort (E)xpenses or (F)unds? ").strip().lower()
            data = expense_hashmap if target == "e" else funds_hashmap
            order = input("(1) Smallest to Largest or (2) Largest to Smallest? ").strip()
            sorted_res = smallest_to_largest(data) if order == "1" else largest_to_smallest(data)
            print("Sorted Results:", sorted_res)

        elif choice == "3":
            t = input("Enter title to search: ").strip()
            print(search_for_object(t))

        elif choice == "4":
            t = input("Enter title to delete: ").strip()
            print(delete_object(t))

        elif choice == "5":
            target = input("Calculate on (E)xpenses or (F)unds? ").strip().lower()
            data = expense_hashmap if target == "e" else funds_hashmap
            keys_raw = input("Enter titles separated by commas: ").strip()
            keys = [k.strip() for k in keys_raw.split(",") if k.strip()]
            op = input("(1) Sum or (2) Difference? ").strip()
            if op == "1":
                print(f"Sum: ${calculate_sum_selected_items(data, keys):.2f}")
            else:
                print(f"Difference: ${calculate_difference_selected_items(data, keys):.2f}")

        elif choice == "6":
            print("Logging out. Goodbye!")
            break

if __name__ == "__main__":
    main()

