import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sour@bh06",
        database="inventory_management"
    )

 