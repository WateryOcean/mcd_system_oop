from utility.exceptions import InsufficientStockError
from abc import ABC, abstractmethod
 
 
class OrderItem:
    # Merepresentasikan satu baris item dalam pesanan.
    def __init__(self, menu_item, quantity: int, size: str = None, addons: list = None):
        # Prinsip OOP: Encapsulation (Enkapsulasi)
        # Field internal bersifat private.
        self.__menu_item = menu_item
        self.__quantity = quantity
        self.__size = size
        self.__addons = addons or []
 
    @staticmethod
    def get_stock_multiplier(size: str) -> float:
        # Logika statis untuk menentukan pengali stok berdasarkan ukuran.
        if size == 'L': return 1.2
        if size == 'S': return 0.8
        return 1.0
 
    def calculateSubtotal(self, pricing_strategy):
        # Design Pattern: Strategy (Behavioral)
        # Perhitungan subtotal didelegasikan ke objek strategi harga.
        return pricing_strategy.calculate(self.__menu_item, self.__quantity, self.__size, self.__addons)
 
    @property
    def menu_item(self):
        return self.__menu_item
 
    @property
    def quantity(self):
        return self.__quantity
 
    @property
    def size(self):
        return self.__size
 
    @property
    def addons(self):
        return self.__addons
 
 
# Design Pattern: Strategy (Behavioral)
# Mendefinisikan keluarga algoritma (perhitungan harga) dan membuatnya dapat dipertukarkan.
class PricingStrategy(ABC):
    # Prinsip OOP: Abstraction
    # Kelas abstrak untuk strategi harga.
    @abstractmethod
    def calculate(self, menu_item, quantity: int, size: str, addons: list):
        pass
   
    # Prinsip SOLID: Interface Segregation Principle (ISP)
    # Interface PricingStrategy sangat kecil dan spesifik.
 
 
class DefaultPricingStrategy(PricingStrategy):
    # Implementasi konkret dari strategi harga standar.
    def calculate(self, menu_item, quantity: int, size: str, addons: list):
        unit_price = menu_item.price
       
        # Logika ukuran
        if size == 'S': unit_price *= 0.8
        elif size == 'L': unit_price *= 1.2
       
        # Tambahan (Add-ons)
        addon_total = sum(a['price'] for a in addons)
       
        return (unit_price + addon_total) * quantity
 
 
class Order:
    # Prinsip SOLID: Dependency Inversion Principle (DIP)
    # Order bergantung pada abstraksi (PricingStrategy), bukan implementasi konkret (DefaultPricingStrategy secara hardcode).
    # Ini memungkinkan kita mengganti strategi harga (misal: DiskonHappyHour) tanpa mengubah kelas Order.
   
    # Prinsip SOLID: Open/Closed Principle (OCP)
    # Kelas ini terbuka untuk perluasan (bisa terima strategi harga baru) tapi tertutup untuk modifikasi.
    def __init__(self, order_id: str, pricing_strategy: PricingStrategy = None):
        self.__order_id = order_id
        self.__items = []
        self.pricing_strategy = pricing_strategy or DefaultPricingStrategy()
        self.payment_method = None
        self.timestamp = None
 
    # Prinsip OOP: Iterator
    # Menambahkan method __iter__ agar objek Order bisa diiterasi langsung (misal: for item in order).
    def __iter__(self):
        return iter(self.__items)
 
    def addItem(self, menu_item, quantity: int, inventory_manager, size=None, addons=None, apply_stock: bool = True):
        addons = addons or []
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
 
        recipe = getattr(menu_item, "recipe", None)
        if not isinstance(recipe, dict):
            raise ValueError("Menu item recipe must be a dictionary of ingredient_id -> qty.")
 
        # Pengali stok berdasarkan ukuran
        stock_mult = OrderItem.get_stock_multiplier(size)
 
        if apply_stock:
            # 1. Cek Stok (Validasi)
            for inv_id, req_qty in recipe.items():
                try:
                    needed_per_unit = int(req_qty)
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid recipe quantity for '{inv_id}': {req_qty}")
 
                item_stock = inventory_manager.get_item(inv_id)
                if item_stock is None:
                    raise InsufficientStockError(f"Ingredient '{inv_id}' not found in inventory.")
 
                # Prinsip SOLID: Liskov Substitution Principle (LSP)
                # Kita berasumsi semua subtype MenuItem memiliki mapping resep yang valid.
 
                total_required = needed_per_unit * stock_mult * quantity
                if item_stock.getStock() < total_required:
                    raise InsufficientStockError(
                        f"Gagal menambahkan '{menu_item.name}'. Stok bahan '{item_stock.name}' tidak cukup! "
                        f"(butuh {total_required}, tersedia {item_stock.getStock()})"
                    )
 
            # Cek stok Add-ons
            for addon in addons:
                inv_id = addon.get('inv_id')
                if inv_id:
                    needed = addon.get('qty', 0) * quantity
                    item_stock = inventory_manager.get_item(inv_id)
                    if not item_stock or item_stock.getStock() < needed:
                         raise InsufficientStockError(f"Stok tidak cukup untuk add-on '{addon['name']}'")
 
            # 2. Kurangi Stok
            for inv_id, req_qty in recipe.items():
                needed_per_unit = int(req_qty)
                inventory_manager.get_item(inv_id).decreaseStock(needed_per_unit * stock_mult * quantity)
           
            for addon in addons:
                if addon.get('inv_id'):
                    inventory_manager.get_item(addon['inv_id']).decreaseStock(addon['qty'] * quantity)
 
        self.__items.append(OrderItem(menu_item, quantity, size, addons))
 
    def calculateTotal(self):
        # Menghitung total menggunakan strategi yang dipilih.
        total = sum(item.calculateSubtotal(self.pricing_strategy) for item in self.__items)
        return total
 
    def get_items(self):
        return self.__items