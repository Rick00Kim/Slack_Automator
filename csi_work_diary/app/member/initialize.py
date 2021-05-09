import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully!!")
cursor = conn.cursor()
cursor.execute(
    "SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'MEMBER' ")
if cursor.fetchone()[0] == 1:
    print("Member Table exists...")
else:
    print("Member Table not exists!!")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS MEMBER (
            slack_id TEXT NOT NULL PRIMARY KEY,
            member_id TEXT,
            user_id TEXT,
            default_start_ts TEXT,
            default_end_ts TEXT
        )
        """)

    print("Table created successfully!!")

conn.close()
