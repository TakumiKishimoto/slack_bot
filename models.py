import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# 語句を格納するテーブルを作成
cursor.execute("""
    CREATE TABLE IF NOT EXISTS phrases (
        id INTEGER PRIMARY KEY,
        keyword TEXT,
        phrase TEXT
    )
""")
conn.commit()
conn.close()

