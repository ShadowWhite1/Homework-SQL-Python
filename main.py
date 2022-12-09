import psycopg2


def create_db(conn):
  with conn.cursor() as cur:
    # cur.execute("""
    #     DROP TABLE client;
    #     DROP TABLE email;
    #     DROP TABLE phone;
    #     """) 
    cur.execute("""
      CREATE TABLE IF NOT EXISTS client(
      id SERIAL PRIMARY KEY,
      name VARCHAR(40) NOT NULL,
      surname VARCHAR(40) NOT NULL
      );""")
    cur.execute("""
      CREATE TABLE IF NOT EXISTS email(
      id SERIAL PRIMARY KEY,
      email VARCHAR(40) NOT NULL,
      client_id INTEGER NOT NULL REFERENCES client(id)
      );""")
    cur.execute("""
      CREATE TABLE IF NOT EXISTS phone(
      id SERIAL PRIMARY KEY,
      number VARCHAR(40) NOT NULL,
      client_id INTEGER NOT NULL REFERENCES client(id)
      );""")
    conn.commit()

def add_client(conn,name,surname):
  with conn.cursor() as cur:
    cur.execute("""
    INSERT INTO client(name, surname) VALUES(%s, %s);
    """, (name,surname))
    conn.commit()

def add_email(conn,client_id,email):
  with conn.cursor() as cur:
    cur.execute("""
    INSERT INTO email(email, client_id) VALUES(%s, %s);
    """, (email,client_id))
    conn.commit()

def add_phone(conn,client_id, number):
  with conn.cursor() as cur:
    cur.execute("""
    INSERT INTO phone(number, client_id) VALUES(%s, %s);
    """, (number,client_id))
    conn.commit()

def change_client_name(conn,old_name,new_name,old_surname,new_surname):
  with conn.cursor() as cur:
    cur.execute("""
    SELECT id FROM client WHERE name=%s AND surname=%s;
    """, (old_name,old_surname))
    client_id = cur.fetchone()[0]
  if new_name != '0' and new_surname == '0':
    with conn.cursor() as cur:
      cur.execute("""
      UPDATE client SET name=%s WHERE id=%s;
      """, (new_name, client_id))
      cur.execute("""
      SELECT * FROM client;
      """)
      print(cur.fetchall())
      сonn.commit()
  elif new_name == '0' and new_surname != '0':
    with conn.cursor() as cur:
      cur.execute("""
      UPDATE client SET surname=%s WHERE id=%s;
      """, (new_surname, client_id))
      cur.execute("""
      SELECT * FROM client;
      """)
      print(cur.fetchall()) 
      conn.commit() 
  else:
    with conn.cursor() as cur:
      cur.execute("""
      UPDATE client SET name=%s WHERE id=%s;
      """, (new_name, client_id))
      cur.execute("""
      SELECT * FROM client;
      """)
      print(cur.fetchall())               
      cur.execute("""
      UPDATE client SET surname=%s WHERE id=%s;
      """, (new_surname, client_id))
      cur.execute("""
      SELECT * FROM client;
      """)
      print(cur.fetchall())
      conn.commit()

def change_client_number(conn,old_number, new_number):
  with conn.cursor() as cur:
    cur.execute("""
    SELECT id FROM phone WHERE number=%s;
    """, (old_number,))
    phone_id = cur.fetchone()[0]
    cur.execute("""
    UPDATE phone SET number=%s WHERE id=%s;
    """, (new_number, phone_id))
    cur.execute("""
    SELECT * FROM phone;
    """)
    print(cur.fetchall())
    conn.commit()

def change_client_email(conn,old_email, new_email):
  with conn.cursor() as cur:
    cur.execute("""
    SELECT id FROM email WHERE email=%s;
    """, (old_email,))
    email_id = cur.fetchone()[0]
    cur.execute("""
    UPDATE email SET email=%s WHERE id=%s;
    """, (new_email, email_id))
    cur.execute("""
    SELECT * FROM email;
    """)
    print(cur.fetchall())
    conn.commit()

def delete_number(conn,name,surname):
  with conn.cursor() as cur:
    cur.execute("""
    SELECT id FROM client WHERE name=%s AND surname=%s;
    """, (name,surname))
    client_id = cur.fetchone()[0]
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM phone;
    """)
    print(cur.fetchall())
    conn.commit() 

def delete_client_name(conn,name,surname):
  with conn.cursor() as cur:
    cur.execute("""
    SELECT id FROM client WHERE name=%s AND surname=%s;
    """, (name,surname))
    client_id = cur.fetchone()[0]
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM phone;
    """)
    print(cur.fetchall())
    cur.execute("""
    DELETE FROM email WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM email;
    """)
    print(cur.fetchall())
    cur.execute("""
    DELETE FROM client WHERE id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM client;
    """)
    print(cur.fetchall())
    conn.commit()
     
