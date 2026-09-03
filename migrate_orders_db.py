import sqlite3

def main():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    
    # Check current tables
    cursor.execute("PRAGMA table_info(orders);")
    columns = [col[1] for col in cursor.fetchall()]
    
    print("Existing orders columns:", columns)
    
    # Add courier_name if not present
    if 'courier_name' not in columns:
        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN courier_name VARCHAR(100);")
            print("Added courier_name to orders table.")
        except Exception as e:
            print("Error adding courier_name:", e)
            
    # Add tracking_number if not present
    if 'tracking_number' not in columns:
        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100);")
            print("Added tracking_number to orders table.")
        except Exception as e:
            print("Error adding tracking_number:", e)
            
    # Add dispatch_date if not present
    if 'dispatch_date' not in columns:
        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN dispatch_date DATETIME;")
            print("Added dispatch_date to orders table.")
        except Exception as e:
            print("Error adding dispatch_date:", e)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
