import sqlite3
import pandas as pd

DB_FILE = 'cemetery.db'
CSV_FILE = 'cemetery_data.csv'

def import_csv_to_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    df = pd.read_csv(CSV_FILE)

    for _, row in df.iterrows():
        cursor.execute("INSERT INTO cemetery VALUES (?,?,?,?,?,?,?,?)", (
            row['Name'], row['DOB'], row['DOD'], row['STONE'],
            row['SECTION'], row['LOT'], row['NOTES'], row['DIRECTION']
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_csv_to_db()
    print("✅ CSV data successfully imported into the SQLite database.")
