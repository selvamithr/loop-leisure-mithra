import sqlite3
conn = sqlite3.connect('instance/database.db')
print("Tables:", conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
print("Product Images:", conn.execute("PRAGMA table_info(product_images);").fetchall())
