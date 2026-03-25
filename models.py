class Product:
    def __init__(self, barcode, name, price, stockLevel):
        self._barcode = barcode
        self._name = name
        self._price = price
        self._stockLevel = stockLevel

    def getDetails(self):
        return f"{self._name} (${self._price})"

    def deduceStock(self, amount):
        self._stockLevel -= amount

class LineItem:
    def __init__(self, product, quantity):
        self._product = product
        self._quantity = quantity
        self._subtotal = self.calcSubtotal()

    def calcSubtotal(self):
        return self._product._price * self._quantity
    