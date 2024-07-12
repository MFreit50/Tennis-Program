from data_engine import DataEngine
from user_request import UserRequest
from player import Player
from match_making import MatchMaking
import copy

class Coordinator:
    def __init__(self):
        self.data_engine = DataEngine()
        self.user_request = self.data_engine.read_user_request(UserRequest)
        self.player_list = self.data_engine.read_player_info_file(Player)
        self.match_making = MatchMaking(self.user_request.days_per_week, self.user_request.number_of_weeks)
    
    def create_user_request(self, number_of_matches, days_per_week, number_of_weeks):
        self.user_request = UserRequest(number_of_matches=number_of_matches, days_per_week=days_per_week, number_of_weeks=number_of_weeks)
        self.update_user_request()
    
    def create_player_list(self):
        self.player_list = self.data_engine.read_player_info_file()

    def add_player(self, player):
        self.player_list.append(player)
        self.update_player_list()
    
    def remove_player(self, player):
        self.player_list.remove(player)
        self.update_player_list()

    def generate_matches(self):
        player_list_copy = copy.deepcopy(self.player_list)
        matches = self.match_making.generate_matches(player_list_copy, self.user_request.days_per_week * self.user_request.number_of_weeks)
        player_list_copy.clear()
        self.data_engine.write_matches(matches)

    #update user files
    def update_player_list(self) -> None:
        self.data_engine.write_player_info_file(self.player_list)
    
    def update_user_request(self) -> None:
        self.data_engine.write_user_request(self.user_request)
        self.update_match_making()
    
    def update_match_making(self) -> None:
        try:
            self.match_making = MatchMaking(self.user_request.days_per_week, self.user_request.number_of_weeks)
        except Exception:
            return
    def finalize(self) -> None:
        self.update_player_list()
        self.update_user_request()