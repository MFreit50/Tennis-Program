#a class that circumvents the necessity for a real calendar before the release version of the product
class AbstractCalendar:
    def __init__(self, days_per_week, num_weeks):
        self.days_per_week = days_per_week
        self.num_weeks = num_weeks
        self.selected_days = set()

    def toggle_day(self, week, day):
        if (week, day) in self.selected_days:
            self.selected_days.remove((week, day))
        else:
            self.selected_days.add((week, day))

    def select_all_in_row(self, week):
        for day in range(self.days_per_week):
            self.selected_days.add((week, day))

    def deselect_all_in_row(self, week):
        for day in range(self.days_per_week):
            self.selected_days.discard((week, day))

    def select_all_in_column(self, day):
        for week in range(self.num_weeks):
            self.selected_days.add((week, day))

    def deselect_all_in_column(self, day):
        for week in range(self.num_weeks):
            self.selected_days.discard((week, day))

    def get_selected_days(self):
        return sorted(self.selected_days)