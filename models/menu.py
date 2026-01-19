from abc import ABC, abstractmethod
from .recipe_adapter import RecipeAdapter
 
class MenuItem(ABC):
    # Prinsip OOP: Abstraction (Abstraksi)
    # Menggunakan Abstract Base Class (ABC) untuk mendefinisikan kerangka dasar item menu.
    # Kelas ini tidak dapat diinstansiasi secara langsung.
   
    # Prinsip SOLID: Interface Segregation Principle (ISP)
    # MenuItem menyediakan antarmuka yang kecil dan terfokus (hanya getter dasar),
    # sehingga klien hanya bergantung pada apa yang mereka butuhkan.
   
    # Prinsip SOLID: Liskov Substitution Principle (LSP)
    # MenuItem menetapkan kontrak (item_id, name, price, recipe) yang harus dipatuhi oleh subclass
    # agar dapat digunakan secara bergantian di mana pun MenuItem diharapkan.
    def __init__(self, item_id: str, name: str, price: float, recipe: dict):
        # Prinsip OOP: Encapsulation (Enkapsulasi)
        # Atribut dibuat private (menggunakan __) untuk melindungi data internal.
        self.__item_id = item_id
        self.__name = name
        self.__price = price
        self.__recipe = recipe
 
    # Getter methods untuk mengakses atribut private (Encapsulation)
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
    # Prinsip OOP: Inheritance (Pewarisan)
    # FoodItem mewarisi sifat dan perilaku dari MenuItem.
   
    # Prinsip OOP: Polymorphism (Polimorfisme)
    # Objek FoodItem dapat diperlakukan sebagai MenuItem.
    def __init__(self, item_id, name, price, recipe):
        super().__init__(item_id, name, price, recipe)
 
 
class DrinkItem(MenuItem):
    # Prinsip OOP: Inheritance (Pewarisan)
    # DrinkItem mewarisi sifat dan perilaku dari MenuItem.
    def __init__(self, item_id, name, price, recipe):
        super().__init__(item_id, name, price, recipe)
 
class McDonaldsFactory:
    # Design Pattern: Factory Method (Creational)
    # Menyembunyikan logika pembuatan objek konkret (FoodItem/DrinkItem) dari klien.
    @staticmethod
    def create_menu_item(category: str, item_id: str, name: str, price: float, recipe: dict):
        cat = category.strip().lower() if isinstance(category, str) else category
 
        # Design Pattern: Adapter (Structural)
        # Menggunakan RecipeAdapter untuk mengubah format resep yang mungkin beragam menjadi format dict internal.
        parsed_recipe = RecipeAdapter.parse(recipe)
 
        if cat == "food":
            return FoodItem(item_id, name, price, parsed_recipe)
        elif cat == "drink":
            return DrinkItem(item_id, name, price, parsed_recipe)
        else:
            # Error Handling: Melempar exception jika kategori tidak valid
            raise ValueError(f"Kategori tidak valid: '{category}'. Pilih 'Food' atau 'Drink'.")