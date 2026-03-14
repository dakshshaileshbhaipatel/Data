# Function to create a new database with user input and error handling

import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import simpledialog, messagebox
import logging

# Configure logging
logging.basicConfig(
    filename="database_operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_database():

    try:
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()

        # Dialogue box
        db_name = simpledialog.askstring(
            "Database Creation",
            "Enter database name you want to create:",
            initialvalue="TEST"
        )

        if not db_name:
            messagebox.showinfo("Cancelled", "Database creation cancelled.")
            logging.info("User cancelled database creation.")
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

        if exists:
            messagebox.showwarning(
                "Database Exists",
                f"Database '{db_name}' already exists."
            )
            logging.warning(f"Database '{db_name}' already exists.")
        else:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(db_name)
                )
            )
            messagebox.showinfo(
                "Success",
                f"Database '{db_name}' created successfully."
            )
            logging.info(f"Database '{db_name}' created successfully.")

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error creating database: {e}")
        messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    create_database()