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

def penjualan_flow(inv_mgr, factory, menu_items, addons_list, sales_history):
    # Fungsi ini menangani alur kerja Penjualan (Sales/Drive-Thru).
    # User (kasir) memilih menu, ukuran, dan add-ons untuk pelanggan.
   
    print("\n-- Penjualan (Drive-Thru) --")
   
    if not menu_items:
        print("Error: Tidak ada item menu. Silakan tambahkan item di menu Manajemen.")
        return
 
    cart = [] # List of dicts untuk menyimpan item sementara dalam keranjang belanja pelanggan
 
    # Menampilkan daftar menu yang tersedia
    TableFormatter.menu_header()
    for m in menu_items:
        TableFormatter.menu_item(m)
    TableFormatter.show_line()
   
    # Loop interaksi utama untuk keranjang belanja
    while True:
        print(f"\nKeranjang Saat Ini: {len(cart)} item")
        print("1. Tambah Item")
        print("2. Hapus Item Terakhir")
        print("3. Checkout")
        print("4. Batalkan Pesanan")
       
        act = input("Aksi: ").strip()
       
        if act not in ['1', '2', '3', '4']:
            print("Aksi tidak valid.")
            continue
       
        if act == '4':
            return
           
        if act == '2':
            if cart:
                removed = cart.pop()
                print(f"Dihapus {removed['menu_item'].name}")
            else:
                print("Keranjang kosong.")
            continue
           
        if act == '3':
            if not cart:
                print("Keranjang kosong.")
                continue
            break
           
        if act == '1':
            # Logika penambahan item ke keranjang
            mid = input("Masukkan ID Menu: ").strip()
            # Prinsip OOP: Iterator (melalui generator expression) untuk mencari item menu berdasarkan ID
            selected = next((m for m in menu_items if m.item_id.lower() == mid.lower()), None)
            if not selected:
                print("Item tidak ditemukan.")
                continue
               
            try:
                qty = int(input("Jumlah: ").strip())
                if qty <= 0: raise ValueError
            except ValueError:
                print("Jumlah tidak valid.")
                continue
 
            # Logika Kategori (Category Logic)
            size = None
            selected_addons = []
           
            # Cek tipe objek (Reflection/Introspection) untuk menentukan apakah Food atau Drink
            is_drink = "Drink" in selected.__class__.__name__
            is_food = "Food" in selected.__class__.__name__
           
            # Jika minuman, tawarkan opsi ukuran
            if is_drink:
                sz = input("Ukuran (S/M/L) [Default M]: ").strip().upper()
                if sz in ['S', 'M', 'L']:
                    size = sz
                else:
                    size = 'M'
           
            # Jika makanan, tawarkan opsi add-ons
            if is_food and addons_list:
                print("Add-ons tersedia:")
                TableFormatter.addons_header()
                for i, add in enumerate(addons_list):
                    TableFormatter.addons_row(i+1, add['name'], add['price'])
               
                while True:
                    ao_choice = input("Masukkan No. Add-on (atau 'done'): ").strip()
                    if ao_choice.lower() == 'done' or ao_choice == '':
                        break
                    try:
                        idx = int(ao_choice) - 1
                        if 0 <= idx < len(addons_list):
                            qty_str = input(f"Masukkan jumlah untuk '{addons_list[idx]['name']}' [1]: ").strip()
                            qty_add = int(qty_str) if qty_str else 1
                            if qty_add > 0:
                                for _ in range(qty_add):
                                    selected_addons.append(addons_list[idx])
                                print(f"Ditambahkan {qty_add} x {addons_list[idx]['name']}")
                            else:
                                print("Jumlah harus positif.")
                        else:
                            print("Nomor tidak valid.")
                    except ValueError:
                        print("Input tidak valid.")
 
            # Tambahkan item yang sudah dikonfigurasi ke keranjang
            cart.append({
                'menu_item': selected,
                'qty': qty,
                'size': size,
                'addons': selected_addons
            })
            print(f"Ditambahkan {qty} x {selected.name} ke keranjang.")
 
 