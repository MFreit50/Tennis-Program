import tkinter as tk
from player_creation_gui import PlayerCreationGUI
from abstract_calendar import AbstractCalendar
from abstract_calendar_gui import AbstractCalendarGUI
from coordinator import Coordinator
from coordinator_gui import CoordinatorGUI

if __name__ == "__main__":
    coordinator = Coordinator()
    gui = CoordinatorGUI(coordinator)
    gui.run()