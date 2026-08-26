import random
import matplotlib.pyplot as plt
import numpy as np

#chance to vast


def roll_dice():
    return random.randint(1, 6)

def get_turn(max_throws, vast_chance):
    throws = 0
    values = []
    prev_dice1 = 0
    prev_dice2 = 0
    while throws < max_throws:
        roll1 = 0
        roll2 = 0
        if (prev_dice1 != 0 ):
            roll1 = prev_dice1
        else:
            roll1 = roll_dice()
        if (prev_dice2 != 0 ):
            roll2 = prev_dice2
        else:
            roll2 = roll_dice()
        if roll1 + roll2 == 3:
            values += [[roll1, roll2]]
            break
        if sorted([roll1, roll2]) == [1,3] and max_throws - throws == 1:
            throws -= 1
        if sorted([roll1, roll2]) == [2,3] and vast_chance > random.random():
            print("Vast!")
            values += [[roll1, roll2]]
            break
        if (prev_dice1 == 0 and (roll1 == 1 or roll1 == 2) ):
            prev_dice1 = roll1
        elif (prev_dice1 == roll1):
            prev_dice1 = 0
        if (prev_dice2 == 0 and (roll2 == 1 or roll2 == 2) ):
            prev_dice2 = roll2
        elif (prev_dice2 == roll2):
            prev_dice2 = 0
        
        values += [[roll1, roll2]]
        throws += 1
        
    return values

def calc_losing_sips(mex_amount):
    return 2 ** (mex_amount)


def simulate_round(players, vast_chance = 0.3, use_mex_in_rule = True, previous_knight = -1, previous_knight_value = -1):
    sips = [0] * players
    sips_from_being_knight = [0] * players
    sips_from_31 = [0] * players
    sips_from_losing = [0] * players
    turns = 3 #you are allowed to throw three times
    mex_amount = 0
    current_knight = previous_knight
    knight_value = previous_knight_value
    highest_values_players = [0] * players
    results = []
    print("Starting round with ", players, " players", "vast chance: ", vast_chance, "use mex in rule: ", use_mex_in_rule, "previous knight: ", previous_knight, "previous knight value: ", previous_knight_value)
    
    
    for player in range(players):
        result = get_turn(turns, vast_chance)
        results += [result]
        print("Player ", player, "got ", result)
        if (len(result) < turns):
            #means mex was thrown
            mex_amount += 1
            if (use_mex_in_rule):
                #if mex in x rule is used set allowed turns to the rolls needed to get the mex
                print("Player ", player, "threw mex in ", len(result), " turns")
                turns = len(result)
        
        for x in result:
            if (x[0] == x[1]):
                #if the dices are the same
                if (x[0] == 1):
                    #if the dices are 1's
                    if (current_knight == player):
                        #if the player is the current knight
                        
                        knight_value += 1
                        print("Player ", player, "is the current knight increased knight value to ", knight_value)
                    else:
                        #if the player is not the current knight
                        current_knight = player
                        print("Player ", player, "is the new knight")
                        knight_value = 1
                else:
                    if (knight_value >= 0):
                        #if the dices are not 1's and there is a knight
                        print("Player ", player, "got a pair of ", x[0], "s", "giving ", x[0] * knight_value, " sips to the knight")
                        sips[current_knight] += x[0] * knight_value
                        sips_from_being_knight[current_knight] += x[0] * knight_value
                        
                    
            if (sorted(x) == [1, 3]):
                chosen_player = random.randint(0, players - 1)
                while (chosen_player == player):
                    chosen_player = random.randint(0, players - 1)
                sips[chosen_player] += 1
                sips_from_31[chosen_player] += 1
                print("Player ", player, "got 31 and giving 1 sip to player ", chosen_player)
        
        #makes it so that lowest number of the values is the first value
        array = sorted(result[len(result) - 1])
        #picks the last value to be first
        val1 = array[1]
        #picks the first value to be second
        val2 = array[0]
        
        highest_value = 0
        if (val1 == val2):
            #if values are the same become a three digit number
            highest_value = val1 * 100
        else:
            highest_value = val1 * 10 + val2
        #makes a mex number out of the values
        
        highest_values_players[player] = highest_value
    
    
    print(highest_values_players)
    #calculate which people have lost, the people with the lowest value are the loser
    
    array_to_find_loser = highest_values_players.copy()
    for x in array_to_find_loser:
        if (x == 21):
            array_to_find_loser[array_to_find_loser.index(x)] = 5000
    lowest_value = min(array_to_find_loser)
    losing_group = []
    for player in range(players):
        if (array_to_find_loser[player] == lowest_value and array_to_find_loser[player] != 21):
            losing_group += [player]
    print("Players ", losing_group, " lost the round getting ", calc_losing_sips(mex_amount), " sips")
    for lowest_player in losing_group:
        sips[lowest_player] += calc_losing_sips(mex_amount)
        sips_from_losing[lowest_player] += calc_losing_sips(mex_amount)
    
    
    round_info = round_results(results, sips, current_knight, knight_value, sips_from_being_knight, sips_from_31, sips_from_losing, mex_amount)
    return round_info
        





