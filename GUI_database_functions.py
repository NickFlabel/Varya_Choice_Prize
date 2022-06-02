import sqlite3
from Randomizer import balance_prizes_to_guests, uid_matcher

def database_decorator(func):
    """This decorator opens, closes a connection to the database and commits the changes
    """

    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('data.db')
        control = conn.cursor()
        # Enable foreign keys
        control.execute('PRAGMA foreign_keys = ON;')
        # Execute SQL command
        result = func(*args, **kwargs, control=control)
        conn.commit()
        conn.close()
        return result

    return wrapper


@database_decorator
def create_database(control):
    """This function checks if database is present or not
    """
    # Create tables if they do not exist

    # Create money ranges table
    control.execute('''CREATE TABLE IF NOT EXISTS ranges (
        range_oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        money_range TEXT UNIQUE ON CONFLICT IGNORE
        )''')

    # Create guests table
    control.execute('''CREATE TABLE IF NOT EXISTS guests (
        guest_oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT,
        range_oid INTEGER NOT NULL,
        guest_uid TEXT UNIQUE ON CONFLICT IGNORE,
        won_prize_id INTEGER NULL,
        FOREIGN KEY(range_oid) REFERENCES ranges(range_oid) ON DELETE CASCADE,
        FOREIGN KEY(won_prize_id) REFERENCES prizes(prize_oid) ON DELETE SET NULL
        )''')
    # Create prizes table
    control.execute('''CREATE TABLE IF NOT EXISTS prizes (
        prize_oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT,
        range_oid INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        winning_text TEXT NOT NULL,
        FOREIGN KEY(range_oid) REFERENCES ranges(range_oid) ON DELETE CASCADE
        )''')


@database_decorator
def new_entry_ranges(entry, control):
    """This function makes a new database entry in ranges table

    entry: str
    """
    control.execute("""INSERT INTO ranges VALUES (:range_oid, :money_range)""",
                    {'range_oid': None, 'money_range': entry}
                    )


@database_decorator
def new_entry_guests(guest_name, guest_range, guest_uid, control):
    """This function makes a new database entry in guests table

    entry: str - the name of the guest
    rng: int - pk of the corresponding money range of the guest
    guest_uid: str - unique text allowing for the identification of the guest during the prize distribution
    """
    control.execute(
        """INSERT INTO guests (guest_oid, name, range_oid, guest_uid) VALUES (:guest_oid, :name, :range_oid, :guest_uid)""",
        {'guest_oid': None, 'name': guest_name, 'range_oid': guest_range, 'guest_uid': guest_uid}
    )


@database_decorator
def new_entry_prizes(prize_name, prize_range, prize_num, prize_text, control):
    """This function makes a new database entry in guests table

    entry: str - the name of the prize
    rng: int - pk of the corresponding money range of the guest
    quantity: int - the number of available prizes of that type
    winning_text: str - the text displayed when winning this prize
    """

    control.execute("""INSERT INTO prizes VALUES (:prize_oid, :name, :range_oid, :quantity, :winning_text)""",
                    {'prize_oid': None, 'name': prize_name, 'range_oid': prize_range,
                     'quantity': prize_num, 'winning_text': prize_text}
                    )


@database_decorator
def show_prize(prize_oid, control):
    """This function makes query and returns the corresponding prize data

    prize_oid: int - the pk of the prize in question

    return: tuple - (prize_oid, name, prize_range, quantity, text)
    """
    control.execute("SELECT * FROM prizes WHERE prize_oid=" + str(prize_oid))
    prize = control.fetchall()
    return prize


@database_decorator
def show_guest_by_uid(guest_uid, control):
    """This function makes query and returns the corresponding prize data

    guest_uid: str - unique text allowing for the identification of the guest during the prize distribution

    return: tuple - (guest_oid, name, guest_range, guest_uid, prize_oid)
    """
    control.execute("SELECT * FROM guests")
    guests = control.fetchall()
    guest = uid_matcher(guest_uid, guests)
    return guest


@database_decorator
def show_ranges(control):
    """This function selects all ranges from a database and returns a list

    return: list of tuples: [(range_oid, money_range),]
    """

    control.execute("""SELECT * FROM ranges""")
    ranges = control.fetchall()
    return ranges


