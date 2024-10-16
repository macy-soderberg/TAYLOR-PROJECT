import tkinter as tk
import sqlite3
import pygame
from tkinter import Tk, Button
from tkinter import font
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

# Connect to the database
conn = sqlite3.connect('ERAS.db')
cursor = conn.cursor()


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("eras.mp3")
    pygame.mixer.music.play()
 
def stop_music():
    pygame.mixer.music.stop()


def add_show():
    country = country_entry.get()
    city = city_entry.get()
    openers = openers_entry.get()
    night_num = night_num_entry.get()
    date = date_entry.get()
    stadium_id = stadium_id_entry.get()

    if country and city and openers and night_num and date and stadium_id:
        try:
            # Connect to the database
            conn = sqlite3.connect('ERAS.db')
            cursor = conn.cursor()

            # Get the next available ShowID
            cursor.execute('SELECT MAX(ShowID) FROM SHOWS')
            result = cursor.fetchone()
            if result[0] is None:
                next_id = 1
            else:
                next_id = result[0] + 1

            # Insert the new row into the table
            cursor.execute('''
                INSERT INTO SHOWS (ShowID, Country, City, Openers, NightNum, Date, StadiumID)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (next_id, country, city, openers, night_num, date, stadium_id))

            conn.commit()
            conn.close()

            messagebox.showinfo('Success', 'Show added successfully!')
            new_window.destroy()  # Close the add show window after successful addition
        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Error adding show: {e}')
    else:
        messagebox.showwarning('Incomplete Input', 'Please fill in all fields.')







def add_show_window():
    global new_window
    new_window = tk.Toplevel(root)
    new_window.title('Add New Show')

    # Create labels and entry fields for input
    tk.Label(new_window, text='Country:').pack()
    global country_entry
    country_entry = tk.Entry(new_window)
    country_entry.pack()

    tk.Label(new_window, text='City:').pack()
    global city_entry
    city_entry = tk.Entry(new_window)
    city_entry.pack()

    tk.Label(new_window, text='Openers:').pack()
    global openers_entry
    openers_entry = tk.Entry(new_window)
    openers_entry.pack()

    tk.Label(new_window, text='NightNum:').pack()
    global night_num_entry
    night_num_entry = tk.Entry(new_window)
    night_num_entry.pack()

    tk.Label(new_window, text='Date (MM-DD-YY):').pack()
    global date_entry
    date_entry = tk.Entry(new_window)
    date_entry.pack()

    tk.Label(new_window, text='StadiumID:').pack()
    global stadium_id_entry
    stadium_id_entry = tk.Entry(new_window)
    stadium_id_entry.pack()

    # Button to add the show
    add_button = tk.Button(new_window, text='Add Show', command=add_show)
    add_button.pack()

def add_stadium():
    name = name_entry.get()
    capacity = capacity_entry.get()
    stadium_type = type_entry.get()
    address = address_entry.get()

    if name and capacity and stadium_type and address:
        try:
            # Connect to the database
            conn = sqlite3.connect('ERAS.db')
            cursor = conn.cursor()

            # Get the next available StadiumID
            cursor.execute('SELECT MAX(StadiumID) FROM STADIUMS')
            result = cursor.fetchone()
            if result[0] is None:
                next_id = 1
            else:
                next_id = result[0] + 1

            # Insert the new row into the table
            cursor.execute('''
                INSERT INTO STADIUMS (StadiumID, Name, Capacity, Type, Address)
                VALUES (?, ?, ?, ?, ?)
            ''', (next_id, name, capacity, stadium_type, address))

            conn.commit()
            conn.close()

            messagebox.showinfo('Success', f'Stadium added successfully! StadiumID: {next_id}')
        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Error adding stadium: {e}')
    else:
        messagebox.showwarning('Incomplete Input', 'Please fill in all fields.')








def open_add_stadium_window():
    global new_window
    new_window = tk.Toplevel(root)
    new_window.title('Add Stadium')

    # Create labels and entry fields for input
    tk.Label(new_window, text='Name:').pack()
    global name_entry
    name_entry = tk.Entry(new_window)
    name_entry.pack()

    tk.Label(new_window, text='Capacity:').pack()
    global capacity_entry
    capacity_entry = tk.Entry(new_window)
    capacity_entry.pack()

    tk.Label(new_window, text='Type:').pack()
    global type_entry
    type_entry = tk.Entry(new_window)
    type_entry.pack()

    tk.Label(new_window, text='Address:').pack()
    global address_entry
    address_entry = tk.Entry(new_window)
    address_entry.pack()

    # Button to add the stadium
    add_button = tk.Button(new_window, text='Add Stadium', command=add_stadium)
    add_button.pack()

def open_setlist_window():
    # Create a new window for selecting date
    select_date_window = tk.Toplevel(root)
    select_date_window.title('Select Date')

    # Function to open the setlist entry window based on selected date
    def open_setlist_entry_window():
        selected_date = date_combobox.get()

        if selected_date:
            # Close the date selection window
            select_date_window.destroy()

            # Create a new window for setlist entry
            setlist_entry_window = tk.Toplevel(root)
            setlist_entry_window.title('Add Setlist')

            # Function to add setlist to database
            def add_setlist_to_db():
                guitar = guitar_entry.get()
                piano = piano_entry.get()
                guitar_album = guitar_album_entry.get()
                piano_album = piano_album_entry.get()
                num_songs = num_songs_entry.get()

                if guitar and piano and guitar_album and piano_album and num_songs:
                    try:
                        # Connect to the database
                        conn = sqlite3.connect('ERAS.db')
                        cursor = conn.cursor()

                        # Get the ShowID based on the selected date
                        cursor.execute('''
                            SELECT ShowID FROM SHOWS
                            WHERE Date = ?
                        ''', (selected_date,))
                        show_id_result = cursor.fetchone()

                        if show_id_result:
                            show_id = show_id_result[0]

                            # Insert the setlist into SONGS table
                            cursor.execute('''
                                INSERT INTO SONGS (SongID, Guitar, Piano, GuitarAlbum, PianoAlbum, NumSongs)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (show_id, guitar, piano, guitar_album, piano_album, num_songs))

                            conn.commit()
                            conn.close()

                            messagebox.showinfo('Success', 'Setlist added successfully!')
                            setlist_entry_window.destroy()  # Close the setlist entry window
                        else:
                            messagebox.showwarning('No Show Found', 'No show found for the selected date.')
                    except sqlite3.Error as e:
                        messagebox.showerror('Error', f'Error adding setlist: {e}')
                else:
                    messagebox.showwarning('Incomplete Input', 'Please fill in all fields.')

            # Labels and entry fields for setlist information
            tk.Label(setlist_entry_window, text='Guitar:').pack()
            guitar_entry = tk.Entry(setlist_entry_window)
            guitar_entry.pack()

            tk.Label(setlist_entry_window, text='Piano:').pack()
            piano_entry = tk.Entry(setlist_entry_window)
            piano_entry.pack()

            tk.Label(setlist_entry_window, text='Guitar Album:').pack()
            guitar_album_entry = tk.Entry(setlist_entry_window)
            guitar_album_entry.pack()

            tk.Label(setlist_entry_window, text='Piano Album:').pack()
            piano_album_entry = tk.Entry(setlist_entry_window)
            piano_album_entry.pack()

            tk.Label(setlist_entry_window, text='Number of Songs:').pack()
            num_songs_entry = tk.Entry(setlist_entry_window)
            num_songs_entry.pack()

            # Button to add setlist
            add_setlist_button = tk.Button(setlist_entry_window, text='Add Setlist', command=add_setlist_to_db)
            add_setlist_button.pack()

    # Dropdown for selecting date
    date_combobox = ttk.Combobox(select_date_window)
    date_combobox.pack()

    # Button to open setlist entry window
    open_setlist_button = tk.Button(select_date_window, text='Open Setlist Entry', command=open_setlist_entry_window)
    open_setlist_button.pack()

    # Function to populate the date dropdown based on data from the database
    def populate_date_dropdown():
        try:
            # Connect to the database
            conn = sqlite3.connect('ERAS.db')
            cursor = conn.cursor()

            # Fetch distinct dates from SHOWS table
            cursor.execute('SELECT DISTINCT Date FROM SHOWS')
            dates = [row[0] for row in cursor.fetchall()]

            conn.close()

            date_combobox['values'] = dates
        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Error accessing database: {e}')

    # Populate the date dropdown initially
    populate_date_dropdown()






