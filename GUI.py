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
                    tkinter.Button(self.window, text='Delete',
                                   command=lambda range_button=rng: self.delete_range(range_button[0])).grid(
                        row=rng_row, column=5
                    )
                    # Show all guests in the range in question
                    guests = show_guests(rng[0])
                    if guests:
                        for number_g, guest in enumerate(guests):
                            # Name of the guest
                            tkinter.Label(self.window, text=guest[1]).grid(row=rng_row + number_g + 1, column=0)
                            # Delete button
                            tkinter.Button(self.window, text='Delete',
                                           command=lambda guest_button=guest: self.delete_guest(guest_button[0])).grid(
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
                                           command=lambda prize_button=prize: self.delete_prize(prize_button[0])).grid(
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
    def delete_range(self, ok, *args, **kwargs):
        """This function deletes a range entry and refreshes a window
        """
        delete_record_range(pk)



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


class WinnersWindow:
    """This class opens a new window containing the list of winners and their prizes
    """

    def refresh_winners_window(func):
        """This decorator method renews the winner window
        """

        def wrapper(self, *args, **kwargs):
            for widget in self.window.winfo_children():
                widget.destroy()
            func(self, *args, **kwargs)
            winners = show_winners()
            if winners:
                for number_w, winner in enumerate(winners):
                    tkinter.Label(self.window, text=winner[0]).grid(row=number_w + 2, column=0)
                    tkinter.Label(self.window, text=winner[1]).grid(row=number_w + 2, column=2)
                tkinter.Button(self.window, text='Delete all winners', command=lambda: self.delete_winners()).grid(
                    row=number_w + 3,
                    column=0,
                    columnspan=3)
            else:
                tkinter.Label(self.window, text='There are no winners yet!').pack()

        return wrapper

    @refresh_winners_window
    def delete_winners(self, *args, **kwargs):
        """This function deletes all winners
        """
        winners_clear()

    @refresh_winners_window
    def new_window_data_window(self, *args, **kwargs):
        """This function fills the new window
        """
        pass

    # Initialize the winners window
    def __call__(self):
        self.window = tkinter.Toplevel()
        self.new_window_data_window()


class RandomDrawingWindow:
    """This window shows all the guests eligible for prizes and lists them with the winning button
    """

    def refresh_random_drawing_window(func):
        def wrapper(self, *args, **kwargs):
            for widget in self.window.winfo_children():
                widget.destroy()

            func(self, *args, **kwargs)

            guests = show_all_guests()

            for number_g, guest in enumerate(guests):
                tkinter.Label(self.window, text=guest[1]).grid(row=number_g+1, column=0)
                draw_button = tkinter.Button(self.window)
                if is_guest_the_winner(guest[0]):
                    draw_button.config(text='This guest have already won his prize', state=tkinter.DISABLED)
                elif not is_there_prizes_for_guest(guest[0]):
                    draw_button.config(text='There are no prizes for this guest in his range. Create some first!', state=tkinter.DISABLED)
                else:
                    draw_button.config(text='Click the button to determine your prize!', command=lambda guest=guest: self.determine_winner(guest))
                draw_button.grid(row=number_g+1, column=1)

        return wrapper

    @refresh_random_drawing_window
    def determine_winner(self, guest):
        prize_list = is_there_prizes_for_guest(guest[0])
        prize_for_guest = randomizer_main(prize_list)
        new_winner = (guest[0], prize_for_guest[0])
        new_entry_winners(new_winner)
        cong_window = tkinter.Toplevel()
        tkinter.Label(cong_window, text=('Congratulations, '+guest[1]+' for you have won the great prize of '+prize_for_guest[1]+'!!!')).pack()

    @refresh_random_drawing_window
    def new_window_drawing_window(self, *args, **kwargs):
        pass

    def __call__(self):
        self.window = tkinter.Toplevel()
        self.new_window_drawing_window()


class MainWindow:
    """This is the main window
    """

    def refresh_main_window(func):
        """This decorator fills the main window
        """

        def wrapper(self, *args, **kwargs):
            for widget in self.window.winfo_children():
                widget.destroy()
            func(self, *args, **kwargs)
            tkinter.Button(text='Guest/Prize database', command=data_window).grid(row=0, column=0)
            tkinter.Button(text='Determine the winners!', command=random_drawing_window).grid(row=0, column=2)
            tkinter.Button(text='Show winners', command=winners_window).grid(row=0, column=3)

        return wrapper

    @refresh_main_window
    def new(self):
        pass

    def __call__(self):
        self.window = tkinter.Tk()
        self.window.title('Guests and Prizes')
        self.window.geometry('600x400')
        self.new()


random_drawing_window = RandomDrawingWindow()
winners_window = WinnersWindow()
entry_window = AddEntryWindow()
data_window = DataWindow()
main_window = MainWindow()
main_window()
