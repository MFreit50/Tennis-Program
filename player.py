class Player():
    def __init__(self, name, total_games, days_unavailable):
        self.name = name
        self.total_games = total_games
        self.days_unavailable = days_unavailable
        self.games_played = 0
        self.consecutive_days_not_played = 0
        self.consecutive_days_played = 0
        self.match_priority = 0 #likely-hood of player joining a match
        self.calculate_priority()

    def is_eligible_to_play(self, date) -> bool:
        return self.games_left() > 0 and date not in self.days_unavailable
    
    def record_player_presence(self):
        self.consecutive_days_played += 1
        self.games_played += 1
        self.consecutive_days_not_played = 0
        self.calculate_priority()
    
    def record_player_absence(self):
        self.consecutive_days_not_played += 1
        self.consecutive_days_played = 0
        self.calculate_priority()
    
    def calculate_priority(self):
        UD = len(self.days_unavailable)
        CDP = self.consecutive_days_played
        CDNP = self.consecutive_days_not_played
        GL = self.games_left()
        self.match_priority = (UD * 0.15) - (CDP * 1.20) + (CDNP * 1.20) + (GL * 0.20)

    def games_left(self):
        return self.total_games - self.games_played
    
    #to string methods
    def __str__(self) -> str:
        return f"Player(player_name={self.name},total_games={self.total_games},days_unavailable={self.days_unavailable},games_played={self.games_played},consecutive_days_not_played={self.consecutive_days_not_played},consecutive_days_played={self.consecutive_days_played},match_priority={self.match_priority})"

    def __repr__(self) -> str:
        return f"Player(player_name={self.name},total_games={self.total_games},days_unavailable={self.days_unavailable})"
    
    #Serialization and Deserialization Functions
    def to_dict(self):
        return{
            "player_name": self.name,
            "total_games": self.total_games,
            "days_unavailable": self.days_unavailable
        }
    
    @staticmethod
    def from_dict(player_json):
        return Player(player_json["player_name"], player_json["total_games"], player_json["days_unavailable"])