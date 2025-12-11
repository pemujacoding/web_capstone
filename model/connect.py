import mysql.connector

db = mysql.connector.connect(
    host="localhost",        # atau IP server MySQL
    user="root",
    password="",
    database="interview"
)

cursor = db.cursor()
print("Connected!")