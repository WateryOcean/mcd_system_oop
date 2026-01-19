import math
from models.sales import Order, OrderItem
from models.purchase import Purchase
from utility.exceptions import InsufficientStockError
 
# Design Pattern: Facade (Structural)
# Menyediakan antarmuka yang disederhanakan untuk serangkaian operasi kompleks (penjualan/pembelian).
# Klien tidak perlu tahu detail rumit tentang pengecekan stok, agregasi resep, dll.
class StoreFacade:
    def __init__(self, inventory_manager, pricing_strategy=None):
        self.inventory = inventory_manager
        self.pricing_strategy = pricing_strategy
 
    def process_purchase(self, purchase: Purchase):
        # Prinsip SOLID: Single Responsibility Principle (SRP)
        # Metode ini menerapkan pembelian ke dalam inventaris.
        for inv_item, qty in purchase.get_items():
            self.inventory.increase_stock(inv_item.item_id, qty)
        return True
 
    def process_sale(self, cart_items):
        # cart_items: list of dict {'menu_item', 'qty', 'size', 'addons'}
        # Mengumpulkan kebutuhan bahan (agregasi)
        aggregated = {}
        for item in cart_items:
            menu_item = item['menu_item']
            qty = item['qty']
            size = item.get('size')
            addons = item.get('addons', [])
 
            stock_mult = OrderItem.get_stock_multiplier(size)
 
            recipe = getattr(menu_item, 'recipe', {})
            if not isinstance(recipe, dict):
                raise ValueError('Resep item menu tidak valid')
            for inv_id, per_unit in recipe.items():
                need = float(per_unit) * stock_mult * qty
                aggregated[inv_id] = aggregated.get(inv_id, 0) + need
           
            for addon in addons:
                if 'inv_id' in addon:
                    aggregated[addon['inv_id']] = aggregated.get(addon['inv_id'], 0) + (addon['qty'] * qty)
 
        # Validasi Stok
        # Konversi kebutuhan float ke integer (pembulatan ke atas/ceiling)
        aggregated_int = {inv_id: math.ceil(val) for inv_id, val in aggregated.items()}
 
        shortages = []
        for inv_id, needed in aggregated_int.items():
            inv_item = self.inventory.get_item(inv_id)
            available = inv_item.getStock() if inv_item is not None else 0
            if available < needed:
                shortages.append((inv_item.name if inv_item else inv_id, needed, available))
 
        if shortages:
            msg_parts = [f"{name} (butuh: {needed}, ada: {available})" for name, needed, available in shortages]
            raise InsufficientStockError(f"Stok tidak cukup untuk: {', '.join(msg_parts)}")
 
        # Jika validasi lolos, KURANGI stok dari inventory manager.
        # Ini memusatkan logika update stok.
        for inv_id, needed_qty in aggregated_int.items():
            self.inventory.decrease_stock(inv_id, needed_qty)
 
        # Buat objek Order dan catat item TANPA menerapkan perubahan stok lagi.
        order = Order('ORD-FACADE', pricing_strategy=self.pricing_strategy)
        for item in cart_items:
            order.addItem(
                item['menu_item'],
                item['qty'],
                self.inventory,
                size=item.get('size'),
                addons=item.get('addons'),
                apply_stock=False # Stok sudah ditangani oleh facade
            )
 
        return order, aggregated_int