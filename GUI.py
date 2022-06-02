import tkinter
import tkinter.font
from Randomizer import *
from tkinter import ttk
from GUI_database_functions import *
import customtkinter
import time

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")


class AddEntryWindow:
    """This class opens a new window containing forms to create new entries in database
    """

    def refresh_entry_window(func):
        """This decorator method refreshes the window
        """

        def wrapper(self, *args, option='Выберите, что вы хотите добавить', **kwargs):
            # Destroy all widgets
            for widget in self.window.winfo_children():
                widget.destroy()

            # perform a function
            result = func(self, *args, option=option, **kwargs)

            # optionMenu to choose what to create
            clicked = tkinter.StringVar()
            clicked.set(option)
            menu = tkinter.OptionMenu(self.window, clicked, "Диапазон", "Приз", "Гость",
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
    def new_guest(self, *args, **kwargs):
        """This method creates a new guest entry while refreshing the data window

        guest_name: str - the name of the guest
        guest_range: str - the pk of the corresponding range
        guest_uid: str - unique text for the guest to enter during the distribution of prizes
        """
        guest_name = kwargs['guest_name']
        guest_range = kwargs['guest_range']
        guest_uid = kwargs['guest_uid']
        new_entry_guests(guest_name=guest_name, guest_range=guest_range, guest_uid=guest_uid)
        self.parent_window.refresh()

    @refresh_entry_window
    def new_prize(self, *args, **kwargs):
        """This method creates a new prize entry while refreshing the data window

        prize_name: str - the name of the prize
        prize_range: str - the pk of the corresponding range
        prize_num: int - the number of available prizes
        prize_text: srt - the text shown when guest wins this prize
        """
        prize_name = kwargs['prize_name']
        prize_range = kwargs['prize_range']
        prize_num = kwargs['prize_num']
        prize_text = kwargs['prize_text']
        try:
            int(prize_num)
            new_entry_prizes(prize_name=prize_name, prize_range=prize_range, prize_num=prize_num, prize_text=prize_text)
            self.parent_window.refresh()
        except ValueError:
            customtkinter.CTkLabel(self.window, text='Приз не был сохранен. '
                                                     'Введите число в поле, предназначенное для количества призов').grid(
                row=100, column=0
            )

    @refresh_entry_window
    def new_entry_field(self, *args, **kwargs):
        """This function shows fields for adding a new entry

        clicked: string - the option which user have chosen
        """

        def check_for_activating_submit_button(var, options, button):
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

        def process_query_ranges(query):
            """This function processes a query making it a list for the tkinter.OptionMenu

            query: list
            """
            if query:
                menu_opts = []
                for opt in query:
                    menu_opts.append(opt[1])
            else:
                menu_opts = ['Сначала необходимо создать диапазон']
            return menu_opts

        # Check the picked option
        if kwargs['option'] == 'Диапазон':
            # Build the form for creating a new range
            customtkinter.CTkLabel(self.window, text='Введите диапазон в рублях (00-00)').grid(row=2, column=0)
            # Range text
            range_entry = customtkinter.CTkEntry(self.window, width=200)
            range_entry.grid(row=3, column=0)
            # Submit button
            customtkinter.CTkButton(self.window, text='Готово',
                                    command=lambda: self.new_range(range_entry.get())).grid(
                row=4, column=0)

        elif kwargs['option'] == 'Приз':
            # Build the form for creating a new prize
            customtkinter.CTkLabel(self.window, text='Введите название приза').grid(row=2, column=0)
            # The name of the prize
            prize_entry = customtkinter.CTkEntry(self.window, width=200)
            prize_entry.grid(row=3, column=0)
            var = tkinter.StringVar()
            var.set('Выберите диапазон для данного приза')
            options = show_ranges()
            # Query the range options or state that there are no ranges
            menu_opts = process_query_ranges(options)

            # The ranges options
            menu = tkinter.OptionMenu(self.window, var, *menu_opts,
                                      command=lambda _: check_for_activating_submit_button(
                                        var, options, submit_button)) # This lambda configs the state of submit button
            menu.grid(
                row=4, column=0)

            # The number of available prizes
            customtkinter.CTkLabel(self.window, text="Введите количество доступных призов такого типа").grid(row=5, column=0)
            prize_num_entry = customtkinter.CTkEntry(self.window, width=200)
            prize_num_entry.grid(row=6, column=0)

            # Prize text
            customtkinter.CTkLabel(self.window, text="Введите текст, отображающийся при получении данного приза").grid(row=7, column=0)
            prize_text_entry = tkinter.Text(self.window, width=40, height=5)
            prize_text_entry.grid(row=8, column=0)

            # Submit button
            submit_button = customtkinter.CTkButton(self.window, text='Готово',
                                                    command=lambda:
                                                    self.new_prize(prize_name = prize_entry.get(),
                                                                   prize_range = range_pk,
                                                                   prize_num = prize_num_entry.get(),
                                                                   prize_text = prize_text_entry.get('1.0', 'end-1c')),
                                                    state=tkinter.DISABLED)
            submit_button.grid(row=9, column=0)
            menu.config(bg="#5B97D3", borderwidth=0, activebackground="#4A7BAD")

        elif kwargs['option'] == 'Гость':
            # Build the form for creating a new guest
            customtkinter.CTkLabel(self.window, text='Введите имя или наименование гостя').grid(row=2, column=0)
            # The name of the guest
            guest_name = customtkinter.CTkEntry(self.window, width=200)
            guest_name.grid(row=3, column=0)
            guest_range = tkinter.StringVar()
            guest_range.set('Выберите диапазон для данного гостя')
            options = show_ranges()
            # Query the range options or state that there are no ranges
            menu_opts_ranges = process_query_ranges(options)

            # The ranges options
            menu = tkinter.OptionMenu(self.window, guest_range, *menu_opts_ranges,
                                      command=lambda _: check_for_activating_submit_button(
                                          guest_range, options,
                                          submit_button))  # This lambda configs the state of submit button and gets range_oid
            menu.grid(
                row=4, column=0)

            # Unique name for the guest
            customtkinter.CTkLabel(self.window, text="Введите уникальное имя для гостя, "
                                                     "которое он будет вводить для получения приза").grid(
                                                      row=7, column=0)
            guest_uid_entry = customtkinter.CTkEntry(self.window, width=200)
            guest_uid_entry.grid(row=8, column=0)

            # Submit button
            submit_button = customtkinter.CTkButton(self.window, text='Готово',
                                                    command=lambda:
                                                    self.new_guest(guest_name=guest_name.get(),
                                                                   guest_range=range_pk,
                                                                   guest_uid=guest_uid_entry.get()),
                                                    state=tkinter.DISABLED)
            submit_button.grid(row=9, column=0)
            menu.config(bg="#5B97D3", borderwidth=0, activebackground="#4A7BAD")

    @refresh_entry_window
    def refresh(self, *args, **kwargs):
        pass

    def __call__(self, parent_window):
        self.window = customtkinter.CTkToplevel()
        self.refresh()
        self.window.title('Добавить запись')
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
            font = tkinter.font.Font(family='Helvetica', size=14, weight='bold')
            customtkinter.CTkLabel(self.window, text='Призы и диапазоны', text_font=font, bg_color='#f2f2f2').pack(side='top')
            main_frame = customtkinter.CTkFrame(self.window, bg='#f2f2f2')
            main_frame.pack(fill=tkinter.BOTH, expand=1)

            my_canvas = customtkinter.CTkCanvas(main_frame, bg='#e3e3e3')
            my_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

            my_scrollbar = tkinter.Scrollbar(main_frame, orient=tkinter.VERTICAL, command=my_canvas.yview, bg='#f2f2f2')
            my_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

            second_frame = customtkinter.CTkFrame(my_canvas, bg='#f2f2f2')

            my_canvas.create_window((0, 0), window=second_frame, anchor='nw')
            # Show table
            customtkinter.CTkLabel(second_frame, text='Название приза').grid(row=0, column=0)
            customtkinter.CTkLabel(second_frame, text='Оставшееся количество').grid(row=0, column=1)
            customtkinter.CTkLabel(second_frame, text='Имя гостя').grid(row=0, column=4)
            customtkinter.CTkLabel(second_frame, text='Уникальный идентификатор гостя').grid(row=0, column=5)
            customtkinter.CTkLabel(second_frame, text='Полученный приз').grid(row=0, column=6)
            # Show all the ranges
            if ranges:
                for number_r, rng in enumerate(ranges):
                    rng_row = rng_row + number_max + 1
                    customtkinter.CTkLabel(second_frame, text='Диапазон ' + rng[1]).grid(row=rng_row + 1, column=0,
                                                                                         columnspan=6)
                    customtkinter.CTkButton(second_frame, pady=5, text='Удалить диапазон', bg='#e3e3e3', borderwidth=1,
                                            command=lambda range_button=rng: self.delete_range(range_button[0])).grid(
                        row=rng_row + 1, column=7
                    )
                    # Show all the prizes
                    prizes = show_prizes_of_given_range(rng[0])
                    guests = show_guests_of_given_range(rng[0])
                    if prizes:
                        for number_p, prize in enumerate(prizes):
                            # Name of the prize
                            customtkinter.CTkLabel(second_frame, text=prize[1]).grid(row=rng_row + number_p + 2,
                                                                                     column=0)
                            # Number of prizes of this type left
                            customtkinter.CTkLabel(second_frame, text=('Всего осталось: '+str(prize[3]))).grid(
                                row=rng_row + number_p + 2, column=1
                            )

                            # Update quantity button
                            customtkinter.CTkButton(second_frame, padx=5, bg='#e3e3e3', text='Изменить количество', command=lambda prize_oid=prize[0]: self.update_quantity(
                                prize_oid=prize_oid
                            )).grid(
                                row=rng_row + number_p + 2, column=2)

                            # Delete button
                            customtkinter.CTkButton(second_frame, pady=5, text='Удалить приз', bg='#e3e3e3',
                                                    command=lambda prize_button=prize: self.delete_prize(
                                                        prize_button[0])).grid(
                                row=rng_row + number_p + 2, column=3
                            )
                    if guests:
                        for number_g, guest in enumerate(guests):
                            # Name of the prize
                            customtkinter.CTkLabel(second_frame, text=guest[1]).grid(row=rng_row + number_g + 2,
                                                                                     column=4)
                            # Number of prizes of this type left
                            customtkinter.CTkLabel(second_frame, text=('Уникальный идентификатор: '+str(guest[3]))).grid(
                                row=rng_row + number_g + 2, column=5
                            )
                            # Show the prize
                            if guest[4]:
                                customtkinter.CTkLabel(second_frame, text=show_prize(guest[4])[0][1]).grid(
                                                       row=rng_row + number_g + 2, column=6)
                            else:
                                customtkinter.CTkLabel(second_frame, text='Этот гость еще ничего не выграл').grid(
                                                       row=rng_row + number_g + 2, column=6)

                            # Delete button
                            customtkinter.CTkButton(second_frame, pady=5, text='Удалить гостя', bg='#e3e3e3',
                                                    command=lambda guest_button=guest: self.delete_guest(
                                                        guest_button[0])).grid(
                                                    row=rng_row + number_g + 2, column=7)

                    # Make a new max row
                    number_max = max(rng_row + number_p, rng_row + number_g)

                # Show the number of guests and prizes
                final_number_max = number_max + max(number_g, number_r)
                number_of_prizes = 0
                list_of_prizes = show_all_prizes()
                for prize in list_of_prizes:
                    number_of_prizes += prize[3]
                number_of_prizes = str(number_of_prizes)
                number_of_guests = str(len(show_all_guests()))

                customtkinter.CTkLabel(second_frame, text='Количество призов: '+number_of_prizes).grid(row=final_number_max+2, column=0)
                customtkinter.CTkLabel(second_frame, text='Количество гостей: '+number_of_guests).grid(row=final_number_max + 2,
                                                                                                     column=1)

            else:
                customtkinter.CTkLabel(second_frame, text='В базе данных нет диапазонов или призов').grid(row=0,
                                                                                                          column=0)
            # Show data Labels

            customtkinter.CTkButton(self.window, text='Добавить новый приз/диапазон', text_font=font,
                                    command=lambda: entry_window(self)).pack(side=tkinter.LEFT, pady=5, padx=5)
            customtkinter.CTkButton(self.window, text='Очистить гостей от призов', text_font=font, command=lambda: self.clear_prizes()).pack(
                side=tkinter.LEFT, pady=5, padx=5)
            customtkinter.CTkButton(self.window, text='Назад', text_font=font, command=self.window.destroy).pack(
                padx=5, pady=5, side=tkinter.LEFT)
            customtkinter.CTkButton(self.window, text='Сбалансировать количество призов и гостей',
                                    text_font=font, command=self.balance_prizes).pack(
                padx=5, pady=5, side=tkinter.LEFT)

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
    def clear_prizes(self, *args, **kwargs):
        """This function deletes all entries about prizes won by guests
        """
        clear_prizes_guests()

    @refresh_data_window
    def balance_prizes(self, *args, **kwargs):
        """This function balances all prizes and guests
        """
        balance_numbers_of_guests_and_prizes()

    def update_quantity(self, prize_oid):
        """This function allows user to update the quantity of a given prize
        """
        def update_prize(prize_oid, number):
            """This function commits changes to the database and closes the window
            """
            try:
                int(number)
                update_prize_quantity(prize_oid=prize_oid, number=number)
                self.refresh()
                new_window.destroy()
            except ValueError:
                customtkinter.CTkLabel(new_window, text='Вы ввели неверный номер').pack()

        new_window = customtkinter.CTkToplevel()
        customtkinter.CTkLabel(new_window, text='Введите количество призов данного типа').pack()
        quantity_entry = customtkinter.CTkEntry(new_window, width=200)
        quantity_entry.pack()

        update_button = customtkinter.CTkButton(new_window, text='Готово', command=lambda:
                                                update_prize(prize_oid=prize_oid, number=quantity_entry.get()))
        update_button.pack()

    @refresh_data_window
    def refresh(self, *args, **kwargs):
        pass

    def __call__(self):
        self.window = customtkinter.CTkToplevel()
        self.refresh()
        self.window.title('Призы и диапазоны')
        self.window.resizable(height=None)
        self.window.geometry('1920x1080')


class RandomDrawingWindow:
    """This window shows all the guests eligible for prizes and lists them with the winning button
    """

    def refresh_random_drawing_window(func):
        def wrapper(self, *args, option='Выберите ваш диапазон!', **kwargs):
            for widget in self.window.winfo_children():
                widget.destroy()

            func(self, *args, **kwargs)

            clicked = tkinter.StringVar()

            font = tkinter.font.Font(family='Bahnshrift SemiCondensed', size=36, weight='bold')

            customtkinter.CTkLabel(self.window, text="Введите ваше имя или наименование").place(
                rely=0.1, relx=0.5, anchor='center')
            guest_uid_entry = customtkinter.CTkEntry(self.window, width=200, placeholder_text='Ваше имя или наименование')
            guest_uid_entry.place(rely=0.13, relx=0.5, anchor='center')

            clicked.set(option)

            self.img = tkinter.PhotoImage(file='logo.png')

            winner_button = tkinter.Button(self.window, image=self.img, compound='top', height='500px',
                                                        width='937px', text ='', borderwidth=0, relief='raised', fg='white',
                                                        command=lambda r=clicked.get(): self.determine_winner(guest_uid=guest_uid_entry.get()))
            winner_button.place(rely=0.5, relx=0.5, anchor='center')

            customtkinter.CTkLabel(self.window, text="Нажмите на кнопку чтобы получить приз!", text_font=font).place(
                rely=0.9, relx=0.5, anchor='center')

        return wrapper

    @refresh_random_drawing_window
    def determine_winner(self, guest_uid):

        def show_avaliable_prizes(guest_range):
            """This function checks if there are prizes left

            prize_list: list of tuples

            return: list of tuples of prizes quantity of which > 0
            """
            prize_list = show_prizes_of_given_range(guest_range)
            new_list = []
            for prize in prize_list:
                if int(prize[3]) > 0:
                    new_list.append(prize)
            return new_list

        def play_animation(progress_bar_widget, window):
            for i in range(300):
                progress_bar_widget['value'] += 0.33333
                window.update_idletasks()
                time.sleep(0.001)

        def center_window(window):
            window.update_idletasks()  # Add this line
            width = window.winfo_width()
            height = window.winfo_height()
            x = (window.winfo_screenwidth() // 2) - (width // 2)
            y = (window.winfo_screenheight() // 2) - (height // 2)
            window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


        # show guest using guest_uid
        try:
            print(guest_uid)
            guest_full = show_guest_by_uid(guest_uid=guest_uid)
            if guest_full:
                guest = guest_full
            else:
                raise sqlite3.OperationalError

            if is_guest_the_winner(guest[0]):
                customtkinter.CTkLabel(self.window, text='У вас уже есть подарок!').place(rely=0.15, relx=0.5, anchor='center')
                return

            guest_range = guest[2]
            prize_list = show_avaliable_prizes(guest_range)
            if prize_list:
                # Determine the prize
                prize = choice(prize_list)
                # Background image
                background_image = tkinter.PhotoImage(file='background.png')
                # Show the winning window
                win_wnd = customtkinter.CTkToplevel()
                win_wnd.title('Ваш приз!')
                win_wnd.geometry('1600x1200')
                center_window(win_wnd)
                # Win frame init

                background_canvas = tkinter.Canvas(win_wnd, width=2000, height=2000)
                background_canvas.create_image(0, 0, image=background_image, anchor='nw')
                background_canvas.pack(fill='both')

                win_wnd.config(bg='#f2f2f2')
                font = tkinter.font.Font(family='Bahnshrift SemiCondensed', size=36, weight='bold')

                # Loading animation for determining the prize
                loading_text = customtkinter.CTkLabel(win_wnd, text_font=font, text="Определяем приз...", bg_color='#154189',
                                                      text_color='#ffffff')
                loading_text.place(anchor='center', relx=0.5, rely=0.4)

                loading_bar = ttk.Progressbar(win_wnd, orient='horizontal', length=400,
                                                           mode='determinate', style='green.Horizontal.TProgressbar')
                loading_bar.place(anchor='center', rely=0.5, relx=0.5)

                play_animation(loading_bar, win_wnd)

                loading_bar.destroy()
                loading_text.destroy()
                background_canvas.destroy()

                background_canvas = tkinter.Canvas(win_wnd, width=1600, height=1200)
                background_canvas.create_image(0, 0, image=background_image, anchor='nw')
                background_canvas.pack(fill='both')

                customtkinter.CTkLabel(win_wnd, text=('Поздравляем!'),
                                       text_font=font, bg_color='#154189', text_color='#ffffff').place(
                    anchor='center', rely=0.2, relx=0.5)

                win_frame = tkinter.Frame(win_wnd, width=800, height=200)

                win_frame.place(anchor='center', rely=0.5, relx=0.5)

                text = customtkinter.CTkLabel(win_frame, text=prize[4], text_font=font, bg_color='#154189', width=1000,
                                              height=200, wraplength=800, text_color='#ffffff')
                text.place(anchor='center', rely=0.5, relx=0.5)
                quit_button = tkinter.Button(win_wnd, text='Назад', font=font, command=win_wnd.destroy, background='#154189')


                # Add prize to the guest
                update_prize_guest(guest_oid=guest[0], prize_oid=prize[0])

                # Update the quantity of prizes
                update_prize_quantity(prize_oid=prize[0])
            else:
                font = tkinter.font.Font(family='Helvetica', size=36, weight='bold')
                customtkinter.CTkLabel(self.window, text=('Для этого диапазона нет призов!'), text_font=font).place(
                    anchor='center',
                    rely=0.15, relx=0.5)
        except sqlite3.OperationalError:
            customtkinter.CTkLabel(self.window, text="К сожалению, такое имя не найдено").place(
                rely=0.15, relx=0.5, anchor='center'
            )


    @refresh_random_drawing_window
    def new_window_drawing_window(self, *args, **kwargs):
        pass

    def center_window(self):
        self.window.update_idletasks()  # Add this line
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def __call__(self):
        self.window = customtkinter.CTkToplevel()
        self.new_window_drawing_window()
        self.window.title('Призы')
        self.window.geometry('1920x1080')
        self.center_window()


class PasswordWindow:

    def refresh_password_window(func):
        def wrapper(self, *args, **kwargs):
            for widget in self.window.winfo_children():
                widget.destroy()

            func(self, *args, **kwargs)

            customtkinter.CTkLabel(self.window, text='Для изменения информации введите пароль').pack()
            password = tkinter.StringVar()
            psw = customtkinter.CTkEntry(self.window, textvariable=password, width=100)
            psw.pack()
            customtkinter.CTkButton(self.window, text='Готово', command=lambda password=password: self.submit_password(
                password=password.get())).pack()

        return wrapper

    def submit_password(self, *args, **kwargs):
        if kwargs['password'] == '112233':
            self.window.destroy()
            data_window()
        else:
            self.wrong_password()

    @refresh_password_window
    def wrong_password(self, *args, **kwargs):
        customtkinter.CTkLabel(self.window, text='Неверный пароль!').pack()

    @refresh_password_window
    def new_window(self):
        pass

    def center_window(self):
        self.window.update_idletasks()  # Add this line
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def __call__(self):
        self.window = customtkinter.CTkToplevel()
        self.new_window()
        self.center_window()


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
            customtkinter.CTkButton(text='Призы и диапазоны', command=password_window, width=400, height=100).place(
                anchor='center', relx=0.5, rely=0.5)
            customtkinter.CTkButton(text='Получить приз!', command=random_drawing_window, width=400,
                                    height=100).place(anchor='center', relx=0.5, rely=0.2)

        return wrapper

    @refresh_main_window
    def new(self):
        pass


    def center_window(self):
        self.window.update_idletasks()  # Add this line
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


    def __call__(self):
        self.window = customtkinter.CTk()
        self.window.title('Призы')
        self.window.geometry('1920x1080')
        self.new()
        self.window.eval('tk::PlaceWindow . center')
        self.center_window()


random_drawing_window = RandomDrawingWindow()
password_window = PasswordWindow()
entry_window = AddEntryWindow()
data_window = DataWindow()
main_window = MainWindow()
main_window()
