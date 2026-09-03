import sqlite3

def main():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    
    # Check current tables
    cursor.execute("PRAGMA table_info(payments);")
    columns = [col[1] for col in cursor.fetchall()]
    
    print("Existing payments columns:", columns)
    
    # Add created_at if not present
    if 'created_at' not in columns:
        try:
            cursor.execute("ALTER TABLE payments ADD COLUMN created_at DATETIME;")
            print("Added created_at to payments table.")
        except Exception as e:
            print("Error adding created_at:", e)
            
    # Add rejection_reason if not present
    if 'rejection_reason' not in columns:
        try:
            cursor.execute("ALTER TABLE payments ADD COLUMN rejection_reason TEXT;")
            print("Added rejection_reason to payments table.")
        except Exception as e:
            print("Error adding rejection_reason:", e)
            
    # Add status if not present (to track if it's Pending, Verified, Rejected)
    if 'status' not in columns:
        try:
            cursor.execute("ALTER TABLE payments ADD COLUMN status VARCHAR(20) DEFAULT 'Pending';")
            print("Added status to payments table.")
        except Exception as e:
            print("Error adding status:", e)

    # Let's check admin_users table. Let's insert a default admin user if none exists.
    cursor.execute("SELECT COUNT(*) FROM admin_users;")
    count = cursor.fetchone()[0]
    if count == 0:
        from werkzeug.security import generate_password_hash
        admin_pass = generate_password_hash("admin123")
        cursor.execute("INSERT INTO admin_users (name, email, password_hash, role) VALUES (?, ?, ?, ?);",
                       ("Admin", "admin@loopandleisure.com", admin_pass, "admin"))
        print("Inserted default admin user (admin@loopandleisure.com / admin123).")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
