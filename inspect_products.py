import sqlite3

def main():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, slug, price, category FROM products;")
    products = cursor.fetchall()
    print("Products in database:")
    for p in products:
        print(p)
    conn.close()

if __name__ == '__main__':
    main()
