import tkinter
import tkinter.font
from Randomizer import *
from PIL import Image, ImageTk
from GUI_database_functions import *
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


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
            menu = tkinter.OptionMenu(self.window, clicked, "Range", "Prize",
                               command=lambda _: self.new_entry_field(option=clicked.get(), window=self.window))
            menu.grid(
                row=0,
                column=0,
                columnspan=3)
            menu.config(bg="#5B97D3", borderwidth=0, activebackground="#4A7BAD")

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
    def new_entry_field(self, *args, **kwargs):
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

        if kwargs['option'] == 'Range':
            customtkinter.CTkLabel(self.window, text='Enter the money range of the guest/prize').grid(row=2, column=0)
            range_entry = customtkinter.CTkEntry(self.window, width=200)
            range_entry.grid(row=3, column=0)
            customtkinter.CTkButton(self.window, text='Submit',
                           command=lambda: self.new_range(range_entry.get())).grid(
                row=4, column=0)

        elif kwargs['option'] == 'Prize':
            customtkinter.CTkLabel(self.window, text='Enter the name of the prize').grid(row=2, column=0)
            prize_entry = customtkinter.CTkEntry(self.window, width=200)
            prize_entry.grid(row=3, column=0)
            var = tkinter.StringVar()
            var.set('Choose a range for the prize')
            options = show_ranges()
            menu_opts = process_query(options)
            submit_button = customtkinter.CTkButton(self.window, text='Submit',
                                           command=lambda: self.new_prize(prize_entry.get(), range_pk),
                                           state=tkinter.DISABLED)
            menu = tkinter.OptionMenu(self.window, var, *menu_opts, command=lambda _: check(var, options, submit_button))
            menu.grid(
                row=4, column=0)
            submit_button.grid(row=5, column=0)
            menu.config(bg="#5B97D3", borderwidth=0, activebackground="#4A7BAD")

    @refresh_entry_window
    def refresh(self, *args, **kwargs):
        pass

    def __call__(self, parent_window):
        self.window = customtkinter.CTkToplevel()
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
                    customtkinter.CTkLabel(self.window, text='Range ' + rng[1]).grid(row=rng_row, column=0, columnspan=2)
                    customtkinter.CTkButton(self.window, text='Delete Range',
                                   command=lambda range_button=rng: self.delete_range(range_button[0])).grid(
                        row=rng_row, column=3
                    )
                    # Show all the prizes
                    prizes = show_prizes(rng[0])
                    if prizes:
                        for number_p, prize in enumerate(prizes):
                            # Name of the prize
                            customtkinter.CTkLabel(self.window, text=prize[1]).grid(row=rng_row + number_p + 1, column=0)
                            # Delete button
                            customtkinter.CTkButton(self.window, text='Delete Prize',
                                           command=lambda prize_button=prize: self.delete_prize(prize_button[0])).grid(
                                row=rng_row + number_p + 1, column=1
                            )


                    # Make a new max row
                    number_max = max(rng_row + number_p, rng_row + number_g)

            # Show data Labels

            customtkinter.CTkLabel(self.window, text='Prizes and Ranges').grid(row=0, column=0, columnspan=2)
            customtkinter.CTkButton(self.window, text='Add New Entry', command=lambda: entry_window(self)).grid(row=0, column=3)

        return wrapper

    @refresh_data_window
    def delete_range(self, pk, *args, **kwargs):
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
        self.window = customtkinter.CTkToplevel()
        self.refresh()
        self.window.geometry('400x400')


class RandomDrawingWindow:
    """This window shows all the guests eligible for prizes and lists them with the winning button
    """

    def refresh_random_drawing_window(func):
        def wrapper(self, *args, option='Select your range!', **kwargs):
            for widget in self.window.winfo_children():
                widget.destroy()

            func(self, *args, **kwargs)

            clicked = tkinter.StringVar()
            helv36 = tkinter.font.Font(family='Helvetica', size=14, weight='bold')
            clicked.set(option)
            ranges = show_ranges()
            range_list = [r[1] for r in ranges]
            menu = tkinter.OptionMenu(self.window, clicked, *range_list, command=lambda r=clicked.get(): self.new_window_drawing_window(option=r))
            menu.place(relx=1.0, rely=0.0, x=-600, y=20)
            menu.config(width=50, height=2, font=helv36, bg="#5B97D3", borderwidth=0, activebackground="#4A7BAD")
            img = tkinter.PhotoImage(file='ASD.png')
            self.img = img.subsample(3, 3)
            winner_button = customtkinter.CTkButton(self.window, image=self.img, compound='top', height=450, width=600, text='Determine your prize!', command=lambda r=clicked.get(): self.determine_winner(r))
            winner_button.place(rely=0.5, relx=0.5, anchor='center')

            if option == 'Select your range!':
                winner_button.config(state=tkinter.DISABLED)

        return wrapper

    @refresh_random_drawing_window
    def determine_winner(self, r):
        def determine_pk(r):
            range_list = show_ranges()
            for range in range_list:
                if r == range[1]:
                    return range[0]

        pk = determine_pk(r)
        prize_list = show_prizes(pk)
        prize = choice(prize_list)
        win_wnd = customtkinter.CTkToplevel()
        win_wnd.geometry('400x400')
        customtkinter.CTkLabel(win_wnd, text=('You have won '+prize[1])).place(anchor='center', rely=0.5, relx=0.5, width=400, height=50)

    @refresh_random_drawing_window
    def new_window_drawing_window(self, *args, **kwargs):
        pass

    def __call__(self):
        self.window = customtkinter.CTkToplevel()
        self.new_window_drawing_window()
        self.window.geometry('1600x1200')


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
            customtkinter.CTkButton(text='Guest/Prize database', command=data_window, width=200, height=50).place(anchor='nw', x=10, y=10)
            customtkinter.CTkButton(text='Determine the winners!', command=random_drawing_window, width=200, height=50).place(anchor='center', rely=0.5, relx=0.5)

        return wrapper

    @refresh_main_window
    def new(self):
        pass

    def __call__(self):
        self.window = customtkinter.CTk()
        self.window.title('Guests and Prizes')
        self.window.geometry('600x400')
        self.new()


random_drawing_window = RandomDrawingWindow()
entry_window = AddEntryWindow()
data_window = DataWindow()
main_window = MainWindow()
main_window()