def find_client_inf(conn,name,surname,email,number):
  with conn.cursor() as cur:
    if email != '0':
      cur.execute("""
      SELECT client_id FROM email WHERE email=%s;
      """, (email,))
      client_id = cur.fetchone()[0]
      cur.execute("""
      SELECT number FROM phone WHERE client_id=%s;
      """, (client_id,))
      print(cur.fetchall())
      cur.execute("""
      SELECT name,surname FROM client WHERE id=%s;
      """, (client_id,))
      print(cur.fetchone())
      return
    elif number != '0':
      cur.execute("""
      SELECT client_id FROM phone WHERE number=%s;
      """, (number,))
      client_id = cur.fetchone()[0]
      cur.execute("""
      SELECT email FROM email WHERE client_id=%s;
      """, (client_id,))
      print(cur.fetchall())
      cur.execute("""
      SELECT number FROM phone WHERE client_id=%s;
      """, (client_id,))
      print(cur.fetchall())
      cur.execute("""
      SELECT name, surname FROM client WHERE id=%s;
      """, (client_id,))
      print(cur.fetchone())
      return
    else:
      cur.execute("""
      SELECT id FROM client WHERE name=%s AND surname=%s;
      """, (name,surname))
      client_id = cur.fetchone()[0]
      print(client_id)
      cur.execute("""
      SELECT email FROM email WHERE client_id=%s;
      """, (client_id,))
      print(cur.fetchall())
      cur.execute("""
      SELECT number FROM phone WHERE client_id=%s;
      """, (client_id,))
      print(cur.fetchall())                        


while True:
      conn = psycopg2.connect(database = 'netology_db', user = 'postgres', password = '')
      create_db(conn)
      print('Введите команду: A, A1, C, C1, D, F, Q, I - информация о командах ')
      command = input('Введите название команды: ')
      if command == 'A' or command == 'a':
        name = input('Введите имя клиента: ')
        surname = input('Введите фамилию клиента: ')
        add_client(conn,name,surname)
      elif command == 'A1' or command == 'a1':
        data = input('Телефон или email? T/E ')
        if data == 'T' or data == 't':
            client_id = input('Введите id клиента: ')
            number = input('Введите номер: ')
            add_phone(conn, client_id, number)
        elif data == 'E' or data == 'e':
            client_id = input('Введите id клиента: ')
            email = input('Введите email: ')
            add_email(conn, client_id, email)
      elif  command == 'C' or command == 'c':
        old_name = input('Старое имя? ')
        new_name = input('Новое имя?(Если нет - введите 0) ')
        old_surname = input('Старая фамилия? ')
        new_surname = input('Новая фамилия? (Если нет - введите 0) ')
        change_client_name(conn,old_name,new_name,old_surname,new_surname)
      elif command == 'C1' or command == 'c1':
        data = input('Телефон или email? T/E ')
        if data == 'T' or data == 't':
            old_number = input('Старый номер? ')
            new_number = input('Новый номер? ')
            change_client_number(conn,old_number, new_number)
        elif data == 'E' or data == 'e':
            old_email = input('Старый email? ')
            new_email= input('Новый email? ')
            change_client_email(conn,old_email, new_email)            
      elif command == 'D' or command == 'd':
        data = input('Удалить все данные или только телефон? A/T ')
        if data == 'A' or data == 'a':
            name = input('Введите имя: ')
            surname = input('Введите фамилию: ')
            delete_client_name(conn,name,surname)
        elif data == 'T' or data == 't':
            name = input('Введите имя: ')
            surname = input('Введите фамилию: ')
            delete_client_name(conn,name,surname)
      elif command == 'F' or command == 'f':
        number = input('Телефон? (Если нет - введите 0) ')
        email = input('Email? (Если нет - введите 0) ')
        name = input('Имя? (Если нет - введите 0) ')
        surname = input('Фамилия? (Если нет - введите 0) ')
        if number == '0' and email == '0' and name == '0' and surname == '0':
            print('Not found')
        else:
            find_client_inf(conn,name,surname,email,number)
        conn.close()
      elif command == 'I' or command == 'i':
        print("Введите команду:\nA - добавить клиента\nA1 - добавить телефон или email\nC - изменить данные клиента\nC1 - изменить телефон или email клиента\nD - удалить данные клиента\nF - найти данные\nQ - команда, котороя завершит работу. ")
      elif command == 'Q' or command == 'q':
        break
      else:
        print("Введите правильную команду или Q. ¯\_(ツ)_/¯")