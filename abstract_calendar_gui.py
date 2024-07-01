import tkinter as tk
from tkinter import ttk

class AbstractCalendarGUI(tk.Frame):
    def __init__(self, parent, calendar, initial_selected_days=None, on_submit=None):
        super().__init__(parent)
        self.calendar = calendar
        self.parent = parent
        self.on_submit = on_submit
        self.parent.title("Abstract Calendar")

        # Set the initial size to 75% of the screen's width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        initial_width = int(screen_width * 0.75)
        initial_height = int(screen_height * 0.75)
        self.parent.geometry(f"{initial_width}x{initial_height}")

        # Define styles for buttons
        self.style = ttk.Style(self)
        self.style.configure("TButton", padding=6, relief="raised", width=10, height=2)
        self.style.configure("Selected.TButton", padding=6, relief="raised", background="#5B9BD5", foreground="black")

        self.create_widgets()

        # If initial selected days are provided, select and highlight them
        if initial_selected_days:
            for week, day in initial_selected_days:
                self.calendar.toggle_day(week, day)
                self.update_button_color(week, day)

    def create_widgets(self):
        # Create a canvas and a frame to contain the grid of buttons
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky='nsew')
        
        canvas = tk.Canvas(container)
        canvas.grid(row=0, column=0, sticky='nsew')

        scrollbar_y = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x = ttk.Scrollbar(container, orient='horizontal', command=canvas.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # Configure the grid to expand with window resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.buttons = []

        for week in range(self.calendar.num_weeks):
            row_buttons = []

            # Add week number label
            week_label = tk.Label(self.frame, text=f'Week {week + 1}')
            week_label.grid(row=week, column=0, padx=5, pady=5)

            for day in range(self.calendar.days_per_week):
                btn = ttk.Button(self.frame, text=f'{week*self.calendar.days_per_week + day + 1}',
                                style="TButton",
                                command=lambda w=week, d=day: self.toggle_day(w, d))
                btn.grid(row=week, column=day+1, padx=5, pady=5, ipadx=10, ipady=10)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

            # Add row select button
            row_select_btn = ttk.Button(self.frame, text='Select Row', command=lambda w=week: self.toggle_row(w))
            row_select_btn.grid(row=week, column=self.calendar.days_per_week+1, padx=5, pady=5)

        for day in range(self.calendar.days_per_week):
            # Add column select button
            col_select_btn = ttk.Button(self.frame, text='Select Col', command=lambda d=day: self.toggle_column(d))
            col_select_btn.grid(row=self.calendar.num_weeks, column=day+1, padx=5, pady=5)

        # Submit button
        submit_btn = ttk.Button(self.frame, text='Submit', command=self.submit)
        submit_btn.grid(row=self.calendar.num_weeks + 1, columnspan=1, padx=5, pady=10)

        # Clear selections button
        clear_btn = ttk.Button(self.frame, text='Clear Selections', command=self.clear_selections)
        clear_btn.grid(row=self.calendar.num_weeks + 1, columnspan=1, column=self.calendar.days_per_week, padx=5, pady=10)

        # Ensure all widgets are displayed before setting window size
        self.parent.update_idletasks()

        # Calculate the minimal size required to display all widgets
        min_width = self.frame.winfo_reqwidth()
        min_height = self.frame.winfo_reqheight()

        # Calculate 75% of the screen's width and height
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        max_width = int(screen_width * 0.75)
        max_height = int(screen_height * 0.75)

        # Calculate a buffer for the minimal size
        buffer_width = 20
        buffer_height = 20

        # Set the window size to the minimal size plus the buffer or 75% of screen size, whichever is smaller
        final_width = min(min_width + buffer_width, max_width)
        final_height = min(min_height + buffer_height, max_height)
        self.parent.geometry(f"{final_width}x{final_height}")

        self.frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Bind mouse wheel events for scrolling
        canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, canvas))
        canvas.bind_all("<Shift-MouseWheel>", lambda event: self._on_shiftmouse(event, canvas))

        # Ensure the calendar GUI fills the window
        self.pack(fill=tk.BOTH, expand=True)
        container.pack(fill=tk.BOTH, expand=True)

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shiftmouse(self, event, canvas):
        canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def toggle_day(self, week, day):
        self.calendar.toggle_day(week, day)
        self.update_button_color(week, day)

    def toggle_row(self, week):
        row_selected = all((week, day) in self.calendar.selected_days for day in range(self.calendar.days_per_week))
        if row_selected:
            self.calendar.deselect_all_in_row(week)
        else:
            self.calendar.select_all_in_row(week)
        self.update_row_colors(week)

    def toggle_column(self, day):
        col_selected = all((week, day) in self.calendar.selected_days for week in range(self.calendar.num_weeks))
        if col_selected:
            self.calendar.deselect_all_in_column(day)
        else:
            self.calendar.select_all_in_column(day)
        self.update_column_colors(day)

    def update_button_color(self, week, day):
        btn = self.buttons[week][day]
        if (week, day) in self.calendar.selected_days:
            btn.config(style="Selected.TButton")
        else:
            btn.config(style="TButton")

    def update_row_colors(self, week):
        for day in range(self.calendar.days_per_week):
            self.update_button_color(week, day)

    def update_column_colors(self, day):
        for week in range(self.calendar.num_weeks):
            self.update_button_color(week, day)

    def submit(self):
        selected_days = self.calendar.get_selected_days()
        print("Selected days:", selected_days)
        if self.on_submit:
            self.on_submit(selected_days)
        self.parent.destroy()

    def clear_selections(self):
        self.calendar.selected_days.clear()
        for week in range(self.calendar.num_weeks):
            self.update_row_colors(week)