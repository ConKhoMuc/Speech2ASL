import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456@aB",
        database="text2sign",
        #cursorclass=pymysql.cursors.DictCursor
    )