def edit_date():
    # Ask the user for the old date
    old_date = simpledialog.askstring('Edit Date', 'Enter the old date (MM-DD-YY):')
    
    if old_date:
        # Ask the user for the new date
        new_date = simpledialog.askstring('Edit Date', 'Enter the new date (MM-DD-YY):')

        if new_date:
            try:
                # Connect to the database
                conn = sqlite3.connect('ERAS.db')
                cursor = conn.cursor()

                # Update the date in the SHOWS table
                cursor.execute('''
                    UPDATE SHOWS
                    SET Date = ?
                    WHERE Date = ?
                ''', (new_date, old_date))

                conn.commit()
                conn.close()

                messagebox.showinfo('Success', 'Date updated successfully!')
            except sqlite3.Error as e:
                messagebox.showerror('Error', f'Error updating date: {e}')
        else:
            messagebox.showwarning('Incomplete Input', 'Please enter the new date.')
    else:
        messagebox.showwarning('Incomplete Input', 'Please enter the old date.')






def get_surprise_songs():
    # Function to handle getting surprise songs info
    def show_song_info():
        selected_city = city_combobox.get()
        selected_night = night_combobox.get()

        if selected_city and selected_night:
            try:
                # Connect to the database
                conn = sqlite3.connect('ERAS.db')
                cursor = conn.cursor()

                # Get the ShowID based on selected city and night
                cursor.execute('''
                    SELECT ShowID FROM SHOWS
                    WHERE City = ? AND NightNum = ?
                ''', (selected_city, selected_night))
                show_id_result = cursor.fetchone()

                if show_id_result:
                    show_id = show_id_result[0]

                    # Get the Guitar and Piano from SONGS table
                    cursor.execute('''
                        SELECT Guitar, Piano FROM SONGS
                        WHERE SongID = ?
                    ''', (show_id,))
                    song_info = cursor.fetchone()

                    conn.close()

                    if song_info:
                        guitar_info, piano_info = song_info
                        messagebox.showinfo('Surprise Song Info', f'Guitar: {guitar_info}\nPiano: {piano_info}')
                    else:
                        messagebox.showwarning('No Song Found', 'No song information found for the selected city and night.')
                else:
                    messagebox.showwarning('No Show Found', 'No show found for the selected city and night.')
            except sqlite3.Error as e:
                messagebox.showerror('Error', f'Error accessing database: {e}')
        else:
            messagebox.showwarning('Incomplete Selection', 'Please select both a city and a night number.')

    # Create the new window for surprise songs
    surprise_window = tk.Toplevel(root)
    surprise_window.title('Surprise Songs')

    # Label and dropdown for selecting city
    city_label = tk.Label(surprise_window, text='City:')
    city_label.pack()
    city_combobox = ttk.Combobox(surprise_window)
    city_combobox.pack()

    # Label and dropdown for selecting night number
    night_label = tk.Label(surprise_window, text='Night:')
    night_label.pack()
    night_combobox = ttk.Combobox(surprise_window)
    night_combobox.pack()

    # Populate the city dropdown based on data from the database
    def populate_city_dropdown():
        try:
            # Connect to the database
            conn = sqlite3.connect('ERAS.db')
            cursor = conn.cursor()

            # Fetch cities from SHOWS table
            cursor.execute('SELECT DISTINCT City FROM SHOWS')
            cities = [row[0] for row in cursor.fetchall()]

            conn.close()

            city_combobox['values'] = cities
        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Error accessing database: {e}')

    # Populate the night dropdown based on the selected city
    def populate_night_dropdown(event):
        selected_city = city_combobox.get()

        if selected_city:
            try:
                # Connect to the database
                conn = sqlite3.connect('ERAS.db')
                cursor = conn.cursor()

                # Fetch night numbers for the selected city
                cursor.execute('''
                    SELECT NightNum FROM SHOWS
                    WHERE City = ?
                ''', (selected_city,))
                nights = [row[0] for row in cursor.fetchall()]

                conn.close()

                night_combobox['values'] = nights
            except sqlite3.Error as e:
                messagebox.showerror('Error', f'Error accessing database: {e}')

    # Populate the city dropdown initially
    populate_city_dropdown()

    # Bind the function to populate the night dropdown to the city selection event
    city_combobox.bind('<<ComboboxSelected>>', populate_night_dropdown)

    # Button to get surprise songs info
    get_info_button = tk.Button(surprise_window, text='Get Song Info', command=show_song_info)
    get_info_button.pack()





