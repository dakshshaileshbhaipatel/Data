# A dialogue to select TSV files

import tkinter as tk
from tkinter import filedialog
import csv

def select_tsv_files():
    root = tk.Tk()
    root.withdraw()  # hide main window

    file_paths = filedialog.askopenfilenames(
        title="Select TSV Files",
        filetypes=[("TSV files", "*.tsv")]
    )

    return list(file_paths)

# Function to read the first line of a TSV file and return column names

def get_columns(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
    return header

# Function to check if a table exists in the database

def table_exists(cursor, table_name):

    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
        )
        """,
        (table_name,)
    )

    return cursor.fetchone()[0]

# Function to generate a CREATE TABLE SQL statement based on column names

def create_table_sql(table_name, columns):

    column_defs = []

    for col in columns:
        col = (
            col.replace("-", "_")
               .replace(" ", "_")
               .replace(".", "_")
        )

        column_defs.append(f'"{col}" TEXT')

    columns_sql = ",\n".join(column_defs)

    return f"""
    CREATE TABLE IF NOT EXISTS "{table_name}" (
        {columns_sql}
    );
    """