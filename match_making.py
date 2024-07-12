class MatchMaking():
    def __init__(self, days_per_week, number_of_weeks):
        self.player_matrix = 0

        #calculating current date
        self.day = days_per_week
        self.week = number_of_weeks
        self.current_week = 0
        self.current_day = 0
        self.date = (self.current_week, self.current_day)

    def generate_matches(self, players, number_of_matches) -> dict:
        matches = {}
        for i in range(number_of_matches):
            match = self.generate_match(players)
            player_list = []
            for player in match:
                player_list.append(player.name)
            matches[f"match number {i}"] = player_list
        return matches
    
    def generate_match(self, players) -> list:
        available_players = self.filter_available_players(players)
        if self.current_week == 16:
            print(f"{available_players}")

        #matches must contain at least 4 players
        if len(available_players) < 4:
            print("match could not be generated")
            self._increment_date() #hotfix
            return []
        
        #sort players by priority
        sorted_players = sorted(available_players, key=lambda player: player.match_priority)

        #pick top 4 players by priority
        generated_match = sorted_players[-4:]
        self.update_match_priority(generated_match, player_present_in_match=True)

        #remove top 4 players from the original list
        sorted_players = sorted_players[:-4]
        self.update_match_priority(sorted_players, player_present_in_match=False)
        
        self._increment_date()
        return generated_match
    
    def update_match_priority(self, players, player_present_in_match) -> None:
        for player in players:
            if player_present_in_match == True:
                player.record_player_presence()
            else:
                player.record_player_absence()


    def filter_available_players(self, players) -> list:
        available_players = []
        print(f"{self.date}")
        for player in players:
            if player.is_eligible_to_play(self.date) == True:
                available_players.append(player)
            else:
                player.record_player_absence()

        return available_players
    
    def _increment_date(self) -> None:
        if self.current_day == self.day - 1:
            self.current_week += 1
            self.current_day = 0
        else:
            self.current_day += 1
        
        if self.current_week >= self.week:
            self.current_week = 0  # Reset week if we surpass the total number of weeks

        self.date = (self.current_week, self.current_day)