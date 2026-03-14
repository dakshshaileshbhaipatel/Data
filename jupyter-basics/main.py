import logging
from scripts.lib import load_tsv_to_postgres

logging.basicConfig(
    filename="database_operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    load_tsv_to_postgres()