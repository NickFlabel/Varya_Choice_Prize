import tkinter
from Randomizer import *
from GUI_database_functions import *


def data_window():
    """This function opens a new window containing the data from database and instruments to delete/add new entries
    """

    def refresh(func):
        """This decorator refreshes the window after deleting/adding the query
        """

        def wrapper(*args, window, **kwargs):

            for widget in window.winfo_children():
                widget.destroy()

            func(*args, **kwargs)
            guests = show_guests()
            prizes = show_prizes()
            # Show all the guests
            if guests:
                for number_g, guest in enumerate(guests):
                    tkinter.Label(window, text=guest[0]).grid(row=number_g + 1, column=0)
                    tkinter.Button(window, text='Delete',
                                   command=lambda: delete_guest(guest[1], window=window)).grid(
                        row=number_g + 1, column=1
                    )
            else:
                number_g = 0

            # Show all the prizes
            if prizes:
                for number_p, prize in enumerate(prizes):
                    tkinter.Label(window, text=prize[0]).grid(row=number_p + 1, column=3)
                    tkinter.Button(window, text='Delete',
                                   command=lambda: delete_prize(prize[1], window=window)).grid(
                        row=number_p + 1, column=4
                    )
            else:
                number_p = 0
            # Show data Labels

            tkinter.Label(data_manipulation_window, text='Guests').grid(row=0, column=0, columnspan=2)
            tkinter.Label(data_manipulation_window, text='Prizes').grid(row=0, column=3, columnspan=2)

            # Select the lowest row

            num_fin = max(number_g, number_p)

            # Enter and submit a new guest
            guest_entry = tkinter.Entry(data_manipulation_window, width=30)
            guest_entry.grid(row=num_fin + 2, column=0, padx=20, columnspan=2)
            tkinter.Button(data_manipulation_window, text='Submit',
                           command=lambda: add_guest(guest_entry.get(), window=window)).grid(
                row=num_fin + 3, column=0, columnspan=2)

            # Enter and submit a new prize
            prize_entry = tkinter.Entry(data_manipulation_window, width=30)
            prize_entry.grid(row=num_fin + 2, column=3, padx=20, columnspan=2)
            tkinter.Button(data_manipulation_window, text='Submit',
                           command=lambda: add_prize(prize_entry.get(), window=window)).grid(
                row=num_fin + 3, column=3, columnspan=2)

        return wrapper

    @refresh
    def delete_guest(pk):
        """This function deletes a guest entry and refreshes a window
        """
        delete_record_guest(pk)

    @refresh
    def add_guest(name):
        """This function takes a guest name and adds it to database while refreshing the window
        """
        new_entry_guests(name)

    @refresh
    def delete_prize(pk):
        """This function deletes a guest entry and refreshes a window
        """
        delete_record_prize(pk)

    @refresh
    def add_prize(name):
        """This function takes a guest name and adds it to database while refreshing the window
        """
        new_entry_prizes(name)

    @refresh
    def new_window():
        """This function fills the new window
        """
        pass

    # Initialization of window
    data_manipulation_window = tkinter.Toplevel()
    new_window(window=data_manipulation_window)


# Main window containing the means to control the app

def winners_window():
    """This function opens a new window containing the list of winners and their prizes
    """

    def refresh(func):
        def wrapper(*args, window, **kwargs):
            for widget in window.winfo_children():
                widget.destroy()
            func(*args, **kwargs)
            winners = show_winners()
            if winners:
                for number_w, winner in enumerate(winners):
                    tkinter.Label(window, text=winner[0]).grid(row=number_w + 2, column=0)
                    tkinter.Label(window, text=winner[1]).grid(row=number_w + 2, column=2)
                tkinter.Button(window, text='Delete all winners', command=lambda: delete_winners(window=window)).grid(
                    row=number_w + 3,
                    column=0,
                    columnspan=3)
            else:
                tkinter.Label(window, text='There are no winners yet!').pack()

        return wrapper

    @refresh
    def delete_winners():
        """This function deletes all winners
        """
        winners_clear()

    @refresh
    def new_window():
        """This function fills the new window
        """
        pass

    # Initialize the winners window
    window_winners = tkinter.Toplevel()
    new_window(window=window_winners)


# Create a window


def refresh(func):
    """This decorator fills the main window
    """

    def wrapper(*args, window, **kwargs):
        for widget in window.winfo_children():
            widget.destroy()
        func(*args, window, **kwargs)
        tkinter.Button(text='Guest/Prize database', command=data_window).grid(row=0, column=0)
        tkinter.Button(text='Determine the winner!', command=lambda: get_winner(window=window)).grid(row=0, column=2)
        tkinter.Button(text='Show winners', command=winners_window).grid(row=0, column=3)

    return wrapper


@refresh
def get_winner(window):
    """This function determines the winner and adds him into the database
    """
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

    # Determine a winner
    if guest_list and prize_list:
        winner = randomizer_main(guest_list, prize_list)
        new_entry_winners(winner)
        # Show the winner
        tkinter.Label(window, text=('The winner is ' + str(winner[0][1]) + '. He won the ' + str(winner[1][1]))).grid(
            row=1,
            column=2)
    # Show alert message if there is no unique pairs of guests and prizes left
    else:
        tkinter.Label(window, text='There is no prizes or guests left :(').grid(row=1, column=2)


@refresh
def new_window(*args, **kwargs):
    """This function fills the main window
    """
    pass


root = tkinter.Tk()
root.title('Prizes for Guests')
root.geometry('600x400')
new_window(window=root)
