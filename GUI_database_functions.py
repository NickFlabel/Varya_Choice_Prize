import sqlite3
import tkinter
from Randomizer import *


# Create a database

def create_database_or_connect():
    '''This function checks if database is present or not
    '''
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    try:
        control.execute('''SELECT * FROM guests''')
    except sqlite3.OperationalError:
        control.execute('''CREATE TABLE guests (
        name text
        )''')
    try:
        control.execute('''SELECT * FROM prizes''')
    except sqlite3.OperationalError:
        control.execute('''CREATE TABLE prizes (
        name text
        )''')
    try:
        control.execute('''SELECT * FROM winners''')
    except sqlite3.OperationalError:
        control.execute('''CREATE TABLE winners (
        guest_id INTEGER NOT NULL REFERENCES guests(id),
        prize_id INTEGER NOT NULL REFERENCES prize(id),
        UNIQUE (guest_id, prize_id) ON CONFLICT ABORT
        )''')
    conn.commit()
    conn.close()


def new_entry_guests(entry):
    """This function makes a new database entry in guests table

    entry: str
    """
    conn = sqlite3.connect('data.db')

    control = conn.cursor()

    control.execute("""INSERT INTO guests VALUES (:name)""",
                    {'name': entry}
                    )
    conn.commit()
    conn.close()


def new_entry_prizes(entry):
    """This function makes a new database entry in guests table

    entry: str
    """
    conn = sqlite3.connect('data.db')

    control = conn.cursor()

    control.execute("""INSERT INTO prizes VALUES (:name)""",
                    {'name': entry}
                    )
    conn.commit()
    conn.close()


def new_entry_winners(entry):
    """This function makes a new database entry in guests table

    entry: tuple
    """
    conn = sqlite3.connect('data.db')

    control = conn.cursor()

    name_of_winner = "'" + str(entry[0]) + "'"
    name_of_prize = "'" + str(entry[1]) + "'"

    guest_id_query = control.execute("SELECT oid FROM guests WHERE name = " + name_of_winner)
    guest_id = guest_id_query.fetchall()

    prize_id_query = control.execute("SELECT oid FROM prizes WHERE name = " + name_of_prize)
    prize_id = prize_id_query.fetchall()

    control.execute("""INSERT INTO winners VALUES (:guest_id, :prize_id)""",
                    {
                        'guest_id': int(guest_id[0][0]),
                        'prize_id': int(prize_id[0][0])
                    }
                    )
    conn.commit()
    conn.close()


def show_guests():
    """This function selects all guests from a database and returns a list
    """
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute("""SELECT name, oid FROM guests""")
    guests = control.fetchall()
    conn.commit()
    conn.close()
    return guests


def show_prizes():
    """This function selects all prizes from a database and returns a list
    """
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute("""SELECT name, oid FROM prizes""")
    prizes = control.fetchall()
    conn.commit()
    conn.close()
    return prizes


def show_winners():
    """This function selects all winners from a database and returns a list
    """
    list_of_winners = []
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute("""SELECT * FROM winners""")
    list_of_winners_id = control.fetchall()
    for winner in list_of_winners_id:
        control.execute("SELECT name FROM guests WHERE oid=" + str(winner[0]))
        name = control.fetchall()
        control.execute("SELECT name FROM prizes WHERE oid=" + str(winner[1]))
        prize = control.fetchall()
        list_of_winners.append((name, prize))
    return list_of_winners


def delete_record_guest(pk):
    """This function deletes a record from a guests table

    pk: int - primary key of a table enrty
    """
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute("DELETE FROM guests WHERE oid=" + str(pk))
    conn.commit()
    conn.close()


def delete_record_prize(pk):
    """This function deletes a record from a prizes table

    pk: int - primary key of a table entry
    """
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute("DELETE FROM prizes WHERE oid=" + str(pk))
    conn.commit()
    conn.close()


def winners_clear():
    """This function deletes all winners entries
    """
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute('DELETE FROM winners')
    conn.commit()
    conn.close()


def select_guests_who_did_non_win():
    """This function selects guests who did not win
    """
    loosers = []
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute('SELECT oid, name FROM guests')
    guest_list = control.fetchall()
    control.execute('SELECT guest_id FROM winners')
    winners_list = control.fetchall()
    print(winners_list)
    print(guest_list)
    if winners_list:
        for guest in guest_list:
            for winner in winners_list:
                if guest[0] == winner[0]:
                    break
            else:
                loosers.append(guest[1])
    else:
        for guest in guest_list:
            loosers.append(guest[1])
    return loosers


def select_prizes_who_did_non_win():
    """This function selects guests who did not win
    """
    masterless_prizes = []
    conn = sqlite3.connect('data.db')
    control = conn.cursor()
    control.execute('SELECT oid, name FROM prizes')
    prize_list = control.fetchall()
    control.execute('SELECT prize_id FROM winners')
    winners_list = control.fetchall()
    if winners_list:
        for prize in prize_list:
            for winner in winners_list:
                if prize[0] == winner[0]:
                    break
            else:
                masterless_prizes.append(prize[1])
    else:
        for prize in prize_list:
            masterless_prizes.append(prize[1])
    print(masterless_prizes)
    return masterless_prizes
