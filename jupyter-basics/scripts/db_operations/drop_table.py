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

def drop_table():

    try:
        root = tk.Tk()
        root.withdraw()

        db_name = simpledialog.askstring(
            "Database Name",
            "Enter database name:",
            initialvalue="TEST"
        )

        if not db_name:
            messagebox.showinfo("Cancelled", "Table drop cancelled.")
            logging.info("User cancelled table drop.")
            return

        table_name = simpledialog.askstring(
            "Table Name",
            "Enter table name to drop:",
        )

        if not table_name:
            messagebox.showinfo("Cancelled", "Table drop cancelled.")
            logging.info("User cancelled table drop.")
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

        if not exists:

            messagebox.showwarning(
                "Table Not Found",
                f"Table '{table_name}' does not exist."
            )

            logging.warning(f"Attempted to drop non-existent table '{table_name}'.")

        else:

            cursor.execute(
                sql.SQL("DROP TABLE {}").format(
                    sql.Identifier(table_name)
                )
            )

            messagebox.showinfo(
                "Success",
                f"Table '{table_name}' dropped successfully."
            )

            logging.info(f"Table '{table_name}' dropped successfully.")

        cursor.close()
        conn.close()

    except Exception as e:

        logging.error(f"Error dropping table: {e}")

        messagebox.showerror(
            "Error",
            f"An error occurred:\n{e}"
        )

def drop_table_if_exists(conn, cursor, table_name):
    """
    Drops a table if it exists.

    Returns:
        True  -> table dropped
        False -> table did not exist
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

        if not exists:

            logging.warning(f"Table '{table_name}' does not exist.")
            return False

        cursor.execute(
            sql.SQL("DROP TABLE {}").format(
                sql.Identifier(table_name)
            )
        )

        conn.commit()

        logging.info(f"Table '{table_name}' dropped successfully.")

        return True

    except Exception as e:

        conn.rollback()
        logging.error(f"Error dropping table '{table_name}': {e}")
        raise

if __name__ == "__main__":
    drop_table()