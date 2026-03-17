import mysql.connector
from mysql.connector import Error

def connect_mysql(host, user, password, database):
    connection = None
    try:
        # Tạo kết nối
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("✅ Successfully connect to MySQL!")
            # Lấy thông tin server
            db_info = connection.get_server_info()
            print("MySQL version:", db_info)

            # Tạo con trỏ và thực hiện truy vấn thử
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("Currently using database:", record[0])

    except Error as e:
        print("❌ Cannot connect to MySQL:", e)

    return connection

