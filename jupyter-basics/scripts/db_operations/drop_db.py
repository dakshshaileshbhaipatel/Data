# Function to drop an existing database with user input and error handling

import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import simpledialog, messagebox
import logging

# Use the same logging file used in the create_database function
logging.basicConfig(
    filename="database_operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def drop_database():

    try:
        root = tk.Tk()
        root.withdraw()

        # Ask user which database to drop
        db_name = simpledialog.askstring(
            "Drop Database",
            "Enter database name to drop:",
            initialvalue="TEST"
        )

        if not db_name:
            messagebox.showinfo("Cancelled", "Database drop cancelled.")
            logging.info("User cancelled database drop.")
            return

        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="admin",
            port=5432
        )

        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s;",
            (db_name,)
        )

        exists = cursor.fetchone()

        if not exists:
            messagebox.showwarning(
                "Database Not Found",
                f"Database '{db_name}' does not exist."
            )
            logging.warning(f"Attempted to drop non-existing database '{db_name}'.")
        else:

            # Terminate existing connections
            cursor.execute("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                AND pid <> pg_backend_pid();
            """, (db_name,))

            # Drop database safely
            cursor.execute(
                sql.SQL("DROP DATABASE {}").format(
                    sql.Identifier(db_name)
                )
            )

            messagebox.showinfo(
                "Success",
                f"Database '{db_name}' dropped successfully."
            )
            logging.info(f"Database '{db_name}' dropped successfully.")

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error dropping database: {e}")
        messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    drop_database()