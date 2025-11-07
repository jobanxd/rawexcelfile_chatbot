import sqlite3
import pandas as pd
import os

def csv_to_sqlite(csv_file, db_file=None, table_name=None):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file '{csv_file}' not found.")

    if db_file is None:
        db_file = os.path.splitext(csv_file)[0] + ".db"

    if table_name is None:
        table_name = os.path.splitext(os.path.basename(csv_file))[0]

    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_file)

    df.to_sql(table_name, conn, if_exists="replace", index=False)

    sample = conn.execute(f"SELECT * FROM {table_name} LIMIT 5;").fetchall()
    for row in sample:
        print(row)

    conn.close()

if __name__ == "__main__":
    csv_to_sqlite("insurance_policies.csv")