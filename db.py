import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="scrap",
        passwd="scrap",
        db="scrap"
    )


def get_cursor(connection):
    return connection.cursor()


def create_table(cursor):
    cursor.execute(
        "CREATE TABLE idealista ("
        "id INT(11) PRIMARY KEY"
        ")"
    )
