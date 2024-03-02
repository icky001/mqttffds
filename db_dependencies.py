import pymysql

connection = pymysql.connect(
    host='192.168.1.1',
    user='root',
    password='',
    db='fire_eye',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def getCursor():
    return connection.cursor()

def commit():
    connection.commit()
