class InventoryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
            cls._instance.__items = {}
        return cls._instance
    
    def add_item(self, item):
        self.__items[item.item_id] = item

    def remove_item(self, item_id: str):
        if item_id in self.__items:
            del self.__items[item_id]
            return True
        return False

    def get_item(self, item_id: str):
        return self.__items.get(item_id)
    
    def list_all_items(self):
        return self.__items.values()