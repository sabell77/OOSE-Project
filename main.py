import os
import time
from database import USERS_DB, PRODUCTS_DB,COUPONS_DB, SALES_HISTORY
from users import Cashier, Administrator
from transactions import SaleTransaction, ProductCatalog, Coupon
from payments import CashPayment, CheckPayment, CreditCardPayment

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_box(text):
    lines = text.split('\n')
    width = max(len(line) for line in lines) + 4
    print("+" + "-" * (width - 2) + "+")
    for line in lines:
        print(f"| {line.ljust(width - 4)} |")
    print("+" + "-" * (width - 2) + "+")

def print_banner(text):
    print("\n" + "="*45)
    print(f"{text:^45}")
    print("="*45)

def display_tabular_receipt(subtotal, discount, final_total):
    """Displays a structured table for the final bill."""
    print("\n" + "="*35)
    print(f"{'ITEM':<20} | {'AMOUNT':>10}")
    print("-" * 35)
    print(f"{'Original Subtotal':<20} | ${subtotal:>9.2f}")
    print(f"{'Coupon Discount':<20} | -${discount:>8.2f}")
    print("-" * 35)
    print(f"{'TOTAL DUE':<20} | ${final_total:>9.2f}")
    print("="*35)

def display_user_table(user_id, name, role):
    """Displays user details in a table during administrative edits."""
    header = f"| {'ID':<10} | {'NAME':<20} | {'ROLE':<15} |"
    divider = "+" + "-"*12 + "+" + "-"*22 + "+" + "-"*17 + "+"
    
    print("\n" + divider)
    print(header)
    print(divider)
    print(f"| {user_id:<10} | {name:<20} | {role:<15} |")
    print(divider)

def cashier_logic(cashier, catalog, users):
    """Handles the tasks assigned to the Cashier class."""
    while True:
        clear_screen()
        print_banner(f"CASHIER TERMINAL: {cashier._name}")
        print("1. Start New Sale ")
        print("2. Handle Returns ")
        print("3. Logout ")
        
        choice = input("\nSelect Action > ")

        if choice == "1":
            txn_id = f"TXN-{int(time.time())}"
            cashier.startNewSale(txn_id)
            sale = SaleTransaction(txn_id)
            
            while True:
                print(f"\n--- Active Sale: {txn_id} ---")
                barcode = input("Scan Barcode (or 'pay' to finish / 'cancel' to void): ").strip().lower()

                # 1. Handle "Pay" Command
                if barcode == 'pay':
                    # Calculate SUBTOTAL (BEFORE discount) - INDENT THIS BLOCK
                    subtotal = 0
                    for item in sale._items:
                        if not hasattr(item, '_subtotal'):
                            item._subtotal = item.calcSubtotal()
                        subtotal += item._subtotal
    
                    discount_amount = 0
                    discount_rate = 0

                    use_coupon = input("\nDo you have a coupon code? (y/n): ").lower()
                    if use_coupon == 'y':
                        code = input("Enter Coupon Code: ").upper()
                        if code in COUPONS_DB:
                            discount_rate = COUPONS_DB[code]
                            coupon_obj = Coupon(code, discount_rate, f"{discount_rate*100:.0f}% discount")
                            sale.applyCoupon(coupon_obj)
                            sale.discount_rate = discount_rate  # <-- ADD THIS LINE!
                            discount_amount = coupon_obj.get_discount_amount(subtotal)
                            print(f"[PROMO] Coupon '{code}' Applied! {discount_rate*100:.0f}% off.")
                        else:
                            print("[ERROR] Invalid or expired coupon.")

                    # Calculate FINAL total (AFTER discount)
                    final_total = subtotal - discount_amount
    
                    # Display bill
                    display_tabular_receipt(subtotal, discount_amount, final_total)

                    # Use final_total for payment
                    print_banner(f"TOTAL DUE: ${final_total:.2f}")
    
                    if final_total > 0:
                        print("1. Cash Payment\n2. Check Payment\n3. Credit Card Payment")
                        m = input("Select Method > ")

                        payment_success = False

                        if m == "1":
                            amt = float(input("Enter Amount Tendered: "))
                            if amt < final_total:  # Use final_total
                                print(f"Insufficient amount. Need ${final_total - amt:.2f} more.")
                                continue
            
                            change = amt - final_total  # Use final_total
                            CashPayment(final_total).processPayment(amt)  # Use final_total
                            sale.payment_method = "CASH"
            
                            print(f"\n✓ Payment Successful! Change: ${change:.2f}")
                            sale.printReceipt(amount_tendered=amt, change=change)
                            payment_success = True
            
                        elif m == "2":
                            bank = input("Enter Bank Name: ")
                            chk = input("Enter Check Number: ")
                            CheckPayment(final_total, bank, chk).processPayment()  # Use final_total
                            sale.payment_method = "CHECK"
                            sale.printReceipt()
                            payment_success = True
            
                        elif m == "3":
                            c_num = input("Enter Card Number: ")
                            exp = input("Enter Expiry (MM/YY): ")
                            CreditCardPayment(final_total, c_num, exp).processPayment()  # Use final_total
                            sale.payment_method = "CREDIT CARD"
                            sale.printReceipt()
                            payment_success = True
        
                        if payment_success:
                            input("\nPress Enter to return to terminal...")
                    else:
                        print("No items scanned. Sale aborted.")
                    break

                # 2. Handle "Cancel" Command
                elif barcode == 'cancel':
                    print("Transaction cancelled.")
                    break

                # 3. Handle Product Scanning
                else:
                    product = catalog.getProduct(barcode)
                    if product:
                        # Uses getDetails() method from the Product class
                        draw_box(f"ITEM FOUND\n{product.getDetails()}\nPrice: ${product._price}")
                        try:
                            qty = int(input("Quantity: "))
                            sale.addLineItem(product, qty)
                        except ValueError:
                            print("Invalid quantity. Please enter a number.")
                    else:
                        print(f"![Error] Barcode '{barcode}' not found in database.")

        elif choice == "2":
            cashier.handleReturns()
            input("\nPress Enter to continue...")
        elif choice == "3":
            cashier.logout()
            break


