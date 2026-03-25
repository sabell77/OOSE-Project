from abc import ABC, abstractmethod
from database import USERS_DB, COUPONS_DB, SALES_HISTORY, PRODUCTS_DB

class User(ABC):
    def __init__(self, userID, password, name):
        self._userID = userID        # Private attribute from diagram
        self._password = password    # Private attribute from diagram
        self._name = name            # Private attribute from diagram

    @abstractmethod
    def login(self): pass

    @abstractmethod
    def logout(self): pass

     # Class User(ABC)
     # Implemented by Muhamad Ilfan Bin Selamat
     # (105125)
    
class Administrator(User):
    def login(self): 
        print(f"\n[AUTH] Administrator {self._name} (ID: {self._userID}) logged in.")

    def logout(self): 
        print(f"[AUTH] Admin session for {self._name} closed.")

    def createUser(self):
        print("\n--- Create New User ---")
        print("Choose Your Role:\n1. Cashier\n2. Admin")
        role = input("\nSelect Role > ")
        role_key = "cashiers" if role == "1" else "admins"
        
        new_id = input("Enter New User ID: ")
        new_name = input("Enter New User Name: ")
        new_pass = input("Enter Password: ")
        
        # Save directly to database
        USERS_DB[role_key][new_id] = {"password": new_pass, "name": new_name}
        print(f"[SUCCESS] {role_key[:-1].capitalize()} '{new_name}' created.")

    def editUser(self):
        target_id = input("Enter User ID to edit: ").strip()
        
        # Check if user exists in either branch
        found_in = None
        if target_id in USERS_DB["cashiers"]: found_in = "cashiers"
        elif target_id in USERS_DB["admins"]: found_in = "admins"

        if found_in:
            print(f"\nEditing User: {target_id} ({found_in})")
            print("1. Change Name\n2. Change Password")
            sub_choice = input("What to update? > ")
            
            if sub_choice == "1":
                new_name = input("Enter new name: ")
                USERS_DB[found_in][target_id]["name"] = new_name
                print("[SUCCESS] Name updated.")
            elif sub_choice == "2":
                new_pass = input("Enter new password: ")
                USERS_DB[found_in][target_id]["password"] = new_pass
                print("[SUCCESS] Password updated.")
        else:
            print(f"[!] User ID {target_id} not found.")

    def deleteUser(self):
        target = input("Enter User ID to delete: ")
        confirm = input(f"Are you sure you want to delete {target}? (y/n): ")
        if confirm.lower() == 'y':
            print(f"[SUCCESS] User {target} removed from system.")

    def configureSecurity(self):
        level = input("Select Encryption Level (Low/Medium/High): ")
        print(f"[SECURITY] System security level updated to: {level}.")

    def manageCoupons(self):
        print("\n--- Manage System Coupons ---")
        code = input("Enter new Coupon Code: ").upper()
        try:
            discount = float(input("Enter Discount Percentage (e.g., 10 for 10%): "))
            COUPONS_DB[code] = discount / 100
            print(f"[SUCCESS] Coupon '{code}' added with {discount}% discount.")
        except ValueError:
            print("[ERROR] Invalid discount value.")

     # Class Administrator(User)
     # Implemented by Muhamad Ilfan Bin Selamat
     # (105125)

