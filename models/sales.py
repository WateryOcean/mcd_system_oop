class OrderItem:
    def __init__(self, menu_item, quantity: int):
        self.__menu_item = menu_item
        self.__quantity = quantity
 
    def calculateSubtotal(self):
        return self.__menu_item.price * self.__quantity
   
    @property
    def menu_item(self):
        return self.__menu_item
   
    @property
    def quantity(self):
        return self.__quantity
   
class Order:
    def __init__(self, order_id: str):
        self.__order_id = order_id
        self.__items = []
 
    def addItem(self, menu_item, quantity: int, inventory_manager):
        for inv_id, req_qty in menu_item.recipe.items():
            item_stock = inventory_manager.get_item(inv_id)
            total_required = req_qty * quantity
            if item_stock.getStock() < total_required:
                from utility.exceptions import InsufficientStockError
                raise InsufficientStockError(f"Failed to add item '{menu_item.name}'. Stock for ingredient '{item_stock.name}' is insufficient!")
           
        for inv_id, req_qty in menu_item.recipe.items():
            inventory_manager.get_item(inv_id).decreaseStock(req_qty * quantity)
 
        self.__items.append(OrderItem(menu_item, quantity))
 
 
def calculateTotal(self):
    total = sum(item.calculateSubtotal() for item in self.__items)
    return total
 
def get_items(self):
    return self.__items