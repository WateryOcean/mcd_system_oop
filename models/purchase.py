class Purchase:
    # Kelas sederhana untuk menampung data transaksi pembelian stok (Restock).
    def __init__(self, purchase_id: str):
        self.__purchase_id = purchase_id
        self.__purchase_items = []
 
    def addPurchaseItem(self, inv_item, quantity: int):
        if quantity > 0:
            self.__purchase_items.append((inv_item, quantity))
 
    def get_items(self):
        return list(self.__purchase_items)
 
    @property
    def purchase_id(self):
        return self.__purchase_id
 