class Cashier(User):
    def login(self): print(f"\n[AUTH] Cashier {self._name} logged in.")
    def logout(self): print(f"[AUTH] Cashier {self._name} logged out.")
    def startNewSale(self, tid): print(f"\nStarting Sale: {tid}")
    def scanItem(self, b): pass

    def handleReturns(self):
        from transactions import SaleTransaction
    
        print("\n" + "="*40)
        print(f"{'RETURN PROCESSING MENU':^40}")
        print("="*40)

        txn_id = input("Enter Transaction ID to return: ").strip()
    
        if txn_id in SALES_HISTORY:
            record = SALES_HISTORY[txn_id]
        
            print(f"\n[RECORD FOUND] Date: 2025-12-25\n")
            print("-" * 45)
            print(f"{'ITEM':<20} | {'QTY':<5} | {'PRICE':>12}")
            print("-" * 45)
        
        # This loop ONLY prints the items
            for item in record["items"]:
                print(f"{item['name']:<20} | {item['qty']:<5} | ${item['price']:>11.2f}")
        
        # FIXED: Total is OUTSIDE the loop so it only prints once
            print("-" * 45)
            print(f"{'ORIGINAL TOTAL':<28} | ${record['total']:>11.2f}")
            print("-" * 45)
        
        # Step 2: Define target_name and Search
            target_name = input("\nWhich item is being returned? ").strip().lower()
            found_item = next((i for i in record["items"] if i["name"].lower() == target_name), None)

            if found_item:
                try:
                    max_qty = found_item['qty']
                    qty = int(input(f"Quantity to return (Max {max_qty}): "))
                
                    if 0 < qty <= max_qty:
                        refund_subtotal = qty * found_item['price']
                    
                        print("\n" + "-"*35)
                        print(f"{found_item['name']:<20} | ${refund_subtotal:>9.2f}")
                        print("-" * 35)
                    
                        confirm = input("Confirm Refund? (y/n): ").lower()
                        if confirm == 'y':
                        # Create a refund transaction object
                            refund_txn_id = f"REF-{txn_id}"
                            refund_sale = SaleTransaction(refund_txn_id)
                        
                        # Create a LineItem for the refund
                            from models import Product, LineItem
                        
                        # Create a temporary product object for the refund
                            temp_product = Product(
                                barcode="REFUND",
                                name=found_item['name'],
                                price=found_item['price'],
                                stockLevel=0
                            )
                        
                            # Create line item for refund
                            refund_line_item = LineItem(temp_product, qty)
                        
                            # Add to refund sale
                            refund_sale._items = [refund_line_item]
                        
                            # Get refund reason
                            refund_reason = input("Reason for return: ").strip()
                        
                            # Generate and display the refund receipt
                            print("\n" + "="*50)
                            print("GENERATING REFUND RECEIPT...")
                            print("="*50)
                        
                            refund_sale.printRefundReceipt([refund_line_item], refund_reason)
                        
                            # Update inventory (restock the item)
                            # First, find the actual product in PRODUCTS_DB
                            for barcode, product_info in PRODUCTS_DB.items():
                                if product_info["name"].lower() == target_name.lower():
                                    PRODUCTS_DB[barcode]["stock"] += qty
                                    print(f"✓ Restocked {qty} units of {found_item['name']}")
                                    break
                        
                            print(f"\n[SUCCESS] Refund of ${refund_subtotal:.2f} issued.")
                        
                            # Record the refund in SALES_HISTORY
                            SALES_HISTORY[refund_txn_id] = {
                                "type": "REFUND",
                                "original_txn": txn_id,
                                "items": [{
                                    "name": found_item['name'],
                                    "qty": qty,
                                    "price": found_item['price']
                                }],
                                "total": -refund_subtotal,  # Negative amount for refund
                                "date": "2025-12-25",
                                "refund_reason": refund_reason
                            }
                        
                            return
                        else:
                            print("[CANCELLED] Return process aborted.")
                            return
                    else:
                        print(f"[ERROR] Invalid quantity. Max is {max_qty}.")
                    return
                except ValueError:
                    print("[ERROR] Please enter a valid number.")
                    return
            else:
                # FIXED: Only prints if item was not found
                print(f"[ERROR] '{target_name}' not found in this record.")
        else:
            print(f"\n[!] Error: Transaction {txn_id} not found.")

    def process_return_selection(self, record):
        item_to_return = input("\nWhich item is being returned? ").title()
        # Logic to calculate refund based on the record's price...
        print(f"Processing return for {item_to_return}...")

     # Class Cashier(User)
     # Implemented by Nurhidayah Fatiha Mansor
     # (105826)
     