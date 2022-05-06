import tkinter
from Randomizer import *
from GUI_database_functions import *


def data_window():
    """This function opens a new window containing the data from database and instruments to delete/add new entries
    """
    data_manupulation_window = tkinter.Toplevel()

    def delete_guest(window, pk):
        """This function deletes a guest entry and refreshes a window
        """
        delete_record_guest(pk)
        window.destroy()
        window.__init__()
        refresh(window)

    def add_guest(window, name):
        """This function takes a guest name and adds it to database while refreshing the window
        """
        new_entry_guests(name)
        window.destroy()
        window.__init__()
        refresh(window)

    def delete_prize(window, pk):
        """This function deletes a guest entry and refreshes a window
        """
        delete_record_prize(pk)
        window.destroy()
        window.__init__()
        refresh(window)

    def add_prize(window, name):
        """This function takes a guest name and adds it to database while refreshing the window
        """
        new_entry_prizes(name)
        window.destroy()
        window.__init__()
        refresh(window)

    def refresh(window):
        """This function refreshes the window after deleting/adding the query
        """
        guests = show_guests()
        prizes = show_prizes()
        # Show all the guests
        if guests:
            for number_g, guest in enumerate(guests):
                tkinter.Label(window, text=guest[0]).grid(row=number_g + 2, column=0)
                tkinter.Button(window, text='Delete',
                               command=lambda: delete_guest(window, guest[1])).grid(
                    row=number_g + 2, column=1
                )
        else:
            number_g = 0

        # Show all the prizes
        if prizes:
            for number_p, prize in enumerate(prizes):
                tkinter.Label(window, text=prize[0]).grid(row=number_p + 2, column=3)
                tkinter.Button(window, text='Delete',
                               command=lambda: delete_prize(window, prize[1])).grid(
                    row=number_p + 2, column=4
                )
        else:
            number_p = 0
        # Show data Labels

        tkinter.Label(data_manupulation_window, text='Guests').grid(row=0, column=0, rowspan=2)
        tkinter.Label(data_manupulation_window, text='Prizes').grid(row=0, column=3, rowspan=2)

        # Select the lowest row

        num_fin = max(number_g, number_p)

        # Enter and submit a new guest
        guest_entry = tkinter.Entry(data_manupulation_window, width=30)
        guest_entry.grid(row=num_fin + 3, column=0, padx=20, columnspan=2)
        tkinter.Button(data_manupulation_window, text='Submit',
                       command=lambda: add_guest(window, guest_entry.get())).grid(
            row=num_fin + 4, column=0, columnspan=2)

        # Enter and submit a new prize
        prize_entry = tkinter.Entry(data_manupulation_window, width=30)
        prize_entry.grid(row=num_fin + 3, column=3, padx=20, columnspan=2)
        tkinter.Button(data_manupulation_window, text='Submit',
                       command=lambda: add_prize(window, prize_entry.get())).grid(
            row=num_fin + 4, column=3, columnspan=2)

    refresh(data_manupulation_window)


def get_winner():

    global root
    # Get the list of guests
    guest_list = []
    guest_query = select_guests_who_did_non_win()
    for guest in guest_query:
        guest_list.append(guest)

    # Get the list of prizes
    prize_list = []
    prize_query = select_prizes_who_did_non_win()
    for prize in prize_query:
        prize_list.append(prize)

    # Determine and show a winner
    print(guest_list, prize_list)
    if guest_list and prize_list:
        winner = randomizer_main(guest_list, prize_list)
        try:
            new_entry_winners(winner)
            root.destroy()
            root.__init__()
            root.title('Prizes for Guests')
            root.geometry('600x400')

            tkinter.Button(text='Guest/Prize database', command=data_window).grid(row=0, column=0)
            tkinter.Button(text='Determine the winner!', command=get_winner).grid(row=0, column=5)
            tkinter.Button(text='Show winners', command=winners_window).grid(row=0, column=8)
            tkinter.Label(root, text=('The winner is ' + str(winner[0]) + '. He won the ' + str(winner[1]))).grid(row=4,
                                                                                                                  column=5)
        except sqlite3.IntegrityError:
            root.destroy()
            root.__init__()
            root.title('Prizes for Guests')
            root.geometry('600x400')

            tkinter.Button(text='Guest/Prize database', command=data_window).grid(row=0, column=0)
            tkinter.Button(text='Determine the winner!', command=get_winner).grid(row=0, column=5)
            tkinter.Button(text='Show winners', command=winners_window).grid(row=0, column=8)
            tkinter.Label(root, text=('Try again please!')).grid(row=10, column=5)
    else:
        root.destroy()
        root.__init__()
        root.title('Prizes for Guests')
        root.geometry('600x400')

        tkinter.Button(text='Guest/Prize database', command=data_window).grid(row=0, column=0)
        tkinter.Button(text='Determine the winner!', command=get_winner).grid(row=0, column=5)
        tkinter.Button(text='Show winners', command=winners_window).grid(row=0, column=8)
        tkinter.Label(text='').grid(row=5, columnspan=10)
        tkinter.Label(root, text='There is no prizes or guests left :(').grid(row=10, column=5)


def winners_window():
    winners_window = tkinter.Toplevel()

    def refresh(window):

        winners = show_winners()

        if winners:
            for number_w, winner in enumerate(winners):
                tkinter.Label(window, text=winner[0]).grid(row=number_w + 2, column=0)
                tkinter.Label(window, text=winner[1]).grid(row=number_w + 2, column=2)
            tkinter.Button(window, text='Delete all winners', command=winners_clear).grid(row=number_w + 3, column=0,
                                                                                          columnspan=3)
        else:
            tkinter.Label(window, text='There are no winners yet!').pack()

    refresh(winners_window)


# Create a window
root = tkinter.Tk()
root.title('Prizes for Guests')
root.geometry('600x400')

tkinter.Button(text='Guest/Prize database', command=data_window).grid(row=0, column=0)
tkinter.Button(text='Determine the winner!', command=get_winner).grid(row=0, column=5)
tkinter.Button(text='Show winners', command=winners_window).grid(row=0, column=10)