class round_results:
    def __init__(self, players_results, sips_gotten, current_knight, knight_value, sips_from_being_knight, sips_from_31, sips_from_losing, total_mexes):
        self.players_results = players_results
        self.sips_gotten = sips_gotten
        self.current_knight = current_knight
        self.knight_value = knight_value
        self.sips_from_being_knight = sips_from_being_knight
        self.sips_from_31 = sips_from_31
        self.sips_from_losing = sips_from_losing
        self.total_mexes = total_mexes
        
class game_results_data:
    def __init__(self, players_results, sips_gotten, sips_from_being_knight, sips_from_31, sips_from_losing, total_mexes):
        self.players_results = players_results
        self.sips_gotten = sips_gotten
        self.sips_from_being_knight = sips_from_being_knight
        self.sips_from_31 = sips_from_31
        self.sips_from_losing = sips_from_losing
        self.total_mexes = total_mexes

class plot_measurables:
    def __init__(self, average_sips_per_player, average_sips_from_being_knight, average_sips_from_31, average_sips_from_losing, average_mexes):
        self.average_sips_per_player = average_sips_per_player
        self.average_sips_from_being_knight = average_sips_from_being_knight
        self.average_sips_from_31 = average_sips_from_31
        self.average_sips_from_losing = average_sips_from_losing
        self.average_mexes = average_mexes


def simulate_game(players, rounds, vast_chance = 0.3, use_mex_in_rule = True):
    game_results = game_results_data([], [0] * players, [0] * players, [0] * players, [0] * players, 0)
    current_knight = -1
    knight_value = -1
    for round in range(rounds):
        result = simulate_round(players, vast_chance, use_mex_in_rule, current_knight, knight_value)
        game_results.players_results += result.players_results
        game_results.sips_gotten = [x + y for x, y in zip(game_results.sips_gotten, result.sips_gotten)]
        game_results.sips_from_being_knight = [x + y for x, y in zip(game_results.sips_from_being_knight, result.sips_from_being_knight)]
        game_results.sips_from_31 = [x + y for x, y in zip(game_results.sips_from_31, result.sips_from_31)]
        game_results.sips_from_losing = [x + y for x, y in zip(game_results.sips_from_losing, result.sips_from_losing)]
        game_results.total_mexes += result.total_mexes
        print("Round ", round, " results on total sips gotten: ", game_results.sips_gotten)
        current_knight = result.current_knight
        knight_value = result.knight_value
    return game_results

def get_measurables_from_game_results_data(game_results: game_results_data, players, rounds) -> plot_measurables:
    average_sips_per_player = sum(game_results.sips_gotten) / (players * rounds)
    average_sips_from_being_knight = sum(game_results.sips_from_being_knight) / (players * rounds)
    average_sips_from_31 = sum(game_results.sips_from_31) / (players * rounds)
    average_sips_from_losing = sum(game_results.sips_from_losing) / (players * rounds)
    average_mexes = game_results.total_mexes / rounds
    return plot_measurables(average_sips_per_player, average_sips_from_being_knight, average_sips_from_31, average_sips_from_losing, average_mexes)




rounds = 2000
player_amounts = [5,10,25,50]
results = []
for player_amount in player_amounts:
    result1 = simulate_game(player_amount, rounds)
    result2 = simulate_game(player_amount, rounds, use_mex_in_rule = False)
    results.append([get_measurables_from_game_results_data(result1, player_amount, rounds), get_measurables_from_game_results_data(result2, player_amount, rounds)])

print(results)
rule = [ "Mex in 3/2/1", "Mex in 3", "Verschil"]
all_data = []
for x in range(len(player_amounts)):
    data = {"Totaal slokken per speler": [results[x][0].average_sips_per_player, results[x][1].average_sips_per_player, abs(results[x][0].average_sips_per_player - results[x][1].average_sips_per_player)],
        "Slokken door ridder zijn": [results[x][0].average_sips_from_being_knight, results[x][1].average_sips_from_being_knight, abs(results[x][0].average_sips_from_being_knight - results[x][1].average_sips_from_being_knight)],
        "Slokken door gekozen te worden door 31": [results[x][0].average_sips_from_31, results[x][1].average_sips_from_31, abs(results[x][0].average_sips_from_31 - results[x][1].average_sips_from_31)],
        "Slokken door ronde verliezen": [results[x][0].average_sips_from_losing, results[x][1].average_sips_from_losing, abs(results[x][0].average_sips_from_losing - results[x][1].average_sips_from_losing)],
        "Mexen per ronde": [results[x][0].average_mexes, results[x][1].average_mexes, abs(results[x][0].average_mexes - results[x][1].average_mexes)]}
    all_data.append(data)



x = np.arange(len(rule))
width = 0.15
multiplier = 0
fig, axs = plt.subplots(2,2, layout='constrained')

index = 0
for a in range(2):
    for b in range(2):
        multiplier = 0
        for attribute, value in all_data[index].items():
            offset = width * multiplier
            rects = axs[a,b].bar(x + offset, value, width, label=attribute)
            axs[a,b].bar_label(rects, padding=3)
            multiplier += 1

        axs[a,b].set_ylabel('Gemiddelde aantal slokken')
        axs[a,b].set_title('Gemiddelde aantal slokken per speler per ronde, en mexen per ronde (' + str(player_amounts[index]) + " spelers)")
        axs[a,b].set_xticks(x + width, rule)
        axs[a,b].legend(loc='upper left', ncols=3)
        axs[a,b].set_ylim(0, 12)
        index += 1

plt.show()








    