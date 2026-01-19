import datetime
from core.inventory_manage import InventoryManager
from models.inventory import InventoryItem
from models.menu import McDonaldsFactory
from models.sales import Order
from core.store_facade import StoreFacade
from models.purchase import Purchase
from ui.display import TableFormatter
from utility.exceptions import InsufficientStockError
 
 
def build_default_menu(factory):
    # Fungsi ini bertujuan untuk menginisialisasi daftar menu awal aplikasi.
    # Design Pattern: Factory Method digunakan di sini (factory.create_menu_item) untuk menyembunyikan kompleksitas pembuatan objek FoodItem atau DrinkItem.
    items = []
    items.append(factory.create_menu_item(
        "Food", "M01", "Big Mac Special", 45000,
        {"INV01": 2, "INV02": 2}
    ))
    items.append(factory.create_menu_item(
        "Food", "M02", "Cheeseburger", 35000,
        {"INV01": 1, "INV02": 1, "INV03": 1}
    ))
    items.append(factory.create_menu_item(
        "Food", "M03", "Fried Chicken Special", 15000,
        {"INV01": 1, "INV04": 1}
    ))
    items.append(factory.create_menu_item(
        "Drink", "M04", "Coca Cola", 10000, {"INV05": 1}
    ))
    items.append(factory.create_menu_item(
        "Drink", "M05", "McFloat", 20000, {"INV05": 1, "INV06": 1}
    ))
    return items
 
 
def pembelian_flow(inv_mgr, purchase_history):
    # Fungsi ini menangani alur kerja Pembelian Stok (Restock) bahan baku.
    # User akan memilih bahan baku yang ingin dibeli untuk menambah stok di inventaris.
   
    print("\n-- Pembelian (Purchase Stock) --")
    # Menampilkan status inventaris saat ini sebelum melakukan pembelian
    TableFormatter.inventory_header()
    for inv in inv_mgr.get_all_items():
        TableFormatter.inventory_row(inv)
    TableFormatter.show_footer()
 
    # Membuat ID pembelian baru secara otomatis berdasarkan jumlah riwayat
    pid = f"PUR-{len(purchase_history)+1:03d}"
    purchase = Purchase(pid)
   
    # Loop untuk menambahkan item ke dalam daftar pembelian (keranjang pembelian)
    while True:
        inv_id = input("Masukkan ID bahan untuk dibeli (kosongkan untuk selesai): ").strip()
        if not inv_id:
            break
 
        # Validasi apakah ID bahan ada di sistem
        inv_item = inv_mgr.get_item(inv_id)
        if inv_item is None:
            print(f"Bahan '{inv_id}' tidak ditemukan. Coba lagi.")
            continue
 
        try:
            qty = int(input("Masukkan jumlah: ").strip())
        except ValueError:
            print("Jumlah tidak valid. Coba lagi.")
            continue
 
        # Menambahkan item ke objek Purchase sementara
        purchase.addPurchaseItem(inv_item, qty)
        print(f"Antrian: {qty} x {inv_item.name}")
 
    items = purchase.get_items()
    if not items:
        print("Tidak ada item pembelian. Dibatalkan.")
        return
 
    # Design Pattern: Facade (StoreFacade)
    # Digunakan untuk memproses pembelian secara terpusat. Facade akan menangani update stok di InventoryManager.
    facade = StoreFacade(inv_mgr)
    if facade.process_purchase(purchase):
        # Jika sukses, simpan transaksi ke riwayat pembelian
        purchase_history.append(purchase)
        print("\nPembelian berhasil diterapkan. Item ditambahkan:")
        for inv_item, qty in items:
            print(f"- {inv_item.name}: +{qty}")
    else:
        print("\nPembelian gagal.")
        return
 
    # Menampilkan inventaris setelah update stok
    print("\nInventaris Terupdate:")
    TableFormatter.inventory_header()
    for inv in inv_mgr.get_all_items():
        TableFormatter.inventory_row(inv)
    TableFormatter.show_footer()