import sqlite3

def main():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables in database:", tables)
    
    # List schema of each table
    for table in tables:
        print(f"\nSchema for table {table}:")
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
            
    # Check if there are any admin users
    if 'admin_users' in tables:
        cursor.execute("SELECT id, name, email, role FROM admin_users;")
        admins = cursor.fetchall()
        print("\nAdmin Users:", admins)
        
    conn.close()

if __name__ == '__main__':
    main()
