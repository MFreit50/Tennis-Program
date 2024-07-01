
import json

class DataEngine():
    def read_player_info_file(self, Player) -> list:
        try:
            with open("players.json", "r") as file:
                players_dicts = json.load(file)
        except FileNotFoundError:
            print(f"The file players.json does not exist.")
            print(f"Creating players.json file...")

            with open("players.json", "w") as file:
                json.dump([], file)

            print(f"players.json created")
            return []
        players_list = [Player.from_dict(player_data) for player_data in players_dicts]
        return players_list
    
    def write_player_info_file(self, players_list) -> None:
        players_dicts = [player.to_dict() for player in players_list]
        with open("players.json", "w") as file:
            json.dump(players_dicts,file, indent=4)
        return
    
    def read_user_request(self, UserRequest):
        try:
            with open("save.json", "r") as file:
                user_request = json.load(file)
        except FileNotFoundError:
            user_request = UserRequest(0,0,0)
            self.write_user_request(user_request)
            return user_request
        user_request = UserRequest.from_dict(user_request)
        return user_request
    
    def write_user_request(self, user_request) -> None:
        user_request_dict = user_request.to_dict()
        with open("save.json", "w") as file:
            json.dump(user_request_dict, file, indent=4)
        return