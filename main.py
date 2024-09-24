from src.DBManager import DBManager
from src.config import conns
from src.interface import user_interaction

if __name__ == "__main__":
    params = conns()
    db = DBManager(**params)
    db.create_table()
    user_interaction()
