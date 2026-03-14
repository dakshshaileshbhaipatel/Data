# Function to connect to the database with user input and error handling

import psycopg2
import logging
import tkinter as tk
from tkinter import simpledialog, messagebox

# Configure logging
logging.basicConfig(
    filename="database_operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def connect_db():

    try:
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()

        # Dialogue box
        db_name = simpledialog.askstring(
            "Database Connection",
            "Enter database name you want to connect to:",
            initialvalue="TEST"
        )

        if not db_name:
            messagebox.showinfo("Cancelled", "Database connection cancelled.")
            logging.info("User cancelled database connection.")
            return
        
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="admin",
            port=5432
        )

        cursor = conn.cursor()

        logging.info("Database connection established")

        return conn, cursor

    except Exception as e:

        logging.error(f"Database connection failed: {e}")
        raise

if __name__ == "__main__":
    connect_db()