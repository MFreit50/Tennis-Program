import tkinter as tk
from tkinter import messagebox
from player_creation_gui import PlayerCreationGUI

class CoordinatorGUI:
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.root = tk.Tk()
        self.root.title("Coordinator GUI")

        # User Request Section

        '''
        Temporarily Removed because 
        days per week * number of weeks 
        is a better metric for determining 
        number of matches to generate

        tk.Label(self.root, text="Number of Matches").grid(row=0, column=0)
        self.number_of_matches_entry = tk.Entry(self.root)
        self.number_of_matches_entry.grid(row=0, column=1)
        '''
        tk.Label(self.root, text="Days per Week").grid(row=1, column=0)
        self.days_per_week_entry = tk.Entry(self.root)
        self.days_per_week_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Number of Weeks").grid(row=2, column=0)
        self.number_of_weeks_entry = tk.Entry(self.root)
        self.number_of_weeks_entry.grid(row=2, column=1)

        #self.number_of_matches_entry.insert(0, self.coordinator.user_request.number_of_matches)
        self.days_per_week_entry.insert(0, self.coordinator.user_request.days_per_week)
        self.number_of_weeks_entry.insert(0, self.coordinator.user_request.number_of_weeks)

        # Player Creation Section
        self.create_player_button = tk.Button(self.root, text="Create Players", command=self.open_player_creation_window)
        self.create_player_button.grid(row=4, column=0, columnspan=2)

        # Player List Section
        tk.Label(self.root, text="Players").grid(row=5, column=0, columnspan=2)
        self.player_listbox = tk.Listbox(self.root)
        self.player_listbox.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.update_player_list()
        self.player_listbox.bind("<Button-3>", self.show_player_menu)   # Right Click
        self.player_listbox.bind("<Double-Button-1>", self.edit_player) # Double Click

        # Match Generation Section
        self.generate_matches_button = tk.Button(self.root, text="Generate Matches", command=self.generate_matches)
        self.generate_matches_button.grid(row=7, column=0, columnspan=2)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_user_request(self, ignore_error_box) -> bool:

        try:
            #number_of_matches = int(self.number_of_matches_entry.get())
            number_of_matches = int(self.days_per_week_entry.get() * int(self.number_of_weeks_entry.get()))
            days_per_week = int(self.days_per_week_entry.get())
            number_of_weeks = int(self.number_of_weeks_entry.get())
        except ValueError:
            if ignore_error_box == False:
                messagebox.showerror("Error", f"Invalid input for user request")
            return False
        
        #if number_of_matches < 1 or days_per_week < 1 or number_of_weeks < 1:
        
        if days_per_week < 1 or number_of_weeks < 1:
            if ignore_error_box == False:
                messagebox.showerror("Error", f"User Request Values must be above 1")
            return False
        
        self.coordinator.create_user_request(number_of_matches, days_per_week, number_of_weeks)
        return True

    def open_player_creation_window(self):
        # player creation needs info in user request
        if self.create_user_request(ignore_error_box=False) == True:
            PlayerCreationGUI(self.root, self.coordinator, self)
        else:
            return

    def generate_matches(self):
        if self.create_user_request(ignore_error_box=False) == True:
            self.coordinator.generate_matches()
            messagebox.showinfo("Info", "Matches generated")

    def update_player_list(self):
        self.player_listbox.delete(0, tk.END)
        for player in self.coordinator.player_list:
            self.player_listbox.insert(tk.END, player.name)
    
    def show_player_menu(self, event):
        try:
            index = self.player_listbox.nearest(event.y)
            self.player_listbox.selection_clear(0, tk.END)
            self.player_listbox.selection_set(index)
            selected_player = self.player_listbox.get(index)
        except tk.TclError:
            return

        if selected_player:
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Edit Player", command=lambda: self.edit_player(None))
            menu.add_command(label="Remove Player", command=self.remove_player)
            menu.post(event.x_root, event.y_root)

    def edit_player(self, event):
        selected_index = self.player_listbox.curselection()
        if selected_index:
            player = self.coordinator.player_list[selected_index[0]]
            PlayerCreationGUI(self.root, self.coordinator, self, player=player)
    
    def remove_player(self):
        selected_index = self.player_listbox.curselection()
        if selected_index:
            player = self.coordinator.player_list[selected_index[0]]
            self.coordinator.remove_player(player)
            self.update_player_list()
    
    def on_close(self):
        self.create_user_request(ignore_error_box=True)
        self.coordinator.finalize()
        self.root.destroy()

    def run(self):
        self.root.mainloop()