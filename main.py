import psycopg2
from psycopg2.sql import SQL, Identifier
# with psycopg2.connect(database="clients_db", user="postgres", password="14341434in") as conn:
#     with conn.cursor() as cur:
#          cur.execute("""
#          DROP TABLE phone;
#          DROP TABLE client;
#           """)
#     conn.commit()
def create_db(cur):
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



# Функция, создающая структуру БД (таблицы).
# Функция, позволяющая добавить нового клиента.
# Функция, позволяющая добавить телефон для существующего клиента.
# Функция, позволяющая изменить данные о клиенте.
# Функция, позволяющая удалить телефон для существующего клиента.
# Функция, позволяющая удалить существующего клиента.
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.



def add_client(cur, first_name, last_name, email):
      cur.execute("""
      INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING client_id;
      """, (first_name, last_name, email))
      pass
def add_phone(cur, client_id, phone):
      cur.execute("""
      INSERT INTO phone (client_id, phone) VALUES (%s, %s)
      ;
      """, (client_id, phone))
      pass

def change_client(cur, client_id, first_name = None, last_name = None, email = None, phone = None):

      arg_list_c = {'first_name': first_name, 'last_name': last_name, 'email': email}
      for key, arg in arg_list_c.items():
          if arg:
              cur.execute(SQL("UPDATE client SET {}=%s WHERE client_id=%s").format(Identifier(key)), (arg, client_id))
      arg_list_p = {'phone': phone}
      for key, arg in arg_list_p.items():
          if arg:
              cur.execute(SQL("UPDATE phone SET {}=%s WHERE client_id=%s").format(Identifier(key)), (arg, client_id))
      pass

def delete_phone(cur, phone):
       cur.execute("""
       DELETE FROM phone
       WHERE  phone = %s;
       """, (phone,))
       pass

def delete_client(cur, client_id):
      cur.execute("""
      DELETE FROM phone
      WHERE client_id = %s;
      """, (client_id,))
      cur.execute("""
      DELETE FROM client
      WHERE client_id = %s;
      """, (client_id,))
      pass

# def find_client_n(conn, first_name, last_name, email):
#    with conn.cursor() as cur:
#      cur.execute("""
#      SELECT client_id FROM client WHERE (first_name, last_name, email)= (%s,%s,%s);
#      """, (first_name, last_name, email))
#      print (cur.fetchone()[0])
#
#
def find_client_p(cur, phone):
    cur.execute("""
    SELECT client_id FROM phone WHERE phone= %s;
    """, (phone,))
    print(cur.fetchone()[0])

def find_client_n (cur, first_name=None, last_name=None, email=None):
    arg_list_c = {'first_name': first_name, 'last_name': last_name, 'email': email}
    cl = []
    for key, arg in arg_list_c.items():
        if arg:
            cur.execute(SQL("SELECT client_id FROM client WHERE {} = %s").format(Identifier(key)), (arg,))
            cl.append(cur.fetchall())
    print(cl)
    pass



if __name__ == '__main__':
 with psycopg2.connect(database="clients_db", user="postgres", password="14341434in") as conn:
   with conn.cursor() as cur:
     #create_db(cur)
     #add_client(cur, "Петр", "Сидоров", "pp@mail.com")
     #add_phone(cur,3, "89031234597")
     #change_client(cur, 3, phone = '89161234567')
     #delete_phone(cur, "89031234597")
     #delete_client(cur, 1)
     find_client_n(cur,  "Петр", "Сидоров","pp@mail.com")
     # find_client_p(cur, "89031234567")
     conn.commit()
 conn.close()