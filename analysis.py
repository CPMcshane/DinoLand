import sqlite3
import csv

conn = sqlite3.connect("dinosaur_information.db")
curr = conn.cursor()

createTableCommand = """ CREATE TABLE DINO_DATA (
    Dinosaurname VARCHAR(20),
    Diet VARCHAR(10),
    Territorrial VARCHAR(15),
    Land VARCHAR(10)
);"""

# curr.execute(createTableCommand)

with open("Dino Info.csv", 'r') as file:
    i = 0
    for item in file:
        if i > 0:
            info = item.split(",")
            addData = f"INSERT INTO DINO_DATA VALUES('{info[0]}','{info[1]}','{info[2]}','{info[3]}')"
            # curr.execute(addData)
        else:
            i += 1
            pass

# conn.commit()

fetchData = "SELECT * from DINO_DATA"
curr.execute(fetchData)

answer = curr.fetchall()
for data in answer:
    print(data)

