
import os
import logging
from psycopg2 import sql
from scripts.db_operations import connect_db, create_database, drop_database
from scripts.lib.tsv import select_tsv_files, get_columns, table_exists, create_table_sql

def load_tsv_to_postgres():

    try:

        create_database()
        conn, cursor = connect_db()

        files = select_tsv_files()

        print("Selected files:")
        logging.info("TSV files selected")

        for f in files:
            print(f)
            logging.info(f"File selected: {f}")

        for file_path in files:

            table_name = (
                os.path.basename(file_path)
                .replace(".tsv", "")
                .replace(".", "_")
                .replace(" ", "_")
            )

            logging.info(f"Processing file: {file_path}")

            try:

                # ---- CHECK TABLE EXISTENCE ----
                if table_exists(cursor, table_name):

                    print(f"Skipping {table_name} (already exists)")
                    logging.warning(f"Skipped load: table '{table_name}' already exists")

                    continue

                # ---- CREATE TABLE ----
                columns = get_columns(file_path)
                create_sql = create_table_sql(table_name, columns)

                cursor.execute(create_sql)

                logging.info(f"Table created: {table_name}")

                # ---- COPY DATA ----
                with open(file_path, "r", encoding="utf-8") as f:

                    cursor.copy_expert(
                        sql.SQL("""
                            COPY {} FROM STDIN
                            WITH (
                                FORMAT TEXT,
                                DELIMITER E'\\t',
                                HEADER TRUE,
                                NULL '\\N'
                            )
                        """).format(sql.Identifier(table_name)).as_string(conn),
                        f
                    )

                conn.commit()

                print(f"Loaded {table_name}")
                logging.info(f"Loaded table successfully: {table_name}")

            except Exception as table_error:

                conn.rollback()

                logging.error(
                    f"Error loading {table_name}: {table_error}"
                )

                print(f"Error loading {table_name}: {table_error}")

        cursor.close()
        conn.close()

        logging.info("TSV ingestion completed")

    except Exception as e:

        logging.critical(f"Fatal loader error: {e}")
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    load_tsv_to_postgres()