def open_date_selection_window():
    # Create a new window for date selection
    date_selection_window = tk.Toplevel(root)
    date_selection_window.title('Select Date')

    # Function to get show info based on selected date
    def get_show_info():
        selected_date = date_combobox.get()

        if selected_date:
            try:
                # Connect to the database
                conn = sqlite3.connect('ERAS.db')
                cursor = conn.cursor()

                # Get the ShowID based on the selected date
                cursor.execute('''
                    SELECT ShowID FROM SHOWS
                    WHERE Date = ?
                ''', (selected_date,))
                show_id_result = cursor.fetchone()

                if show_id_result:
                    show_id = show_id_result[0]

                    # Get the show details from SHOWS table
                    cursor.execute('''
                        SELECT City, NightNum, Openers, StadiumID FROM SHOWS
                        WHERE ShowID = ?
                    ''', (show_id,))
                    show_info = cursor.fetchone()

                    if show_info:
                        city, night_num, openers, stadium_id = show_info

                        # Get the stadium name from STADIUMS table
                        cursor.execute('''
                            SELECT Name FROM STADIUMS
                            WHERE StadiumID = ?
                        ''', (stadium_id,))
                        stadium_name_result = cursor.fetchone()
                        if stadium_name_result:
                            stadium_name = stadium_name_result[0]
                        else:
                            stadium_name = 'Unknown Stadium'

                        # Get the guitar and piano from SONGS table
                        cursor.execute('''
                            SELECT Guitar, Piano FROM SONGS
                            WHERE SongID = ?
                        ''', (show_id,))
                        song_info = cursor.fetchone()

                        conn.close()

                        if song_info:
                            guitar_info, piano_info = song_info
                            # Display the show information in a new window
                            display_show_info(city, night_num, openers, stadium_name, guitar_info, piano_info)
                        else:
                            messagebox.showwarning('No Song Info', 'No song information found for the selected show.')
                    else:
                        messagebox.showwarning('No Show Info', 'No show information found for the selected show.')
                else:
                    messagebox.showwarning('No Show Found', 'No show found for the selected date.')
            except sqlite3.Error as e:
                messagebox.showerror('Error', f'Error accessing database: {e}')
        else:
            messagebox.showwarning('Incomplete Selection', 'Please select a date.')

    # Dropdown for selecting date
    date_combobox = ttk.Combobox(date_selection_window)
    date_combobox.pack()

    # Button to get show info
    get_info_button = tk.Button(date_selection_window, text='Get Show Info', command=get_show_info)
    get_info_button.pack()

    # Function to populate the date dropdown based on data from the database
    def populate_date_dropdown():
        try:
            # Connect to the database
            conn = sqlite3.connect('ERAS.db')
            cursor = conn.cursor()

            # Fetch distinct dates from SHOWS table
            cursor.execute('SELECT DISTINCT Date FROM SHOWS')
            dates = [row[0] for row in cursor.fetchall()]

            conn.close()

            date_combobox['values'] = dates
        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Error accessing database: {e}')

    # Populate the date dropdown initially
    populate_date_dropdown()

