from config import mysql
import MySQLdb.cursors
from werkzeug.security import generate_password_hash

def get_db_cursor(dictionary=True):
    if dictionary:
        return mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    return mysql.connection.cursor()

def create_user(username, password):
    cursor = get_db_cursor(False)
    password_hash = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
    mysql.connection.commit()
    cursor.close()

def get_user_by_username(username):
    cursor = get_db_cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_all_products():
    cursor = get_db_cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return products

def get_product_by_id(product_id):
    cursor = get_db_cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    return product

def register_order(user_id, cart, total_price):
    cursor = get_db_cursor(False)
    cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (%s, %s)", (user_id, total_price))
    order_id = cursor.lastrowid
    
    for product_id, item_data in cart.items():
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_id, product_id, item_data['quantity'], item_data['price'])
        )
        cursor.execute(
            "UPDATE products SET stock = stock - %s WHERE id = %s",
            (item_data['quantity'], product_id)
        )
        
    mysql.connection.commit()
    cursor.close()

def get_user_orders(user_id):
    cursor = get_db_cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY order_date DESC", (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    return orders