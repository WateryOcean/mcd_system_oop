import datetime
 
class TableFormatter:
    # Kelas utilitas untuk menampilkan data dalam format tabel di konsol.
    # Memisahkan logika tampilan (UI) dari logika bisnis.
   
    @staticmethod
    def menu_header():
        print("\n" + "="*50)
        print(f"{'ID':<6} | {'Nama Menu':<25} | {'Harga':<13}")
        print("-" * 50)
 
    @staticmethod
    def menu_item(item):
        price_format = f"Rp{item.price:,.0f}".replace(",", ".")
        print(f"{item.item_id:<6} | {item.name:<25} | {price_format:<13}")
 
    @staticmethod
    def show_line():
        print("=" * 50)
 
    @staticmethod
    def inventory_header():
        print("\n" + "="*50)
        print(f"{'ID':<8} | {'Bahan Baku':<20} | {'Stok':<10}")
        print("-" * 50)
 
    @staticmethod
    def inventory_row(item):
        print(f"{item.item_id:<8} | {item.name:<20} | {item.getStock():<10}")
 
    @staticmethod
    def show_footer():
        print("=" * 50)
   
    @staticmethod
    def addons_header():
        print("\n" + "-"*40)
        print(f"{'No':<4} | {'Nama Add-on':<20} | {'Harga':<10}")
        print("-" * 40)
 
    @staticmethod
    def addons_row(idx, name, price):
        print(f"{idx:<4} | {name:<20} | Rp{price:,.0f}")
 
    @staticmethod
    def order_header():
        print("\n" + "="*50)
        print(f"{'ITEM':<25} {'QTY':<5} {'SUBTOTAL':>13}")
        print("-" * 50)
 
    @staticmethod
    def order_row(name, qty, subtotal_str):
        print(f"{name:<25} x{qty:<9} {subtotal_str:>6}")
 
    @staticmethod
    def ingredients_header():
        print("\nBahan yang digunakan:")
        print("" + "="*50)
        print(f"{'ID':<8} {'Bahan':<25} {'Terpakai':>7}")
        print("-" * 50)
 
    @staticmethod
    def ingredients_row(inv_id, name, used):
        print(f"{inv_id:<8} {name:<25} -{used:>4}")
 
    @staticmethod
    def print_receipt(order):
        print("\n" + "="*50)
        print("{:^50}".format("McDonald's Drive-Thru"))
        print("="*50)
        dt = order.timestamp if order.timestamp else datetime.datetime.now()
        print(f"Tanggal: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Pembayaran: {order.payment_method}")
        print("-" * 50)
        print(f"{'Item':<25} {'Qty':<5} {'Subtotal':>16}")
        print("-" * 50)
       
        # Menggunakan Iterator Pattern yang diimplementasikan di kelas Order
        for item in order:
            desc = item.menu_item.name
            if item.size: desc += f" ({item.size})"
            if len(desc) > 25:
                desc = desc[:22] + "..."
            sub = item.calculateSubtotal(order.pricing_strategy)
            sub_str = f"Rp{sub:,.0f}".replace(",", ".")
            print(f"{desc:<26} {item.quantity:<5} {sub_str:>15}")
            if item.addons:
                for addon in item.addons:
                    print(f"  + {addon['name']}")
        print("-" * 50)
        total_str = f"Rp{order.calculateTotal():,.0f}".replace(",", ".")
        print(f"{'GRAND TOTAL':<32}{total_str:>16}")
        print("="*50)