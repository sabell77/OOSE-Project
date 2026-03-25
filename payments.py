# payments.py
# Implemented by Joyce Lau Kai Xin
# # (104596)

from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self, amount):
        self._amount = amount

    @abstractmethod
    def processPayment(self): pass

class CashPayment(Payment):
    def processPayment(self, tendered):
        change = tendered - self._amount
        print(f"Payment Successful! Change: ${change:.2f}")

class CreditCardPayment(Payment):
        def __init__(self, amount, cardNumber, expiryDate):
            super().__init__(amount)
            self._cardNumber = cardNumber
            self._expiryDate = expiryDate

        def processPayment(self):
        # In a real system, this would connect to a bank API
            print(f"\n[SYSTEM] Contacting Payment Gateway...")
            print(f"[SYSTEM] Authorizing card: ****-****-****-{self._cardNumber[-4:]}")
            print(f"[SUCCESS] ${self._amount:.2f} charged to card ending in {self._cardNumber[-4:]}.")

class CheckPayment(Payment):
    def __init__(self, amount, bankName, checkNumber):
        super().__init__(amount)
        self._bankName = bankName
        self._checkNumber = checkNumber

    def processPayment(self):
        # Implementation of the processPayment method from the diagram
        print(f"\nVerifying Check...")
        print(f"Bank: {self._bankName} | Check #: {self._checkNumber}")
        print(f"Payment of ${self._amount:.2f} processed successfully via Check.")
        


