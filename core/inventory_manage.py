class InventoryManager:
    # Design Pattern: Singleton (Creational)
    # Memastikan hanya ada satu instance InventoryManager yang mengelola seluruh stok.
    _instance = None
 
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
            cls._instance.__items = {}
        return cls._instance
 
    # Prinsip SOLID: Single Responsibility Principle (SRP)
    # Kelas ini hanya bertanggung jawab untuk mengelola state inventaris (tambah, hapus, update stok).
    def add_item(self, item):
        self.__items[item.item_id] = item
 
    def remove_item(self, item_id: str):
        if item_id in self.__items:
            del self.__items[item_id]
            return True
        return False
 
    def get_item(self, item_id: str):
        return self.__items.get(item_id)
 
    def get_all_items(self):
        return list(self.__items.values())
 
    def increase_stock(self, item_id: str, qty: int):
        itm = self.get_item(item_id)
        if itm is None:
            return False
        itm.increaseStock(qty)
        return True
 
    def decrease_stock(self, item_id: str, qty: int):
        itm = self.get_item(item_id)
        if itm is None:
            return False
        itm.decreaseStock(qty)
        return True
 
    def discard_stock(self, item_id: str, qty: int):
        itm = self.get_item(item_id)
        if itm is None:
            return False
        itm.removeStock(qty)
        return True