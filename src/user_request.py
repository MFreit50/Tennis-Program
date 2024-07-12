class UserRequest():
    def __init__(self, number_of_matches, days_per_week, number_of_weeks):
        self.number_of_matches = number_of_matches
        self.days_per_week = days_per_week
        self.number_of_weeks = number_of_weeks

    def user_request_is_valid(self):
        return True
    
    #Serialization and Deserialization Functions
    def to_dict(self):
        return{
            "number_of_matches": self.number_of_matches,
            "days_per_week": self.days_per_week,
            "number_of_weeks": self.number_of_weeks
        }
    
    @staticmethod
    def from_dict(player_json):
        return UserRequest(player_json["number_of_matches"], player_json["days_per_week"], player_json["number_of_weeks"])