def admin_logic(admin):
    """Handles the tasks assigned to the Administrator class."""
    while True:
        clear_screen()
        print_banner(f"ADMIN PANEL: {admin._name}")
        print("1. Create User")
        print("2. Edit User")
        print("3. Delete User")
        print("4. Configure Security")
        print("5. Manage Coupons")
        print("6. Logout")
        
        
        choice = input("\nSelect Task > ")

        if choice == "1":
            print("\n--- Create New User ---")
            user_type = input("User Type (cashier/admin): ").lower()
            user_id = input("User ID: ")
            name = input("Full Name: ")
            password = input("Password: ")
            
            # Simple validation
            if user_id and name and password:
                if user_type in ['cashier', 'admin']:
                    # Add to database (assuming USERS_DB structure)
                    if user_type == 'cashier':
                        USERS_DB['cashiers'][user_id] = {
                            'name': name,
                            'password': password
                        }
                    else:
                        USERS_DB['admins'][user_id] = {
                            'name': name,
                            'password': password
                        }
                    print(f"User '{name}' created successfully!")
                else:
                    print("Invalid user type. Must be 'cashier' or 'admin'.")
            else:
                print("All fields are required.")
                
        elif choice == "2":
            print("\n--- Edit User ---")
            user_type = input("User Type to edit (cashiers/admins): ").lower()
            user_id = input("User ID to edit: ")
            
            if user_type in USERS_DB and user_id in USERS_DB[user_type]:
                current_data = USERS_DB[user_type][user_id]
                display_user_table(user_id, current_data['name'], user_type.upper())
                
                print("\nWhat would you like to edit?")
                print("1. Name")
                print("2. Password")
                edit_choice = input("Select: ")
                
                if edit_choice == "1":
                    new_name = input("New Name: ")
                    USERS_DB[user_type][user_id]['name'] = new_name
                    print("Name updated successfully!")
                elif edit_choice == "2":
                    new_password = input("New Password: ")
                    USERS_DB[user_type][user_id]['password'] = new_password
                    print("Password updated successfully!")
            else:
                print("User not found.")
                
        elif choice == "3":
            print("\n--- Delete User ---")
            user_type = input("User Type to delete (cashier/admin): ").lower()
            user_id = input("User ID to delete: ")
            
            if user_type in USERS_DB and user_id in USERS_DB[user_type]:
                confirm = input(f"Are you sure you want to delete user '{user_id}'? (y/n): ")
                if confirm.lower() == 'y':
                    del USERS_DB[user_type][user_id]
                    print("User deleted successfully!")
            else:
                print("User not found.")
                
        elif choice == "4":
            print("\n--- Security Configuration ---")
            print("1. Change Password Requirements")
            print("2. Set Session Timeout")
            print("3. Enable/Disable Login Attempts Lock")
            
            sec_choice = input("Select option: ")
            if sec_choice == "1":
                min_length = input("Set minimum password length (default 6): ")
                print(f"Password minimum length set to {min_length} characters.")
            elif sec_choice == "2":
                timeout = input("Set session timeout in minutes (default 30): ")
                print(f"Session timeout set to {timeout} minutes.")
            elif sec_choice == "3":
                print("Login attempt lock toggled.")
            else:
                print("Invalid option.")
                
        elif choice == "5":
            print("\n--- Manage Coupons ---")
            print("1. Create New Coupon")
            print("2. View All Coupons")
            print("3. Delete Coupon")
            
            coupon_choice = input("Select option: ")
            if coupon_choice == "1":
                code = input("Coupon Code: ").upper()
                discount = float(input("Discount Percentage (e.g., 0.1 for 10%): "))
                COUPONS_DB[code] = discount
                print(f"Coupon {code} created: {discount*100}% off")
            elif coupon_choice == "2":
                print("\nActive Coupons:")
                for code, discount in COUPONS_DB.items():
                    print(f"  {code}: {discount*100}% off")
            elif coupon_choice == "3":
                code = input("Coupon Code to delete: ").upper()
                if code in COUPONS_DB:
                    del COUPONS_DB[code]
                    print(f"Coupon {code} deleted.")
                else:
                    print("Coupon not found.")
                
        elif choice == "6":
            admin.logout()
            print("Logged out successfully.")
            break
            
        else:
            print("Invalid choice. Please select 1-7.")
            
        input("\nPress Enter to return to menu...")


