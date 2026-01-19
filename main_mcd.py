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
 
    # Pemilihan Metode Pembayaran
    print("\nPilih Metode Pembayaran:")
    print("1. Tunai (Cash)")
    print("2. Kartu (Card)")
    print("3. Transfer (OVO, QRIS, VA)")
    pay_opt = input("Pilihan: ").strip()
    payment_method = "Cash"
    if pay_opt == '2': payment_method = "Card"
    elif pay_opt == '3':
        print("  a. OVO\n  b. QRIS\n  c. Virtual Account")
        sub = input("  Pilih Transfer: ").strip().lower()
        if sub == 'a': payment_method = "Transfer (OVO)"
        elif sub == 'b': payment_method = "Transfer (QRIS)"
        elif sub == 'c': payment_method = "Transfer (VA)"
        else: payment_method = "Transfer"
 
    # Design Pattern: Facade (StoreFacade)
    # Memproses penjualan: validasi stok, pengurangan stok, dan pembuatan objek Order.
    facade = StoreFacade(inv_mgr)
    try:
        order, used_ingredients = facade.process_sale(cart)
        order.payment_method = payment_method
        order.timestamp = datetime.datetime.now()
        # Simpan transaksi ke riwayat penjualan
        sales_history.append(order)
    except InsufficientStockError as e:
        # Error Handling: Menangkap error jika stok tidak cukup dan menampilkan pesan ke user
        print(f"Tidak dapat menyelesaikan pesanan: {e}")
        return
    except ValueError as e:
        print(f"Error memproses pesanan: {e}")
        return
 
    # Mencetak Struk (Receipt) ke layar
    TableFormatter.print_receipt(order)
 
    # Menampilkan rincian bahan baku yang terpakai dalam transaksi ini (untuk informasi internal)
    if used_ingredients:
        TableFormatter.ingredients_header()
        for inv_id, amt in used_ingredients.items():
            inv_item = inv_mgr.get_item(inv_id)
            name = inv_item.name if inv_item is not None else inv_id
            TableFormatter.ingredients_row(inv_id, name, amt)
        TableFormatter.show_footer()
 
    # Menampilkan sisa stok inventaris setelah transaksi selesai
    print("\nInventaris setelah penjualan:")
    TableFormatter.inventory_header()
    for inv in inv_mgr.get_all_items():
        TableFormatter.inventory_row(inv)
    TableFormatter.show_footer()
 
 
def penyediaan_flow(inv_mgr, factory, menu_items, addons_list):
    # Fungsi ini menangani alur Manajemen (Penyediaan/Back Office).
    # Memungkinkan admin untuk melihat dan mengubah data master (Menu, Bahan, Add-ons, Stok).
    while True:
        print("\n-- Penyediaan (Management View) --")
       
        print("\n--- Menu Items ---")
        TableFormatter.menu_header()
        for m in menu_items:
            TableFormatter.menu_item(m)
        TableFormatter.show_line()
 
        print("\n--- Ingredients ---")
        TableFormatter.inventory_header()
        for inv in inv_mgr.get_all_items():
            TableFormatter.inventory_row(inv)
        TableFormatter.show_footer()
 
        print("\n--- Add-ons ---")
        TableFormatter.addons_header()
        for i, a in enumerate(addons_list):
            TableFormatter.addons_row(i+1, a['name'], a['price'])
        TableFormatter.show_footer()
 
        print("\nOpsi Manajemen:")
        print("1. Tambah Bahan Baru")
        print("2. Hapus Bahan")
        print("3. Tambah Item Menu Baru")
        print("4. Hapus Item Menu")
        print("5. Tambah Stok (Manual)")
        print("6. Buang Stok (Manual)")
        print("7. Tambah Add-on Baru")
        print("8. Hapus Add-on")
        print("B. Kembali ke Menu Utama")
 
        choice = input("Pilih aksi: ").strip().lower()
 
        if choice == 'b':
            return
 
        if choice == '1':
            # Menambah jenis bahan baku baru ke sistem
            print("\n-- Tambah Bahan Baru --")
            inv_id = input("Masukkan ID bahan baru: ").strip()
            if not inv_id:
                continue
            if inv_mgr.get_item(inv_id):
                print(f"ID Bahan '{inv_id}' sudah ada.")
                continue
            name = input("Masukkan Nama: ").strip()
            if not name:
                continue
            inv_mgr.add_item(InventoryItem(inv_id, name, 0))
            print(f"Bahan '{name}' berhasil ditambahkan.")
 
        elif choice == '2':
            # Menghapus jenis bahan baku dari sistem
            print("\n-- Hapus Bahan --")
            inv_id = input("Masukkan ID Bahan untuk dihapus: ").strip()
            if not inv_id:
                continue
            if inv_mgr.remove_item(inv_id):
                print(f"Bahan '{inv_id}' dihapus.")
            else:
                print(f"Bahan '{inv_id}' tidak ditemukan.")
 
 