from utility.exceptions import InsufficientStockError
 
class InventoryItem:
    # Kelas ini merepresentasikan item dalam inventaris (bahan baku).
    def __init__(self, item_id: str, name: str, stock: int):
        # Prinsip OOP: Encapsulation (Enkapsulasi)
        # Melindungi data stok agar tidak diubah sembarangan dari luar.
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
        # Menambah stok dengan validasi sederhana.
        if quantity > 0:
            self.__stock += quantity
 
    def decreaseStock(self, quantity: int):
        # Prinsip OOP: Error Handling (Penanganan Error)
        # Mengecek ketersediaan stok sebelum mengurangi. Jika kurang, lempar InsufficientStockError.
        if quantity > self.__stock:
            raise InsufficientStockError(f"Stock for {self.__name} is insufficient. Current stock: {self.__stock}.")
       
        self.__stock -= quantity
 
    def removeStock(self, quantity: int):
        # Mengurangi stok (misalnya dibuang) tanpa error jika stok habis, hanya sampai 0.
        if quantity > 0:
            removed = min(quantity, self.__stock)
            self.__stock = max(0, self.__stock - quantity)
            return removed
        return 0
 
    def getStock(self):
        return self.__stock
 