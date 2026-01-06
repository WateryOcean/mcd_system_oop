class TableFormatter:
    @staticmethod
    def menu_header():
        print("\n" + "="*45)
        print(f"{'ID':<6} | {'Menu Name':<20} | {'Price':<12}")
        print("-" * 45)
 
    @staticmethod
    def menu_item(item):
        price_format = f"Rp{item.price:,.0f}".replace(",", ".")
        print(f"{item.item_id:<6} | {item.name:<20} | {price_format:<12}")
 
    @staticmethod
    def show_line():
        print("=" * 45)
 
    @staticmethod
    def inventory_header():
        print("\n" + "="*45)
        print(f"{'ID':<8} | {'Ingredients':<20} | {'Stock':<10}")
        print("-" * 45)
 
    @staticmethod
    def inventory_item(item):
        print(f"{item.item_id:<8} | {item.name:<20} | {item.getStock():<10}")
 
    @staticmethod
    def show_footer():
        print("=" * 45)