# This python script loads data from xlsx files into sqlite database.
import pandas as pd
import sqlite3
import openpyxl

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

def create_table(table_name, columns):
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({', '.join(columns)})")

def load_data_to_table(table_name, file_path):
    df = pd.read_excel(file_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def get_columns(data):
    columns = []
    for row in data:
        for key in row.keys():
            if key not in columns:
                columns.append(key)
    return columns

def read_excell_data(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    rows = []
    header = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        rows.append(dict(zip(header, row)))
    return rows

transaction_data = read_excell_data('transactions.xlsx')
vendor_data = read_excell_data('vendors.xlsx')

create_table('transactions_transaction', get_columns(transaction_data))
create_table('vendors_vendor', get_columns(vendor_data))

load_data_to_table('transactions_transaction', 'transactions.xlsx')
load_data_to_table('vendors_vendor', 'vendors.xlsx')

cur.close()
conn.close()