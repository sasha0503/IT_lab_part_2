import os
import pickle

from classes import Table, IntegerColumn, TextColumn, Database, Row
from custom_logger import logger


def load_db_from_file(name):
    pkl_path = f"databases/{name}.pkl"
    database = None
    if os.path.exists(pkl_path):
        logger.debug(f"database {name} found. Loading database")
        try:
            with open(pkl_path, 'rb') as f:
                database = pickle.load(f)
        except Exception as e:
            logger.error(f"Error loading database '{name}': {e}")
    if not os.path.exists(pkl_path):
        logger.debug(f"database '{name}' not found. Creating new database")
        database = Database(name)
        pickle.dump(database, open(pkl_path, 'wb'))
    if not database:
        raise ValueError(f"database '{name}' could not be loaded or created")
    return database


def save_db_to_file(db):
    pkl_path = f"databases/{db.name}.pkl"
    logger.debug(f"saving database '{db.name}' to {pkl_path}")
    pickle.dump(db, open(pkl_path, 'wb'))


def load_db_from_request(req):
    name = req.args.get('db_name')
    if not name:
        logger.debug("db_name not found in request. Using default db")
        name = "example_db"
    return load_db_from_file(name)


def create_example_db():
    db = Database("example_db")

    table = Table("ExampleTable")
    table.add_column(IntegerColumn("ID"))
    table.add_column(TextColumn("Name"))

    db.add_table(table)

    table.add_row(Row(table, [1, "Bob"]))
    table.add_row(Row(table, [2, "Alice"]))

    save_db_to_file(db)

    return table.to_json()


if __name__ == '__main__':
    create_example_db()
