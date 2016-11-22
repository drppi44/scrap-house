from db import get_connection, create_table, get_cursor
import sys


if __name__ == "__main__":
    connection = get_connection()
    cursor = get_cursor(connection)
    if 'create_table' in sys.argv:
        create_table(cursor)
    connection.close()
