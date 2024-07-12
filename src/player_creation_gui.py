import tkinter as tk
from tkinter import messagebox
from player import Player
from abstract_calendar import AbstractCalendar
from abstract_calendar_gui import AbstractCalendarGUI

class PlayerCreationGUI:
    def __init__(self, parent, coordinator, coordinator_gui, player=None):
        self.parent = parent
        self.coordinator = coordinator
        self.coordinator_gui = coordinator_gui
        self.player = player
        self.window = tk.Toplevel(parent)
        self.window.title("Create Player" if player is None else "Edit Player")

        self.selected_days = []

        self.days_per_week = coordinator.user_request.days_per_week
        self.number_of_weeks = coordinator.user_request.number_of_weeks

        tk.Label(self.window, text="Player Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Total Games").grid(row=1, column=0)
        self.total_games_entry = tk.Entry(self.window)
        self.total_games_entry.grid(row=1, column=1)

        if player:
            self.name_entry.insert(0, player.name)
            self.total_games_entry.insert(0, player.total_games)
            self.selected_days = player.days_unavailable

        self.days_unavailable_button = tk.Button(self.window, text="Select Days Unavailable", command=self.open_calendar)
        self.days_unavailable_button.grid(row=2, column=0, columnspan=2)

        self.create_button = tk.Button(self.window, text="Create Player" if player is None else "Save Changes", command=self.create_or_edit_player)
        self.create_button.grid(row=3, column=0, columnspan=2)

    def open_calendar(self):
        self.calendar_window = tk.Toplevel(self.window)
        calendar = AbstractCalendar(self.days_per_week, self.number_of_weeks)
        self.calendar_gui = AbstractCalendarGUI(self.calendar_window, calendar, initial_selected_days=self.selected_days, on_submit=self.on_calendar_submit)
        self.calendar_gui.pack()
        self.calendar_window.protocol("WM_DELETE_WINDOW", self.on_calendar_close)

    def on_calendar_submit(self, selected_days):
        self.selected_days = selected_days
        self.calendar_window.destroy()

    def on_calendar_close(self):
        self.selected_days = self.calendar_gui.calendar.get_selected_days()
        self.calendar_window.destroy()

    def create_or_edit_player(self):
        try:
            name = self.name_entry.get()
            total_games = int(self.total_games_entry.get())
            days_unavailable = self.selected_days
        except ValueError:
            messagebox.showerror("Error", f"Invalid Input: {self.total_games_entry.get()}")
            return

        #check that name entry isn't blank
        if len(self.name_entry.get().strip()) == 0:
            messagebox.showerror("Error", f"Invalid Input: Player must have name")
            return

        if self.player: # Editing player
            self.player.name = name
            self.player.total_games = total_games
            self.player.days_unavailable = days_unavailable
        else:           # Creating a new player
            player = Player(name, total_games, days_unavailable)
            self.coordinator.add_player(player)

        self.coordinator_gui.update_player_list()
        self.window.destroy()