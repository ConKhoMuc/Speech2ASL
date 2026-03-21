from mysql.connector import Error
from TextToSign.Database.ConnectDB import connect_mysql

import pandas as pd

class ImportExcel:

    def __init__(self, conn):
        self.conn = conn

    def import_words(self, file_path):

        df = pd.read_excel(file_path)

        # chuẩn hóa header
        df.columns = df.columns.str.strip().str.lower()

        # xử lý ô trống
        df = df.fillna("")

        cursor = self.conn.cursor()

        sql = "INSERT INTO text2sign (word, video, image, source) VALUES (%s,%s,%s,%s)"

        data = [
            (row["word"], row["video"], row["image"], row["source"])
            for _, row in df.iterrows()
        ]

        cursor.executemany(sql, data)
        self.conn.commit()

        print(f"✅ Imported {len(data)} rows")



# CREATE
def create_word(conn, word, video, image):
    try:
        cursor = conn.cursor()
        sql:str = "INSERT INTO text2sign (word, video, image) VALUES (%s, %s, %s)"
        cursor.execute(sql, (word, video, image))
        conn.commit()
        print(f"✅ Added word: {word}")
    except Error as e:
        print("❌ Cannot add word:", e)

# READ
def read_words(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, word, video, image, source FROM text2sign")
        rows = cursor.fetchall()
        print("📋 Words list:")
        for row in rows:
            print(row)
    except Error as e:
        print("❌ Cannot read the list:", e)

# UPDATE
def update_word(conn, id, new_word, new_video, new_image):
    try:
        cursor = conn.cursor()
        sql = "UPDATE text2sign SET word = %s, video = %s, image = %s WHERE id = %s"
        cursor.execute(sql, (new_word, new_video, new_image, id))
        conn.commit()
        print(f"✅ Updated the ID {id}")
    except Error as e:
        print("❌ Cannot update:", e)

# DELETE
def delete_word(conn, id):
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM text2sign WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        print(f"✅ Deleted ID {id}")
    except Error as e:
        print("❌ Cannot delete:", e)

# CRUD
if __name__ == "__main__":
    conn = connect_mysql(
    host="localhost",      # IP server MySQL
    user="root",           # MySQL user
    password="123456@aB",  # Password
    database="text2sign"   # Database name
)
    if conn:
        #cursor = conn.cursor()
        # Use CRUD
        #create_word(conn, "house", "/wordtosign/video/wrong.mp4","/wordtosign/video/wrong.mp4")

        #read_words(conn)
       # update_user_email(conn, 1, "new_a@example.com")
       # read_users(conn)
       # delete_user(conn, 2)
       # read_users(conn)

        importer = ImportExcel(conn)

        importer.import_words(r"D:\Python\SpeechToSignAI\text2sign\Text2SignDB.xlsx")

        read_words(conn)

        # Close connection
        conn.close()
        print("🔒 Closed connection to MySQL.")