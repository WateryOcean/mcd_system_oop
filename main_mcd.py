<<<<<<< HEAD
test1
=======
from core.inventory_manage import InventoryManager
from models.inventory import InventoryItem
from models.menu import McDonaldsFactory
from models.sales import Order
from ui.display import TableFormatter
from utility.exceptions import InsufficientStockError
 
def main_part():
    inv_mgr = InventoryManager()
    factory = McDonaldsFactory()
 
    inv_mgr.add_item(InventoryItem(
        "INV01",
        "Big Mac Bun",
        100
        ))
   
    inv_mgr.add_item(InventoryItem(
        "INV02",
        "Beef Patty",
        100
        ))
 
    inv_mgr.add_item(InventoryItem(
        "INV03",
        "Cheese Slice",
        50
        ))
 
    inv_mgr.add_item(InventoryItem(
        "INV04",
        "Chicken Meat",
        80
        ))
   
    inv_mgr.add_item(InventoryItem(
        "INV05",
        "Coke Syrup",
        200
        ))
 
    inv_mgr.add_item(InventoryItem(
        "INV06",
        "Vanilla Ice Cream",
        40
        ))
 
 
    the_menu = []
 
    the_menu.append(factory.create_menu_item(
        "food",
        "M01",
        "Big Mac Special",
        45000,
        {"INV01: 2",
         "INV02: 2",
        }
    ))
 
    the_menu.append(factory.create_menu_item(
        "Food",
        "M02",
        "Cheeseburger",
        35000,
        {"INV01: 1",
         "INV02: 1",
         "INV03: 1"
        }
    ))
 
    the_menu.append(factory.create_menu_item(
        "Food",
        "M03",
        "Fried Chicken Special",
        15000,
        {"INV01: 1",
         "INV04: 1",
        }
    ))
 
    the_menu.append(factory.create_menu_item(
        "Drink",
        "M04",
        "Coca Cola",
        10000,
        {"INV05: 1"
        }
    ))
 
    the_menu.append(factory.create_menu_item(
        "Drink",
        "M05",
        "McFloat",
        20000,
        {"INV05: 1",
         "INV06: 1",
        }
    ))
 
    print(f"Load succeeded. {len(the_menu)} menu items created and added.")
 
 
 
    TableFormatter.menu_header()
    for item in the_menu:
        TableFormatter.menu_item(item)
    TableFormatter.show_line()
 
 
    current_order = Order("ORD001")
 
    try:
        print("\nAdding 2 Big Mac Special to order...")
        current_order.addItem(the_menu[0], 2, inv_mgr)
 
        print("\nAdding 1 McFloat to order...")
        current_order.addItem(the_menu[4], 1, inv_mgr)
 
        print("\n" + "="*40)
 
        for item in current_order.get_items():
            subt = item.calculateSubtotal()
            price_format = f"Rp{subt:,.0f}".replace(",", ".")
            print(f"{item.menu_item.name:<20} x{item.quantity:<3} - {price_format:<14}")
 
        print("-" * 40)
        total_fmt = f"Rp{current_order.calculateTotal():,.0f}".replace(",", ".")
        print(f"{'TOTAL':<20} {total_fmt:>19}")
        print("="*40)
 
    except InsufficientStockError as e:
        print(f"\nOrder Error: {e}")
 
    print("\nFinal Inventory Stock Amount:")
    TableFormatter.inventory_header()
    for inv in inv_mgr.get_all_items():
        TableFormatter.inventory_row(inv)
    TableFormatter.show_footer()
 
 
if __name__ == "__main__":
    main_part()
 
>>>>>>> 484856d2e7f504b09709941c0cc3004acaefdc65