def display_show_info(city, night_num, openers, stadium_name, guitar_info, piano_info):
    # Create a new window to display show information
    show_info_window = tk.Toplevel(root)
    show_info_window.title('Show Information')

    # Display the show information in labels
    tk.Label(show_info_window, text=f'City: {city}').pack()
    tk.Label(show_info_window, text=f'NightNum: {night_num}').pack()
    tk.Label(show_info_window, text=f'Openers: {openers}').pack()
    tk.Label(show_info_window, text=f'Stadium: {stadium_name}').pack()
    tk.Label(show_info_window, text=f'Guitar: {guitar_info}').pack()
    tk.Label(show_info_window, text=f'Piano: {piano_info}').pack()





# Create the main window
root = tk.Tk()
root.title("Add Entries")

canvas = tk.Canvas(root, height = 240 , width = 480)
canvas.pack()

background_image = tk.PhotoImage(file = 'tsback1.png')
background_label = tk.Label(root, image = background_image)
background_label.place(relwidth = 1, relheight = 1)

# Create buttons to open each window
add_show_button = tk.Button(root, text='Add Show', font=('Comic Sans MS',9), width=20, height=1, bg='#72BFDF', fg="navy", command=lambda: add_show_window())
add_show_button.place(x=10, y=10)

#add_stadium_button = tk.Button(root, text="Add Stadium", font=('Comic Sans MS',9), width=20, height=1, command=add_stadium, bg='#72BFDF', fg="navy")
#add_stadium_button.place(x=170, y=10)