@database_decorator
def show_guests_of_given_range(range_oid, control):
    """This function selects all guests from a database and returns a list

    range_oid: int - pk of range

    return: list of tuples -  [(guest_oid, name, guest_range, guest_uid, prize_oid),(...),]
    """

    control.execute("""SELECT * FROM guests WHERE range_oid=""" + str(range_oid))
    guests = control.fetchall()
    return guests


@database_decorator
def show_prizes_of_given_range(range_oid, control):
    """This function selects all prizes from a database and returns a list

    range_oid: int - pk of range

    return: list of tuples: [(prize_oid, name, prize_range, quantity, text),(...),)
    """
    control.execute("""SELECT * FROM prizes WHERE range_oid=""" + str(range_oid))
    prizes = control.fetchall()
    return prizes


@database_decorator
def show_all_guests(control):
    """This function selects all guests from a database and returns a list

    return: list of tuples -  [(guest_oid, name, guest_range, guest_uid, prize_oid),(...),]
    """
    control.execute('SELECT * FROM guests')
    guests = control.fetchall()
    return guests


@database_decorator
def show_all_prizes(control):
    """This function selects all guests from a database and returns a list

    return: list of tuples -  [(prize_oid, name, prize_range, quantity, text),(...),)
    """
    control.execute('SELECT * FROM prizes')
    prizes = control.fetchall()
    return prizes


@database_decorator
def delete_record_range(pk, control):
    """This function deletes a record from a ranges table

    pk: int - primary key of a table entry
    """
    control.execute("DELETE FROM ranges WHERE range_oid=" + str(pk))


@database_decorator
def delete_record_guest(pk, control):
    """This function deletes a record from a guests table

    pk: int - primary key of a table entry
    """
    control.execute("DELETE FROM guests WHERE guest_oid=" + str(pk))


@database_decorator
def delete_record_prize(pk, control):
    """This function deletes a record from a prizes table

    pk: int - primary key of a table entry
    """
    control.execute("DELETE FROM prizes WHERE prize_oid=" + str(pk))


@database_decorator
def is_guest_the_winner(pk, control):
    """This function checks if the guest is in winners list

    pk: int - guest_oid

    return: False in case if there is no prize, prize_oid in case is there is one
    """
    control.execute('SELECT won_prize_id FROM guests WHERE guest_oid=' + str(pk))
    winner = control.fetchall()
    if winner[0][0]:
        return winner[0][0]
    else:
        return False


@database_decorator
def update_prize_guest(guest_oid, prize_oid, control):
    """This function updates the guest entry adding a reference to the prize won

    guest_oid: int - the pk of the guest in question
    prize_oid: int - the pk of the prize won
    """
    control.execute("UPDATE guests SET won_prize_id="+str(prize_oid)+" WHERE guest_oid="+str(guest_oid))


@database_decorator
def update_prize_quantity(prize_oid, control, number='-1'):
    """This function updates the guest entry adding a reference to the prize won

    prize_oid: int - the pk of the prize won
    """
    prize = show_prize(prize_oid)
    if number == '-1':
        number = int(prize[0][3]) - 1
    control.execute("UPDATE prizes SET quantity="+str(number)+" WHERE prize_oid="+str(prize_oid))


@database_decorator
def clear_prizes_guests(control):
    """This function clears all prizes won entries in guests table
    """
    control.execute('UPDATE guests SET won_prize_id=NULL')


@database_decorator
def balance_numbers_of_guests_and_prizes(control):
    """This function proportionally balances the number of guests and prizes
    """
    ranges = show_ranges()
    for range_ in ranges:
        range_oid = range_[0]
        guests = show_guests_of_given_range(range_oid)
        prizes = show_prizes_of_given_range(range_oid)

        if prizes:
            num_of_guests = len(guests)

            new_list = balance_prizes_to_guests(prizes, num_of_guests)

            for i in range(len(prizes)):
                prize_oid = prizes[i][0]
                update_prize_quantity(prize_oid=prize_oid, number=new_list[i])