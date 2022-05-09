import tkinter
from Randomizer import *
from GUI_database_functions import *


class AddEntryWindow:
    """This class opens a new window containing forms to create new entries in database
    """

    def refresh_entry_window(func):
        """This decorator method refreshes the window
        """

        def wrapper(self, *args, option='Select what you would like to add', **kwargs):
            for widget in self.window.winfo_children():
                widget.destroy()

            result = func(self, *args, option=option, **kwargs)

            clicked = tkinter.StringVar()
            clicked.set(option)
            tkinter.OptionMenu(self.window, clicked, "Range", "Guest", "Prize",
                               command=lambda _: self.new_entry_field(option=clicked.get(), window=self.window)).grid(
                row=0,
                column=0,
                columnspan=3)

            return result

        return wrapper

    @refresh_entry_window
    def new_range(self, range_entry, *args, **kwargs):
        """This method creates a new range while refreshing the data window

        range_entry: str - the text description of a range
        """
        new_entry_ranges(range_entry)
        self.parent_window.refresh()

    @refresh_entry_window
    def new_guest(self, guest_entry, range_pk, *args, **kwargs):
        """This method creates a new guest entry while refreshing the data window

        guest_entry: str - the name of the guest
        range_pk: str - the pk of the corresponding range
        """
        new_entry_guests(guest_entry, range_pk)
        self.parent_window.refresh()

    @refresh_entry_window
    def new_prize(self, guest_entry, range_pk, *args, **kwargs):
        """This method creates a new guest entry while refreshing the data window

        prize_entry: str - the name of the prize
        range_pk: str - the pk of the corresponding range
        """
        new_entry_prizes(guest_entry, range_pk)
        self.parent_window.refresh()

    @refresh_entry_window
    def new_entry_field(self, *args, option, **kwargs):
        """This function shows fields for adding a new entry

        clicked: string - the option which user have chosen
        """

        def check(var, options, button):
            """This functions checks if the value from the menu corresponds to any range in the database

            var: tkinter.StringVar()
            options: list - a query list of ranges
            button: button object - a button which needs to be activated
            """
            global range_pk
            for opt in options:
                if var.get() == opt[1]:
                    button.config(state=tkinter.NORMAL)
                    range_pk = opt[0]

        def process_query(query):
            """This function processes a query making it a list for the tkinter.OptionMenu

            query: list
            """
            if query:
                menu_opts = []
                for opt in query:
                    menu_opts.append(opt[1])
            else:
                menu_opts = ['Create ranges first!']
            return menu_opts

        if option == 'Range':
            tkinter.Label(self.window, text='Enter the money range of the guest/prize').grid(row=2, column=0)
            range_entry = tkinter.Entry(self.window, width=30)
            range_entry.grid(row=3, column=0)
            tkinter.Button(self.window, text='Submit',
                           command=lambda: self.new_range(range_entry.get())).grid(
                row=4, column=0)

        elif option == 'Guest':
            tkinter.Label(self.window, text='Enter the name of the guest').grid(row=2, column=0)
            guest_entry = tkinter.Entry(self.window, width=30)
            guest_entry.grid(row=3, column=0)
            var = tkinter.StringVar()
            var.set('Choose a range for the guest')
            options = show_ranges()
            menu_opts = process_query(options)
            submit_button = tkinter.Button(self.window, text='Submit',
                                           command=lambda: self.new_guest(guest_entry.get(), range_pk),
                                           state=tkinter.DISABLED)
            tkinter.OptionMenu(self.window, var, *menu_opts, command=lambda _: check(var, options, submit_button)).grid(
                row=4, column=0)
            submit_button.grid(row=5, column=0)

        elif option == 'Prize':
            tkinter.Label(self.window, text='Enter the name of the prize').grid(row=2, column=0)
            prize_entry = tkinter.Entry(self.window, width=30)
            prize_entry.grid(row=3, column=0)
            var = tkinter.StringVar()
            var.set('Choose a range for the prize')
            options = show_ranges()
            menu_opts = process_query(options)
            submit_button = tkinter.Button(self.window, text='Submit',
                                           command=lambda: self.new_prize(prize_entry.get(), range_pk),
                                           state=tkinter.DISABLED)
            tkinter.OptionMenu(self.window, var, *menu_opts, command=lambda _: check(var, options, submit_button)).grid(
                row=4, column=0)
            submit_button.grid(row=5, column=0)

    @refresh_entry_window
    def refresh(self, *args, **kwargs):
        pass

    def __call__(self, parent_window):
        self.window = tkinter.Toplevel()
        self.refresh()
        self.parent_window = parent_window


