# from database import Database
from database import create_connection
from model.customer import Customer
from model.user import User

def all_users():
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        results = cursor.fetchall()
        list_user = []
        for row in results:
            user = User(id=row[0], username=row[1], password=row[2], gender=row[3],fullname=row[4], contact=row[5], birth=row[6], address=row[7])
            list_user.append(user)
        return list_user
    
def check_customer(username, password):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM user WHERE username = '" + username + "' AND password = '" + password + "'"
        cursor.execute(sql)
        results = cursor.fetchone()
        if results:
            sql = "SELECT * FROM customer WHERE userId = '" + str(results[0]) + "'"
            cursor.execute(sql)
            result_2 = cursor.fetchone()
            if result_2:
                customer = Customer(id=result_2[0], userId=result_2[1])
                return customer
            return None
        return None

def existing_customer(username):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM user WHERE username = '" + username + "'"
        cursor.execute(sql)
        results = cursor.fetchone()
        if not results:
            return False
        user = User(id=results[0], username=results[1], password=results[2], gender=results[3],fullname=results[4], contact=results[5], birth=results[6], address=results[7])
        return user

def info_customer(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM customer WHERE id = '" + str(id) + "'"
        cursor.execute(sql)
        result_2 = cursor.fetchone()
        if result_2:
            sql = "SELECT * FROM user WHERE id = '" + str(result_2[1]) + "'"
            cursor.execute(sql)
            results = cursor.fetchone()
            user = User(id=results[0], username=results[1], password=results[2], gender=results[3],fullname=results[4], contact=results[5], birth=results[6], address=results[7])
            return user
        return None
    
def create_user(fullname, username, password, contact, address):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO user (fullname, username, password, contact, address) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (fullname, username, password, contact, address ))
        conn.commit()
    with conn.cursor() as cursor:
        user = existing_customer(username)
        sql = "INSERT INTO customer (userId) VALUES (%s)"
        cursor.execute(sql, (str(user.id),))
        conn.commit()
        