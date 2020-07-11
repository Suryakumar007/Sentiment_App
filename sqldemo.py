import mysql.connector as mysql

print("Hai")

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "billy7bones",
    database = "demo"
)

cursor=db.cursor()
query="SELECT * FROM taula"

cursor.execute(query)

records=cursor.fetchall()

for record in records:
    print(record)

print(db)