from src.main.api_helpers import get_random_comics
from src.main.db_helpers import insert_comics, get_from_db, parse_db_data, drop_table, create_table

if __name__ == "__main__":
    print("create table\n")
    create_table()
    print("get comics\n")
    data = get_random_comics(15)
    print("insert comics\n")
    insert_comics(data)
    print("get comics from db\n")
    data = get_from_db(10)
    print("parse comics\n")
    parse_db_data(data)
