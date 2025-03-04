import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import sys
import os

# ---------------------------
# Database Setup for Profile
# ---------------------------
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="papa0042",
        database="gameverse"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")


def open_profile():
    """Open a window to display profile information from the database."""
    if len(sys.argv) > 1:
        logged_in_username = sys.argv[1]
    else:
        logged_in_username = ""

    profile_win = tk.Toplevel(root)
    profile_win.title("Profile")
    profile_win.geometry("300x200")

    cursor.execute(f"SELECT * FROM users WHERE username='{logged_in_username}'")
    profile = cursor.fetchone()

    if profile:
        username, email = profile[1], profile[2]
    else:
        username, email = "Unknown Name", "unknown Username"

    tk.Label(profile_win, text="Profile", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(profile_win, text=f"Name: {username}", font=("Arial", 14)).pack(pady=5)
    tk.Label(profile_win, text=f"Username: {email}", font=("Arial", 14)).pack(pady=5)
    tk.Button(profile_win, text="Close", command=profile_win.destroy).pack(pady=10)


if len(sys.argv) > 1:
        logged_in_username = sys.argv[1]
else:
        logged_in_username = ""

cursor.execute(f"select * from users where username='{logged_in_username}'")
user=cursor.fetchone()

# ---------------------------
# Game Launch Functions
# ---------------------------

def tictactoe():
        """Launch Tic-Tac-Toe and add user_id & game_id to score table if not exists."""
        try:
            # Get user_id from users table
            cursor.execute("SELECT id FROM users WHERE username = %s", (logged_in_username,))
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "User not found!")
                return
            user_id = user[0]

            # Get game_id for Tic-Tac-Toe
            cursor.execute("SELECT id FROM games WHERE name = 'Tic-Tac-Toe'")
            game = cursor.fetchone()
            if not game:
                messagebox.showerror("Error", "Tic-Tac-Toe game entry not found!")
                return
            game_id = game[0]

            # Check if user_id and game_id already exist in the score table
            cursor.execute("SELECT * FROM scores WHERE user_id = %s AND game_id = %s", (user_id, game_id))
            existing_entry = cursor.fetchone()

            # If entry does not exist, insert into score table with initial score 0
            if not existing_entry:
                cursor.execute("INSERT INTO scores (user_id, game_id, score) VALUES (%s, %s, %s)", (user_id, game_id, 0))
                db.commit()

            # Launch the Tic-Tac-Toe game
            os.system(f"python Tic-Tac-Toe.py {logged_in_username}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


def launch_murderMystery():
    os.system(f"python murderMystery.py")



def treasurehunt():
    """Launch treasurehunt and add user_id & game_id to score table if not exists."""
    try:
        # Get user_id from users table
        cursor.execute("SELECT id FROM users WHERE username = %s", (logged_in_username,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found!")
            return
        user_id = user[0]

        # Get game_id for Tic-Tac-Toe
        cursor.execute("SELECT id FROM games WHERE name = 'Treasure Hunt'")
        game = cursor.fetchone()
        if not game:
            messagebox.showerror("Error", "Treasure Hunt game entry not found!")
            return
        game_id = game[0]

        # Check if user_id and game_id already exist in the score table
        cursor.execute("SELECT * FROM scores WHERE user_id = %s AND game_id = %s", (user_id, game_id))
        existing_entry = cursor.fetchone()

        # If entry does not exist, insert into score table with initial score 0
        if not existing_entry:
            cursor.execute("INSERT INTO scores (user_id, game_id, score) VALUES (%s, %s, %s)", (user_id, game_id, 0))
            db.commit()

        # Launch the Tic-Tac-Toe game
        os.system(f"python TreasureHunt.py {logged_in_username}")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def launch_mario():
    print("Launching Mario...")


def launch_sonic():
    print("Launching Sonic...")


# ---------------------------
# Learn or Die - Level Selection
# ---------------------------
def open_learn_or_die_levels():
    """Open a new window with 5 levels for 'Learn or Die'."""
    levels_win = tk.Toplevel(root)
    levels_win.title("Learn or Die - Select Level")
    levels_win.geometry("400x400")

    tk.Label(levels_win, text="Select Level", font=("Arial", 18, "bold")).pack(pady=10)
    cursor.execute(f"select level from scores where user_id={user[0]}")
    level=cursor.fetchone()
    for levels in range(1,level[0]+1):
        tk.Button(levels_win, text=f"Level {levels}", font=("Arial", 14), width=15,
                  command=lambda lvl=levels: launch_level(lvl)).pack(pady=5)

    tk.Button(levels_win, text="Close", command=levels_win.destroy).pack(pady=10)


def launch_level(level_number):
    # """Placeholder function to launch a selected level."""
    # try:
    #     # Get game_id for Learn Or Die game
    #     cursor.execute("SELECT * FROM games WHERE name = 'Learn Or Die'")
    #     game = cursor.fetchone()
    #     if not game:
    #         messagebox.showerror("Error", "Learn Or Die game entry not found!")
    #         return
    #
    #     print(game[0])
    #     # Check if user_id and game_id already exist in the score table
    #     cursor.execute("SELECT * FROM scores WHERE user_id = %s AND game_id = %s", (user[0], game[0]))
    #     existing_entry = cursor.fetchone()
    #
    #     # If entry does not exist, insert into score table with initial score 0
    #     if not existing_entry:
    #         cursor.execute("INSERT INTO scores (user_id, game_id) VALUES (%s, %s)", (user[0], game[0]))
    #         db.commit()
    #
    #     # Launch the game
    os.system(f"python LearnorDieL{level_number}.py {user[0]}")

    # except mysql.connector.Error as err:
    #     messagebox.showerror("Database Error", f"Error: {err}")


# ---------------------------
# Search Functionality
# ---------------------------
def update_buttons(search_query):
    """Update the visibility and order of game buttons based on the search query."""
    search_query = search_query.lower()
    filtered_buttons = [btn for btn in game_buttons if search_query in btn['text'].lower()]

    for widget in main_frame.winfo_children():
        widget.grid_forget()

    row, col = 0, 0
    for btn in filtered_buttons:
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        col += 1
        if col == num_columns:
            col = 0
            row += 1


def on_search_entry_change(*args):
    """Callback for when the search entry content changes."""
    search_query = search_var.get()
    update_buttons(search_query)


# ---------------------------
# Main Dashboard Setup
# ---------------------------
root = tk.Tk()
root.title("Dashboard")
root.geometry("900x600")
root.configure(bg="#f2f2f2")

# Load Background Image
bg_image = Image.open("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/HomeBackground.png")
bg_photo = ImageTk.PhotoImage(bg_image.resize((1600, 1000)))

canvas = tk.Canvas(root, width=900, height=600)
canvas.pack(fill="both", expand=True)
bg_image_id = canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Header Frame
header_frame = tk.Frame(root, bg="violet", bd=5)
header_frame.place(relx=0.5, rely=0.05, relwidth=1, relheight=0.15, anchor="n")

title_label = tk.Label(header_frame, text="Select GAME To Play", bg="violet", font=("Arial", 24))
title_label.pack(side="left", padx=20, pady=20)

profile_btn = tk.Button(header_frame, text="Profile", bg="violet", font=("Arial", 12), command=open_profile)
profile_btn.pack(side="right", padx=20, pady=20)

# Search Bar
search_var = tk.StringVar()
search_var.trace_add("write", on_search_entry_change)

search_entry = tk.Entry(root, textvariable=search_var, font=("Arial", 16), width=30, bg="violet", bd=2)
search_entry.place(relx=0.5, rely=0.2, anchor="n", y=30)

# Main Game Area
main_frame = tk.Frame(root, bg="violet", bd=5)
main_frame.place(relx=0.5, rely=0.35, relwidth=0.9, relheight=0.52, anchor="n")

num_columns = 3
main_frame.columnconfigure(list(range(num_columns)), weight=1, uniform="column")

game_buttons = []

# Creating each button
space_invaders_btn = tk.Button(main_frame, text="Tic-Tac-Toe", bg="#ff5555", fg="Black", font=("Arial", 24),
                               height=3, width=20, command=tictactoe)
game_buttons.append(space_invaders_btn)

pacman_btn = tk.Button(main_frame, text="Murder-Mystery", bg="#ffff66", fg="Black", font=("Arial", 24),
                       height=3, width=20, command=launch_murderMystery)
game_buttons.append(pacman_btn)

tetris_btn = tk.Button(main_frame, text="Treasure Hunt", bg="#66aaff", fg="Black", font=("Arial", 24),
                       height=3, width=20, command=treasurehunt)
game_buttons.append(tetris_btn)

mario_btn = tk.Button(main_frame, text="Mario", bg="#55ff55", fg="Black", font=("Arial", 24),
                      height=3, width=20, command=launch_mario)
game_buttons.append(mario_btn)

zelda_btn = tk.Button(main_frame, text="Learn or Die", bg="#cc66ff", fg="black", font=("Arial", 24),
                      height=3, width=20, command=open_learn_or_die_levels)  # Opens the level selection
game_buttons.append(zelda_btn)

sonic_btn = tk.Button(main_frame, text="Sonic", bg="#ff9933", fg="Black", font=("Arial", 24),
                      height=3, width=20, command=launch_sonic)
game_buttons.append(sonic_btn)

# Display Buttons
update_buttons("")

root.mainloop()
