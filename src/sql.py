import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="test_account",
    password="test_account",
    database="testDB",
)

cur = db.cursor()


def query(operation, value=None):
    cur.execute(operation, value)
    result = cur.fetchall()
    db.commit()

    return result
