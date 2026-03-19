import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="Chaveneau",          
    password = "mysql",
    database="TP_SecuBDD_Menez_Chaveneau"
)
cursor = conn.cursor()
data = [
    ("Fluffy", "Harold", "chat", "f", "2013-02-04", None),
    ("Claws", "Gwen", "chat", "m", "2014-03-17", None),
    ("Buffy", "Harod", "chien", "f", "2019-05-13", None),
    ("Fang", "Benny", "chien", "m", "2010-08-27", None),
    ("Bowser", "Diane", "chien", "m", "2018-08-31", "2021-07-29"),
    ("Chirpy", "Gwen", "oiseau", "f", "2018-09-11", None),
    ("Whistler", "Gwen", "oiseau", None, "2017-12-09", None),
    ("Slim", "Benny", "serpent", "m", "2016-04-29", None),
    ("Puffball", "Diane", "hamster", "f", "2019-03-30", None)
]

query = """
INSERT INTO animaux (nom, proprietaire, espece, genre, naissance, mort) VALUES (%s, %s, %s, %s, %s, %s)
"""
cursor.executemany(query, data)
conn.commit()
print(f"{cursor.rowcount} lignes insérées.")
cursor.close()
conn.close()
