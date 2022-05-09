import sqlite3


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
def create_database_or_connect(control):
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
        FOREIGN KEY(range_oid) REFERENCES ranges(range_oid) ON DELETE CASCADE
        )''')

    # Create prizes table
    control.execute('''CREATE TABLE IF NOT EXISTS prizes (
        prize_oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT,
        range_oid INTEGER NOT NULL,
        FOREIGN KEY(range_oid) REFERENCES ranges(range_oid) ON DELETE CASCADE
        )''')

    # Create winners table
    control.execute('''CREATE TABLE IF NOT EXISTS winners (
        guest_oid INTEGER NOT NULL,
        prize_oid INTEGER NOT NULL,
        UNIQUE (guest_oid, prize_oid) ON CONFLICT IGNORE,
        FOREIGN KEY(guest_oid) REFERENCES guests(guest_oid) ON DELETE CASCADE,
        FOREIGN KEY(prize_oid) REFERENCES prizes(prize_oid) ON DELETE CASCADE
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
def new_entry_guests(entry, rng, control):
    """This function makes a new database entry in guests table

    entry: str - the name of the guest
    rng: int - pk of the corresponding money range of the guest
    """
    control.execute("""INSERT INTO guests VALUES (:guest_oid, :name, :range_oid)""",
                    {'guest_oid': None, 'name': entry, 'range_oid': rng}
                    )


@database_decorator
def new_entry_prizes(entry, rng, control):
    """This function makes a new database entry in guests table

    entry: str - the name of the prize
    rng: int - pk of the corresponding money range of the guest
    """

    control.execute("""INSERT INTO prizes VALUES (:prize_oid, :name, :range_oid)""",
                    {'prize_oid': None, 'name': entry, 'range_oid': rng}
                    )


@database_decorator
def new_entry_winners(entry, control):
    """This function makes a new database entry in guests table

    entry: tuple -
    """

    pk_of_winner = entry[0][0]
    pk_of_prize = entry[1][0]

    control.execute("INSERT INTO winners VALUES (:guest_oid, :prize_oid)",
                    {
                        'guest_oid': pk_of_winner,
                        'prize_oid': pk_of_prize
                    }
                    )


@database_decorator
def show_ranges(control):
    """This function selects all ranges from a database and returns a list

    return: list of tuples: [(range_oid, money_range),]
    """

    control.execute("""SELECT * FROM ranges""")
    ranges = control.fetchall()
    return ranges


@database_decorator
def show_guests(range_oid, control):
    """This function selects all guests from a database and returns a list

    range_oid: int - pk of range

    return: list of tuples -  [(guest_oid, name),(...),]
    """

    control.execute("""SELECT * FROM guests WHERE range_oid=""" + str(range_oid))
    guests = control.fetchall()
    return guests


@database_decorator
def show_prizes(range_oid, control):
    """This function selects all prizes from a database and returns a list

    range_oid: int - pk of range

    return: list of tuples: [(guest_oid, name],(...),)
    """
    control.execute("""SELECT * FROM prizes WHERE range_oid=""" + str(range_oid))
    prizes = control.fetchall()
    return prizes


@database_decorator
def show_winners(control):
    """This function selects all winners from a database and returns a list

    return: list of tuples of winners: [(winner_name, winner_prize),(...),]
    """
    list_of_winners = []
    control.execute("""SELECT * FROM winners""")
    list_of_winners_id = control.fetchall()
    for winner in list_of_winners_id:
        control.execute("SELECT name FROM guests WHERE guest_oid=" + str(winner[0]))
        name = control.fetchall()
        control.execute("SELECT name FROM prizes WHERE prize_oid=" + str(winner[1]))
        prize = control.fetchall()
        list_of_winners.append((name, prize))
    return list_of_winners


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
def winners_clear(control):
    """This function deletes all winners entries
    """
    control.execute('DELETE FROM winners')


# Obsolete
@database_decorator
def select_guests_who_did_non_win(control):
    """This function selects guests who did not win

    return: list of all the guests who did not get the prize
    """
    loosers = []
    control.execute('SELECT guest_oid, name FROM guests')
    guest_list = control.fetchall()
    control.execute('SELECT guest_oid FROM winners')
    winners_list = control.fetchall()
    if winners_list:
        for guest in guest_list:
            for winner in winners_list:
                if guest[0] == winner[0]:
                    break
            else:
                loosers.append(guest)
    else:
        for guest in guest_list:
            loosers.append(guest)
    return loosers


@database_decorator
def select_prizes_who_did_non_win(control):
    """This function selects guests who did not win

    return: list of all the prizes which were not distributed
    """
    masterless_prizes = []
    control.execute('SELECT prize_oid, name FROM prizes')
    prize_list = control.fetchall()
    control.execute('SELECT prize_oid FROM winners')
    winners_list = control.fetchall()
    if winners_list:
        for prize in prize_list:
            for winner in winners_list:
                if prize[0] == winner[0]:
                    break
            else:
                masterless_prizes.append(prize)
    else:
        for prize in prize_list:
            masterless_prizes.append(prize)
    return masterless_prizes
