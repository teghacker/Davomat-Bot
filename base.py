from sqlite3 import *
import sqlite3

def Creat():
    try:
        connection = connect("teg.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE Users(
        id INTEGER PRIMARY KEY,
        U_id INTEGER,
        username TEXT NOT NULL,
        Course TEXT NOT NULL);''')

        cursor.execute('''CREATE TABLE students(
        S_id INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Course TEXT NOT NULL);''')

        cursor.execute('''CREATE TABLE Dovamat(
        id INTEGER PRIMARY KEY,
        S_id INTEGER,
        Name TEXT NOT NULL,
        Course TEXT NOT NULL,
        Qatnashganmi BOOLEAN NOT NULL DEFAULT 0,
        Date DATE NOT NULL DEFAULT CURRENT_DATE);''')

        connection.commit()
    except (Exception, Error) as eror:
        print("Xato: ", eror)
    finally:
        if connection:
            cursor.close()
            connection.close()

def ADD_Students(a,b):
    try:
        connection = connect("teg.db")
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO students(Name, Course)  VALUES(?,?)""",(a,b))
        connection.commit()
    except (Exception, Error) as eror:
        print("Xato: ", eror)
    finally:
        if connection:
            cursor.close()
            connection.close()


def ADD_User(a,b,c):
    try:
        connection = connect("teg.db")
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO Users(U_id, username, Course)  VALUES(?,?,?)""",(a,b,c))

        connection.commit()
    except (Exception, Error) as eror:
        print("Xato: ", eror)
    finally:
        if connection:
            cursor.close()
            connection.close()



def R_User():
    try:
        connection = connect("teg.db")
        cursor = connection.cursor()
        cursor.execute(f"select * from Users")
        a = cursor.fetchall()
        return a
    except (Exception, Error) as eror:
        print("Xato: ", eror)
    finally:
        if connection:
            cursor.close()
            connection.close()


def R_Students():
    try:
        connection = connect("teg.db")
        cursor = connection.cursor()
        cursor.execute(f"select * from students")
        a = cursor.fetchall()
        return a
    except (Exception, Error) as eror:
        print("Xato: ", eror)
    finally:
        if connection:
            cursor.close()
            connection.close()

# def R_Davomat(guruh):
#     try:
#         connection = connect("teg.db")
#         cursor = connection.cursor()
#         cursor.execute(f"select * from ")
#         a = cursor.fetchall()
#         return a
#     except (Exception, Error) as eror:
#         print("Xato: ", eror)
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

def R_Davomat():
    try:
        connection = connect("teg.db")
        cursor = connection.cursor()
        cursor.execute(f"select * from Dovamat")
        a = cursor.fetchall()
        return a
    except (Exception, Error) as eror:
        print("Xato: ", eror)
    finally:
        if connection:
            cursor.close()
            connection.close()


def Delete_User(row_id):
    try:
        connection = sqlite3.connect("teg.db")
        cursor = connection.cursor()
        query = "DELETE FROM Users WHERE id = ?"
        cursor.execute(query, (row_id,))
        connection.commit()
    except (Exception, sqlite3.Error) as error:
        print("Xato: ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def Delete_Student(row_id):
    try:
        connection = sqlite3.connect("teg.db")
        cursor = connection.cursor()
        query = "DELETE FROM students WHERE S_id = ?"
        cursor.execute(query, (row_id,))
        connection.commit()
    except (Exception, sqlite3.Error) as error:
        print("Xato: ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()



def add_to_dovamat(S_id, name, a, qatnashganmi=0):
    try:
        connection = sqlite3.connect("teg.db")
        cursor = connection.cursor()
        query = '''INSERT INTO Dovamat (S_id, Name, Course, Qatnashganmi) VALUES (?, ?, ?, ?)'''
        cursor.execute(query, (S_id,name, a, qatnashganmi))
        connection.commit()
    except (Exception, sqlite3.Error) as error:
        print("Xato: ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()



def Delete_Davomat(row_id):
    try:
        connection = sqlite3.connect("teg.db")
        cursor = connection.cursor()
        query = "DELETE FROM Dovamat WHERE S_id = ?"
        cursor.execute(query, (row_id,))
        connection.commit()
    except (Exception, sqlite3.Error) as error:
        print("Xato: ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

Creat()