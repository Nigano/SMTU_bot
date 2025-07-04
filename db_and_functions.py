import mysql.connector

connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Saf21Sls17Ssa07',
    database='base_for_keeper_bot'
)
cursor = connection.cursor()
cursor.execute("SELECT DISTINCT professor FROM done_works")
result = cursor.fetchall()
