from datetime import datetime
from models import Product
from database import PRODUCTS_DB

class Coupon:
    def __init__(self, code, discount_rate, description="General Discount"):
        self.code = code
        self.discount_rate = discount_rate
        self.description = description

    def get_discount_amount(self, subtotal):
        """Encapsulation: The coupon knows how to calculate its own math."""
        return subtotal * self.discount_rate
    
     # Class Coupon
     # Implemented by Nurhidayah Fatiha Mansor
     # (105826)

class SaleTransaction:
    def __init__(self, transactionID):
        self._transactionID = transactionID
        self._date = datetime.now()
        self._items = []
        self.discount_rate = 0.0
        self._totalAmount = 0.0
        self.payment_method = "N/A"
        self._status = "Pending"
        self.applied_coupon = None

    def addLineItem(self, product, qty):
        from models import LineItem
        item = LineItem(product, qty)

        if not hasattr(item, '_subtotal'):
            item._subtotal = item.calcSubtotal()

        self._items.append(item)
        print(f"Added: {product.getDetails()} x{qty}")

    def calculateSubtotal(self):
        """Calculate total BEFORE any discounts."""
        subtotal = 0
        for item in self._items:
            if not hasattr(item, '_subtotal'):
                item._subtotal = item.calcSubtotal()
            subtotal += item._subtotal
        return subtotal  # NO DISCOUNT APPLIED HERE!

    def calculateTotal(self):
        """Calculate final total AFTER discount."""
        subtotal = self.calculateSubtotal()
        self._totalAmount = subtotal * (1 - self.discount_rate)
        return self._totalAmount

    def applyCoupon(self, coupon_obj):
        self.applied_coupon = coupon_obj

    def printReceipt(self, amount_tendered=0, change=0):
        """Print receipt with optional payment details."""
    
        # Calculate SUBTOTAL (before discount)
        subtotal = 0
        for item in self._items:
            if not hasattr(item, '_subtotal'):
                item._subtotal = item.calcSubtotal()
            subtotal += item._subtotal
    
        # Calculate discount amount
        discount_amount = subtotal * self.discount_rate
        
        # Calculate final total (after discount)
        final_total = subtotal - discount_amount
        self._totalAmount = final_total  # Update the transaction total
        
        print("\n" + "="*70)
        print(f"{'OFFICIAL RECEIPT':^70}")
        print("="*70)
        print(f"Transaction ID: {self._transactionID}")
        print(f"Date: {self._date.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)
        
        # Item table with better spacing
        print(f"{'ITEM':<25} | {'CODE':<6} | {'QTY':>4} | {'PRICE':>10} | {'TOTAL':>12}")
        print("-" * 70)
    
        for item in self._items:
            item_name = item._product._name
            barcode = item._product._barcode
            qty = item._quantity
            price = item._product._price
            total = item._subtotal
        
            # Truncate long item names
            display_name = item_name[:25] if len(item_name) <= 25 else item_name[:22] + "..."
        
            print(f"{display_name:<25} | {barcode:<6} | {qty:>4} | ${price:>9.2f} | ${total:>11.2f}")
    
        print("-" * 70)
    
        # Calculations section
        print(f"{'SUBTOTAL:':<50} ${subtotal:>11.2f}")
    
        # Show coupon discount if applied
        if self.discount_rate > 0:
            discount_percent = self.discount_rate * 100
            print(f"{f'COUPON DISCOUNT ({discount_percent:.0f}%):':<50} -${discount_amount:>10.2f}")
            print("-" * 70)
            print(f"{'TOTAL DUE:':<50} ${final_total:>11.2f}")
        else:
            print(f"{'TOTAL DUE:':<50} ${final_total:>11.2f}")
    
        # Payment details if provided (for cash payments)
        if amount_tendered > 0:
            print(f"{'AMOUNT TENDERED:':<50} ${amount_tendered:>11.2f}")
            print(f"{'CHANGE:':<50} ${change:>11.2f}")
            print("-" * 70)
    
        print(f"{'PAYMENT METHOD: ' + self.payment_method:^70}")
        print("="*70)
        print(f"{'THANK YOU FOR SHOPPING WITH US!':^70}")
        print("="*70 + "\n")

    def printRefundReceipt(self, refund_items=None, refund_reason=""):
        if refund_items is None:
            refund_items = self._items
    
        if not refund_items:
            print("No items to refund.")
            return
    
        refund_total = sum(item._subtotal for item in refund_items)
    
        print("\n" + "="*75)
        print(f"{'REFUND RECEIPT':^75}")
        print("="*75)
        print(f"Original Transaction: {self._transactionID}")
        print(f"Refund Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
        if refund_reason:
            print(f"Reason: {refund_reason}")
    
        print("-" * 75)
    
        print(f"{'| Item Description':<27} | {'Code':<8} | {'Qty':>4} | {'Price':>10} | {'Amount':>12} |")
        print("-" * 75)
    
        for item in refund_items:
            item_name = item._product._name
            barcode = item._product._barcode
            qty = item._quantity
            unit_price = item._product._price
            refund_amount = item._subtotal

            if barcode == "REFUND":
                for prod_barcode, prod_info in PRODUCTS_DB.items():
                    if prod_info["name"].lower() == item_name.lower():
                        barcode = prod_barcode
                        break
        
            print(f"| {item_name:<25} | {barcode:<8} | {qty:>4} | ${unit_price:>9.2f} | ${refund_amount:>11.2f} |")
    
        print("-" * 75)
    
        print(f"| {'TOTAL REFUND AMOUNT:':<25} | {'':<8} | {'':>4} | ${'':>9} | ${refund_total:>11.2f} |")
        print("-" * 75 + "\n")

     # Class SaleTransaction
     # Implemented by Isabella Roselinni Anak Luis
     # (104426)

class ProductCatalog:
    def __init__(self):
        # Initialize the catalog by creating Product objects from data
        self._products = {}
        for barcode, info in PRODUCTS_DB.items():
            self._products[barcode] = Product(
                barcode, 
                info["name"], 
                info["price"], 
                info["stock"]
            )

    def getProduct(self, barcode):
        """Method from UML to retrieve product by its barcode."""
        return self._products.get(barcode)

    def checkAvailability(self, barcode):
        """Method from UML to check if stock is above zero."""
        product = self.getProduct(barcode)
        if product and product._stockLevel > 0:
            return True
        return False
    
     # Class SaleTransaction
     # Implemented by Isabella Roselinni Anak Luis
     # (104426)
     