import sqlite3


def create_member(member: tuple):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO MEMBER (
            slack_id, 
            member_id, 
            user_id,
            default_start_ts,
            default_end_ts)
            VALUES 
            (?, ?, ?, ?, ?)
        """, member)
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()


def select_member(slack_id: tuple):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

    cursor.execute('SELECT * FROM MEMBER WHERE slack_id = ?', slack_id)
    rows = cursor.fetchall()

    print(rows)
    conn.close()

    return rows[0] if len(rows) > 0 else None


def update_member():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
    conn.close()


def delete_member():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
    conn.close()
