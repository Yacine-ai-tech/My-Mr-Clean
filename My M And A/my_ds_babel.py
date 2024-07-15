import sqlite3
import pandas as pd
from io import StringIO
import warnings
warnings.filterwarnings('ignore')
def sql_to_csv(database, table_name):
    conn = sqlite3.connect(database)
    query = f"SELECT * FROM {table_name}"
    results = pd.read_sql_query(query, conn)
    csv_path = "list_fault_lines.csv"
    results.to_csv(csv_path, index=False)
    with open(csv_path, 'r') as csv_file:
        csv_content = csv_file.read()
    return csv_content.strip()

def csv_to_sql(csv_content, database, table_name):
    if isinstance(csv_content, StringIO):
        csv_content = csv_content.getvalue()
    df = pd.read_csv(StringIO(csv_content))
    conn = sqlite3.connect(database)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
