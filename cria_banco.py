import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

criar_tabela = "CREATE TABLE IF NOT EXISTS hoteis (id_user text PRIMARY KEY,\
 nome text)"

cursor.execute(criar_tabela)
cursor.execute(cria_hotel)

connection.commit()
connection.close()
