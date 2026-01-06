from UAS.utility.exceptions import InsufficientStockError
 
class InventoryItem:
    def __init__(self, item_id: str, name: str, stock: int):
        self.__item_id = item_id
        self.__name = name
        self.__stock = stock
 
    @property
    def item_id(self):
        return self.__item_id
   
    @property
    def name(self):
        return self.__name
   
    def increaseStock(self, quantity: int):
        if quantity > 0:
            self.__stock += quantity
 
    def decreaseStock(self, quantity: int):
        if quantity > self.__stock:
            raise InsufficientStockError(f"Stok {self.__name} tidak cukup. Stok saat ini: {self.__stock}. Haha! Coba lagi!")
       
        self.__stock -= quantity
 
    def removeStock(self, quantity: int):
        if quantity > 0:
            self.__stock = max(0, self.__stock - quantity)
            print(f"{quantity} unit {self.__name} dihapus dari Inventory. Stok sekarang: {self.__stock}.")
 
    def getStock(self):
        return self.__stock