class DataWindow:
    """This function opens a new window containing the data from database and instruments to delete/add new entries
    """

    def refresh_data_window(func):
        """This decorator refreshes the window after deleting/adding the query
        """

        def wrapper(self, *args, **kwargs):

            for widget in self.window.winfo_children():
                widget.destroy()

            func(self, *args, **kwargs)
            ranges = show_ranges()
            # Initialize the rows
            number_g = 0
            number_p = 0
            number_max = 0
            rng_row = 0
            # Show all the ranges
            if ranges:
                for number_r, rng in enumerate(ranges):
                    rng_row = rng_row + number_max + 1
                    tkinter.Label(self.window, text='Range ' + rng[1]).grid(row=rng_row, column=0, columnspan=4)
                    # Show all guests in the range in question
                    guests = show_guests(rng[0])
                    if guests:
                        for number_g, guest in enumerate(guests):
                            # Name of the guest
                            tkinter.Label(self.window, text=guest[1]).grid(row=rng_row + number_g + 1, column=0)
                            # Delete button
                            tkinter.Button(self.window, text='Delete',
                                           command=lambda: self.delete_guest(guest[0])).grid(
                                row=rng_row + number_g + 1, column=1
                            )
                    # Show all the prizes
                    prizes = show_prizes(rng[0])
                    if prizes:
                        for number_p, prize in enumerate(prizes):
                            # Name of the prize
                            tkinter.Label(self.window, text=prize[1]).grid(row=rng_row + number_p + 1, column=3)
                            # Delete button
                            tkinter.Button(self.window, text='Delete',
                                           command=lambda: self.delete_prize(prize[0])).grid(
                                row=rng_row + number_p + 1, column=4
                            )

                    # Make a new max row
                    number_max = max(rng_row + number_p, rng_row + number_g)

            # Show data Labels

            tkinter.Label(self.window, text='Guests').grid(row=0, column=0, columnspan=2)
            tkinter.Label(self.window, text='Prizes').grid(row=0, column=3, columnspan=2)
            tkinter.Button(self.window, text='Add New Entry', command=lambda: entry_window(self)).grid(row=0, column=5)

        return wrapper

    @refresh_data_window
    def delete_guest(self, pk, *args, **kwargs):
        """This function deletes a guest entry and refreshes a window
        """
        delete_record_guest(pk)

    @refresh_data_window
    def delete_prize(self, pk, *args, **kwargs):
        """This function deletes a guest entry and refreshes a window
        """
        delete_record_prize(pk)

    @refresh_data_window
    def refresh(self, *args, **kwargs):
        pass

    def __call__(self):
        self.window = tkinter.Toplevel()
        self.refresh()


# Main window containing the means to control the app

def winners_window():
    """This function opens a new window containing the list of winners and their prizes
    """

    def refresh_winners_window(func):
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

    @refresh_winners_window
    def delete_winners():
        """This function deletes all winners
        """
        winners_clear()

    @refresh_winners_window
    def new_window_data_window():
        """This function fills the new window
        """
        pass

    # Initialize the winners window
    window_winners = tkinter.Toplevel()
    new_window_data_window(window=window_winners)


# Create a window


def refresh_main_window(func):
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


@refresh_main_window
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


@refresh_main_window
def new_window(*args, **kwargs):
    """This function fills the main window
    """
    pass


entry_window = AddEntryWindow()
data_window = DataWindow()
root = tkinter.Tk()
root.title('Prizes for Guests')
root.geometry('600x400')
new_window(window=root)