def main():
    catalog = ProductCatalog()
    
    while True:
        clear_screen()
        print_banner("WELCOME TO THE POS SYSTEM!!")
        print("\nStep 1: Choose Your Role")
        print("1. Cashier")
        print("2. Administrator")
        print("3. Shutdown System")
        
        role_choice = input("\nSelect Role (1-3) > ")

        if role_choice == "3":
            print("\nShutting down system. Goodbye!")
            break

        # Step 2: Input Attributes from the 'User' Abstract Class
        print("\nStep 2: Authenticate")
        uid = input("User ID: ")
        pwd = input("Password: ")
        name = input("Display Name: ")

        db_key = "cashiers" if role_choice == "1" else "admins"
        
        # Validation Logic
        if uid in USERS_DB[db_key] and USERS_DB[db_key][uid]["password"] == pwd:
            name = USERS_DB[db_key][uid]["name"]
            
            if role_choice == "1":
                user = Cashier(uid, pwd, name) #
                user.login()
                cashier_logic(user, catalog, USERS_DB)
            else:
                user = Administrator(uid, pwd, name) #
                user.login()
                admin_logic(user)
        else:
            print("\n[!] Invalid ID or Password. Access Denied.")
            time.sleep(2)

if __name__ == "__main__":
    main()

#---------------------------------------------------------------------+
# Function                 | Implemented by                 |Matric No|
#--------------------------|--------------------------------|---------|
# def clear_screen         | Nurhidayah Fatiha Mansor       |105826   |
# draw_box                 | Nurhidayah Fatiha Mansor       |105826   |
# print_banner             | Nurhidayah Fatiha Mansor       |105826   |
# display_tabular_receipt  | Muhamad Ilfan Bin Selamat      |105125   |
# display_user_table       | Muhamad Ilfan Bin Selamat      |105125   |
# cashier_logic            | Isabella Roselinni Anak Luis   |104426   |
# admin_logic              | Joyce Lau Kai Xin              |104596   |
# main                     | Mohammad Faqrullah Bin Raba'ee |105058   |
#---------------------------------------------------------------------+