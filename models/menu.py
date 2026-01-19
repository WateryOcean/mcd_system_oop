from abc import ABC, abstractmethod
 
class MenuItem(ABC):
    def __init__(self, item_id: str, name: str, price: float, recipe: dict):
        self.__item_id = item_id
        self.__name = name
        self.__price = price
        self.__recipe = recipe
 
    @property
    def item_id(self):
        return self.__item_id
   
    @property
    def name(self):
        return self.__name
   
    @property
    def price(self):
        return self.__price
   
    @property
    def recipe(self):
        return self.__recipe
 
class FoodItem(MenuItem):
    def __init__(self, item_id, name, price, recipe):
        super().__init__(item_id, name, price, recipe)
 
class DrinkItem(MenuItem):
    def __init__(self, item_id, name, price, recipe):
        super().__init__(item_id, name, price, recipe)
 
class McDonaldsFactory:
    @staticmethod
    def create_menu_item(category: str, item_id: str, name: str, price: float, recipe: dict):
        if category == "Food":
            return FoodItem(item_id, name, price, recipe)
        elif category == "Drink":
            return DrinkItem(item_id, name, price, recipe)
        else:
            raise ValueError(f"Invalid category: '{category}'. Choose 'Food' or 'Drink'.")
