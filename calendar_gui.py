import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta

class CalendarApp:
    def __init__(self, root, preselected_dates):
        self.root = root
        self.root.title("Calendar Selector")
        
        self.selected_dates = set(preselected_dates)
        
        # Calendar Widget
        self.cal = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(pady=20)
        
        self.highlight_dates()
        
        # Buttons Panel
        self.panel = ttk.Frame(root)
        self.panel.pack(pady=10)
        
        # Add Weekday Selection Buttons
        self.add_weekday_buttons()
        
        # Clear Selection Button
        self.clear_button = ttk.Button(self.panel, text="Clear Selections", command=self.clear_selections)
        self.clear_button.grid(row=0, column=7, padx=5, pady=5)
        
        # Selected Dates List
        self.selected_list_label = ttk.Label(root, text="Selected Dates:")
        self.selected_list_label.pack(pady=10)
        
        self.selected_listbox = tk.Listbox(root, height=10, width=50)
        self.selected_listbox.pack(pady=10)
        self.update_selected_listbox()
        
        # Finalize Button
        self.finalize_button = ttk.Button(root, text="Finalize Selections", command=self.finalize_selections)
        self.finalize_button.pack(pady=10)
        
        # Bind date selection
        self.cal.bind("<<CalendarSelected>>", self.date_selected)
        
    def highlight_dates(self):
        # Clear all existing highlights
        self.cal.calevent_remove('all')
        # Highlight selected dates
        for date in self.selected_dates:
            self.cal.calevent_create(date, 'selected', 'selected')

    def add_weekday_buttons(self):
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.weekday_buttons = []
        for idx, day in enumerate(weekdays):
            button = ttk.Button(self.panel, text=f"Every {day}", command=lambda d=day: self.toggle_weekday(d))
            button.grid(row=0, column=idx, padx=5, pady=5)
            self.weekday_buttons.append(button)
    
    def toggle_weekday(self, weekday):
        current_year = datetime.now().year
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    date = datetime(current_year, month, day).date()
                    if date.strftime('%A') == weekday:
                        if date in self.selected_dates:
                            self.selected_dates.remove(date)
                        else:
                            self.selected_dates.add(date)
                except ValueError:
                    continue
        self.update_selected_listbox()
        self.highlight_dates()

    def clear_selections(self):
        self.selected_dates.clear()
        self.update_selected_listbox()
        self.highlight_dates()

    def date_selected(self, event):
        date = self.cal.selection_get()
        if date in self.selected_dates:
            self.selected_dates.remove(date)
        else:
            self.selected_dates.add(date)
        self.update_selected_listbox()
        self.highlight_dates()

    def update_selected_listbox(self):
        self.selected_listbox.delete(0, tk.END)
        for date in sorted(self.selected_dates):
            self.selected_listbox.insert(tk.END, date.strftime('%Y-%m-%d'))

    def finalize_selections(self):
        self.root.quit()
        self.root.destroy()

def main(preselected_dates):
    root = tk.Tk()
    app = CalendarApp(root, preselected_dates)
    root.mainloop()
    selected_dates = sorted(app.selected_dates)
    return [date.strftime('%Y-%m-%d') for date in selected_dates]

if __name__ == "__main__":
    # Example preselected dates
    preselected_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in ['2024-05-01', '2024-05-05', '2024-05-10']]
    selected_dates = main(preselected_dates)
    print(selected_dates)