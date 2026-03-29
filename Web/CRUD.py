from mysql.connector import Error

import pandas as pd

from Speech2ASL.Web.DBConnect import get_connection


class ImportExcel:
     def import_words(self):
        conn1 = get_connection()
        df = pd.read_excel(r"C:\Users\trungnh\PycharmProjects\Speech2ASL\text2sign\Text2SignDB.xlsx")

        # chuẩn hóa header
        df.columns = df.columns.str.strip().str.lower()

        # xử lý ô trống
        df = df.fillna("")

        cursor = conn1.cursor()

        sql = "INSERT INTO text2sign (word, nlpword,video, images, source) VALUES (%s,%s,%s,%s,%s)"

        data = [
            (row["word"], row["nlpword"], row["video"], row["image"], row["source"])
            for _, row in df.iterrows()
        ]

        cursor.executemany(sql, data)
        conn1.commit()

        print(f"✅ Imported {len(data)} rows")
        conn1.close()



"""
# CREATE
def create_word(word, video, images, source, dword):
    try:
        conn1 = connect_mysql()
        cursor = conn1.cursor()
        sql:str = "INSERT INTO text2sign (word, video, images, source, nlpword) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (word, dword, video, images, source))
        conn1.commit()
        print(f"✅ Added word: {word}")
        conn1.close()
    except Error as e:
        print("❌ Cannot add word:", e)
"""
# READ
def read_words():
    try:
        conn1 = get_connection()
        cursor = conn1.cursor()
        cursor.execute("SELECT id, word, video, images, source FROM text2sign")
        rows = cursor.fetchall()
        print("📋 Words list:")
        for row in rows:
            print(row)
        conn1.close()
    except Error as e:
        print("❌ Cannot read the list:", e)
"""
# UPDATE
def update_word(id, new_word, new_video, new_image):
    try:
        conn1 = connect_mysql()
        cursor = conn1.cursor()
        sql = "UPDATE text2sign SET word = %s, video = %s, images = %s WHERE id = %s"
        cursor.execute(sql, (new_word, new_video, new_image, id))
        conn1.commit()
        print(f"✅ Updated the ID {id}")
        conn1.close()
    except Error as e:
        print("❌ Cannot update:", e)

# DELETE
def delete_word(id):
    try:
        conn1 = connect_mysql()
        cursor = conn1.cursor()
        sql = "DELETE FROM text2sign WHERE id = %s"
        cursor.execute(sql, (id,))
        conn1.commit()
        print(f"✅ Deleted ID {id}")
        conn1.close()
    except Error as e:
        print("❌ Cannot delete:", e)
"""
# CRUD
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        importer = ImportExcel()
        importer.import_words()

        read_words()

        # Close connection
        conn.close()
        print("🔒 Closed connection to MySQL.")