import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import simpledialog, messagebox
import logging

logging.basicConfig(
    filename="database_operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_table():

    try:
        root = tk.Tk()
        root.withdraw()

        # Ask database name
        db_name = simpledialog.askstring(
            "Database Name",
            "Enter database name:",
            initialvalue="TEST"
        )

        if not db_name:
            messagebox.showinfo("Cancelled", "Table creation cancelled.")
            logging.info("User cancelled table creation.")
            return

        # Ask table name
        table_name = simpledialog.askstring(
            "Table Name",
            "Enter table name:",
            initialvalue="new_table"
        )

        if not table_name:
            messagebox.showinfo("Cancelled", "Table creation cancelled.")
            logging.info("User cancelled table creation.")
            return

        # Ask column definitions
        columns = simpledialog.askstring(
            "Columns",
            "Enter columns (example: id INT, name TEXT, age INT):",
            initialvalue="id INT, name TEXT"
        )

        if not columns:
            messagebox.showinfo("Cancelled", "Table creation cancelled.")
            logging.info("User cancelled table creation.")
            return

        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="admin",
            port=5432
        )

        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT current_database();")
        db_result = cursor.fetchone()
        if db_result is not None:
            print("Connected DB:", db_result[0])
        else:
            print("Connected DB: Unknown (no result)")

        # Check if table exists
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema='public'
                AND table_name=%s
            )
            """,
            (table_name,)
        )

        result = cursor.fetchone()
        exists = result[0] if result is not None else False

        if exists:

            messagebox.showwarning(
                "Table Exists",
                f"Table '{table_name}' already exists."
            )

            logging.warning(f"Table '{table_name}' already exists.")

        else:

            cursor.execute(
                sql.SQL("CREATE TABLE {} ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(columns)
                )
            )

            conn.commit()  # IMPORTANT

            messagebox.showinfo(
                "Success",
                f"Table '{table_name}' created successfully."
            )

            logging.info(f"Table '{table_name}' created successfully.")

        cursor.close()
        conn.close()

    except Exception as e:

        logging.error(f"Error creating table: {e}")

        messagebox.showerror(
            "Error",
            f"An error occurred:\n{e}"
        )

# Function to check if a table exists and create it if it doesn't
def ensure_table_exists(conn, cursor, table_name, columns):
    """
    Checks if a table exists. If not, creates it.

    Returns:
        True  -> table created
        False -> table already exists
    """

    try:

        cursor.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema='public'
                AND table_name=%s
            );
            """,
            (table_name,)
        )

        exists = cursor.fetchone()[0]

        if exists:
            logging.warning(f"Table '{table_name}' already exists. Skipping creation.")
            return False

        column_defs = []

        for col in columns:
            col = (
                col.replace("-", "_")
                   .replace(" ", "_")
                   .replace(".", "_")
            )

            column_defs.append(f'"{col}" TEXT')

        columns_sql = ",\n".join(column_defs)

        create_sql = sql.SQL(
            """
            CREATE TABLE {} (
                {}
            );
            """
        ).format(
            sql.Identifier(table_name),
            sql.SQL(columns_sql)
        )

        cursor.execute(create_sql)
        conn.commit()

        logging.info(f"Table '{table_name}' created successfully.")

        return True

    except Exception as e:

        conn.rollback()
        logging.error(f"Error creating table '{table_name}': {e}")
        raise

if __name__ == "__main__":
    create_table()