import GUI
from GUI_database_functions import create_database_or_connect

create_database_or_connect()

GUI.main_window.window.mainloop()