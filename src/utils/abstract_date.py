from typing import List, Dict

class AbstractDate:
    def __init__(self, number_of_weeks: int, days_per_week: int) -> None:
        """
        Initialize an AbstractDate instance.

        Args:
            number_of_weeks (int): The total number of weeks in the schedule.
            days_per_week (int): The number of days in each week.
        """
        self.number_of_weeks: int = number_of_weeks
        self.days_per_week: int = days_per_week
        self.current_week: int = 0
        self.current_day: int = 0
        self.date: List[int] = [self.current_week, self.current_day]
    
    def get_date(self) -> List[int]:
        """
        Get the current date in the form [current_week, current_day].

        Returns:
            List[int]: The current date.
        """
        return self.date
    
    def get_number_of_weeks(self) -> int:
        """
        Get the total number of weeks.

        Returns:
            int: The number of weeks.
        """
        return self.number_of_weeks
    
    def get_days_per_week(self) -> int:
        """
        Get the number of days per week.

        Returns:
            int: The number of days in each week.
        """
        return self.days_per_week
    
    def get_calendar_days(self) -> List[tuple]:
        """
        Get a list of all calendar days as (week, day) tuples.

        Returns:
            List[tuple]: A list of all days in the calendar.
        """
        return [(week, day) for week in range(self.number_of_weeks) for day in range(self.days_per_week)]
    
    def reset_date(self) -> None:
        """
        Reset the current date to the first week and first day.
        """
        self.current_week = 0
        self.current_day = 0
        self.date = [self.current_week, self.current_day]
    
    def increment_date(self) -> bool:
        """
        Increment the current date to the next day.

        If the current day is the last day of the week, move to the next week.
        If the current week exceeds the number of weeks, return False.

        Returns:
            bool: True if the date was incremented successfully, False if the end of the schedule was reached.
        """
        current_week = self.current_week
        current_day = self.current_day

        if current_day == self.days_per_week - 1:
            current_week += 1
            current_day = 0
        else:
            current_day += 1
        
        if current_week >= self.number_of_weeks:
            return False
        
        self.current_week = current_week
        self.current_day = current_day
        self.date = [self.current_week, self.current_day]
        return True  # Added to return True when the date increments successfully

    def print_date(self) -> str:
        """
        Return the current date as a formatted string.

        Returns:
            str: The current date in the format "Week: X, Day: Y".
        """
        return f'Week: {self.current_week}, Day: {self.current_day}\n'

    def to_dict(self) -> Dict[str, int]:
        """
        Convert the AbstractDate object to a dictionary.

        Returns:
            Dict[str, int]: A dictionary containing the number of weeks and days per week.
        """
        return {
            "number_of_weeks": self.number_of_weeks,
            "days_per_week": self.days_per_week
        }
    
    @staticmethod
    def from_dict(json: Dict[str, int]) -> 'AbstractDate':
        """
        Create an AbstractDate instance from a dictionary.

        Args:
            json (Dict[str, int]): A dictionary with keys "number_of_weeks" and "days_per_week".

        Returns:
            AbstractDate: An instance of AbstractDate created from the provided dictionary.
        """
        return AbstractDate(
            json["number_of_weeks"],
            json["days_per_week"]
        )