add_setlist_button = tk.Button(root, text='Add Setlist', font=('Comic Sans MS',9), width=20, height=1, bg='#72BFDF', fg="navy", command=open_setlist_window)
add_setlist_button.place(x=330, y=10)

play_music()  # Call the function to play music when the program starts
 
play_button = Button(root, text="Play Music", font=('Comic Sans MS',9), width=10, height=2, command=play_music, bg='#72BFDF', fg="navy")
play_button.place(x=30, y=90)

stop_button = Button(root, text="Stop Music", font=('Comic Sans MS',9), width=10, height=2, command=stop_music, bg='#72BFDF', fg="navy")
stop_button.place(x=380, y=90)

open_window_button = tk.Button(root, text='Add Stadium', font=('Comic Sans MS',9), width=20, height=1, bg='#72BFDF', fg="navy", command=open_add_stadium_window)
open_window_button.place(x=170, y=10)

edit_date_button = tk.Button(root, text='Edit Date', font=('Comic Sans MS',9), width=20, height=1, bg='#72BFDF', fg="navy", command=edit_date)
edit_date_button.place(x=10, y=200)

get_surprise_songs_button = tk.Button(root, text='Get Surprise Songs', font=('Comic Sans MS',9), width=20, height=1, bg='#72BFDF', fg="navy", command=get_surprise_songs)
get_surprise_songs_button.place(x=170, y=200)

get_info_button = tk.Button(root, text='Get Show Info', font=('Comic Sans MS',9), width=20, height=1, bg='#72BFDF', fg="navy", command=open_date_selection_window)
get_info_button.place(x=330, y=200)

# Start the main loop
root.mainloop()

# Close the connection when the application is closed
conn.close()