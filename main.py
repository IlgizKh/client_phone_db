import psycopg2
# with psycopg2.connect(database="clients_db", user="postgres", password="14341434in") as conn:
#  with conn.cursor() as cur:
#          cur.execute("""
#          DROP TABLE phone;
#          DROP TABLE client;
#          """)
def create_db(conn):

  with conn.cursor() as cur:
       cur.execute("""
       CREATE TABLE IF NOT EXISTS client(
                  client_id SERIAL PRIMARY KEY,
                  first_name VARCHAR(40),
                  last_name VARCHAR(60),
                  email VARCHAR(60)
       );
       """)
       cur.execute("""
       CREATE TABLE IF NOT EXISTS phone(
             phone_id SERIAL PRIMARY KEY,
             phone VARCHAR(15) UNIQUE,
             client_id INTEGER NOT NULL REFERENCES client(client_id)
         );
         """)
       conn.commit()


# Функция, создающая структуру БД (таблицы).
# Функция, позволяющая добавить нового клиента.
# Функция, позволяющая добавить телефон для существующего клиента.
# Функция, позволяющая изменить данные о клиенте.
# Функция, позволяющая удалить телефон для существующего клиента.
# Функция, позволяющая удалить существующего клиента.
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.



def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
      cur.execute("""
      INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING client_id;
      """, (first_name, last_name, email))
    conn.commit()
    pass
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
      cur.execute("""
      INSERT INTO phone (client_id, phone) VALUES (%s, %s)
      ;
      """, (client_id, phone))
    pass

def change_client(conn, client_id, first_name, last_name, email, phone):
    with conn.cursor() as cur:
      cur.execute("""
        UPDATE client
        SET (first_name, last_name, email) = (%s, %s, %s)
        WHERE client_id = %s
      ;
      """, (first_name, last_name, email, client_id))
      cur.execute("""
        UPDATE phone
        SET phone = %s
        WHERE client_id = %s
        ;
        """, (phone, client_id))
    pass

def delete_phone(conn, phone):
    with conn.cursor() as cur:
       cur.execute("""
       DELETE FROM phone
       WHERE  phone = %s;
       """, (phone,))
    pass

def delete_client(conn, client_id):
    with conn.cursor() as cur:
      cur.execute("""
      DELETE FROM client
      WHERE client_id = %s;
      """, (client_id,))
    pass

def find_client_n(conn, first_name, last_name, email):
   with conn.cursor() as cur:
     cur.execute("""
     SELECT client_id FROM client WHERE (first_name, last_name, email)= (%s,%s,%s);
     """, (first_name, last_name, email))
     print (cur.fetchone()[0])


def find_client_p(conn, phone):
  with conn.cursor() as cur:
    cur.execute("""
    SELECT client_id FROM phone WHERE phone= %s;
    """, (phone,))
    print (cur.fetchone()[0])


with psycopg2.connect(database="clients_db", user="postgres", password="") as conn:
     create_db(conn)
     add_client(conn, "Петр", "Петров", "pp@mail.com")
     add_phone(conn,2, "89031234597")
     change_client(conn, 2,  "Петр", "Сидоров", "ps@mail.com", "89037654321")
     delete_phone(conn, "89031234597")
     delete_client(conn, 23)
     find_client_n(conn,  "Петр", "Сидоров", "ps@mail.com")
     find_client_p(conn, "89031234567")
conn.close()
