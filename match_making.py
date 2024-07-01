from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpBinary, LpStatus
import itertools

class MatchMaking():
    def __init__(self, days_per_week, number_of_weeks):
        self.days_per_week = days_per_week
        self.number_of_weeks = number_of_weeks
        self.current_week = 0
        self.current_day = 0
        self.date = (self.current_week, self.current_day)

    def generate_matches(self, players, number_of_matches) -> dict:
        self.generate_matches2(players, number_of_matches)
        return
        matches = {}
        for i in range(number_of_matches):
            match = self.generate_match(players)
            player_list = []
            for player in match:
                player_list.append(player.name)
            matches[f"match number {i}"] = player_list

        print(f"{matches}")
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
    
    def experiment(self, number_of_matches, players):
        # Create the problem
        prob = LpProblem("MatchScheduling", LpMaximize)

        # Variables
        matches = [(i, j) for i in range(number_of_matches) for j in range(4)]
        x = LpVariable.dicts("x", (matches, [player.name for player in players]), cat='Binary')

        for match_num in range(number_of_matches):
            # Increment the date to get the correct week and day
            self._increment_date()
            current_week, current_day = self.date

            # Define match for this iteration
            match = [(match_num, j) for j in range(4)]

            # Each match must have exactly 4 different players
            for j in range(4):
                prob += lpSum(x[(match_num, j)][player.name] for player in players) == 1

            for player in players:
                # Ensure each player can only play one position per match
                prob += lpSum(x[(match_num, j)][player.name] for j in range(4)) <= 1

                # Players must not exceed their total games
                prob += lpSum(x[m][player.name] for m in matches) <= player.games_left()

                # Players must not play on unavailable days
                if current_day in player.days_unavailable:
                    for m in match:
                        prob += x[m][player.name] == 0

        # Objective: Maximize diversity and balance
        prob += lpSum(x[match][player.name] for match in matches for player in players)

        # Solve the problem
        prob.solve()

        # Print the results
        for match in matches:
            for player in players:
                if x[match][player.name].varValue:
                    print(f"{match}: {player.name}")

    def increment_date(self):
        self.current_day += 1
        if self.current_day >= self.days_per_week:
            self.current_day = 0
            self.current_week += 1
        self.date = (self.current_week, self.current_day)

        self.date = (self.current_week, self.current_day)

    def generate_matches2(self, players, number_of_matches):
        player_names = [player.name for player in players]
        
        # Define the optimization problem
        prob = LpProblem("Matchmaking_Optimization", LpMaximize)

        # Define variables: match variables are 1 if player is in the match, 0 otherwise
        matches = LpVariable.dicts("Match", (range(number_of_matches), player_names), 0, 1, LpBinary)
        match_played = LpVariable.dicts("MatchPlayed", range(number_of_matches), 0, 1, LpBinary)

        # Constraints: Each match must have exactly 4 players or not happen at all
        for match in range(number_of_matches):
            prob += lpSum([matches[match][player] for player in player_names]) == 4 * match_played[match]

        # Constraints: Each player cannot exceed their total games
        for player in players:
            prob += lpSum([matches[match][player.name] for match in range(number_of_matches)]) <= player.total_games

        # Constraints: Players must be available on the day of the match
        for match in range(number_of_matches):
            self.increment_date()
            for player in players:
                if self.date in player.days_unavailable:
                    prob += matches[match][player.name] == 0

        # Objective: Maximize the total number of matches played
        prob += lpSum([match_played[match] for match in range(number_of_matches)])

        # Solve the problem
        prob.solve()

        # Check if the problem was solved successfully
        if LpStatus[prob.status] != 'Optimal':
            print("An optimal solution was not found.")
            return {}

        # Extract results
        match_results = {}
        for match in range(number_of_matches):
            if match_played[match].varValue == 1:
                match_results[f"match number {match}"] = [player for player in player_names if matches[match][player].varValue == 1]

        # Debugging: Verify player match counts
        player_match_count = {player.name: 0 for player in players}
        for match in match_results.values():
            for player in match:
                player_match_count[player] += 1
        
        for player in players:
            if player_match_count[player.name] > player.total_games:
                print(f"Error: Player {player.name} is scheduled for more than {player.total_games} games.")
        
        print(f"{match_results}")
        return match_results
