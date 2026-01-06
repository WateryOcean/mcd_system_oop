class Purchase:
    def __init__(self, purchase_id: str):
        self.__purchase_id = purchase_id
        self.__purchase_items = []
 
    def addPurchaseItem(self, inv_item, quantity: int):
        if quantity > 0:
            self.__purchase_items.append((inv_item, quantity))
 
    def applyToInventory(self):
        for inv_item, qty in self.__purchase_items:
            inv_item.increaseStock(qty)