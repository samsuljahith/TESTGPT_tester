import sqlite3
import hashlib

def test_sqlite_data():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE rockets (id INTEGER, name TEXT, price INTEGER)")
    rows = [
        (1, "Falcon", 2999),
        (2, "Atlas", 1999),
        (3, "Delta", 3999)
    ]
    c.executemany("INSERT INTO rockets VALUES (?, ?, ?)", rows)
    conn.commit()
    c.execute("SELECT * FROM rockets")
    all_rows = c.fetchall()
    assert len(all_rows) == 3
    row_hashes = [hashlib.md5(str(row).encode()).hexdigest() for row in all_rows]
    assert len(set(row_hashes)) == 3
    conn.close()