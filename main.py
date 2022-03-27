from sre_constants import SUCCESS
from card import Card
import random
import sys
from poker import TexasPokerHand
from itertools import combinations
import os

MAX_ITERATION = 10000

def find_highest_hand(cards, player_cards):
    """
    This function will take in a list of cards and
        return the highest hand possible from the combinations.
    """
    # Create a list of possible hands.
    possible_hands = make_possible_hands(cards, player_cards)

    # Find the highest hand.
    highest_hand = sorted(
        possible_hands,
        key=lambda hand: hand.hand_ranking,
        reverse=True)[0]

    return highest_hand


def make_possible_hands(cards, player_cards):
    """
    This function will take in a list of cards
    and return a list of possible hands.
    It includes 2 card on the hand, 3 community card and 2 cards from deck.
    Possible combinations are: 5!/3!*2! = 120
    """
    # Create a list of possible hands.

    possible_cards = combinations(cards, 3)
    possible_hands = [TexasPokerHand(*possible_cards, *player_cards) for
                      possible_cards in possible_cards]
    return possible_hands


def try_two_cards(players, community_cards, two_cards):
    """
    This function will try to find the highest hand based on the
    cards on players hand and the community cards and two cards picked.

    """

    player_hands = {}
    # Create a list of players and their hands. Hand icludes two cards
    # and community cards and cards in players hand.
    for player in players:
        player_hands[player] = [*community_cards, *two_cards]

    # Given the 7 set of cards for each player find the highest
    # hand possible from the combination
    player_hand_rankings = {}
    for player in player_hands:
        player_hand_rankings[player] = find_highest_hand(
            player_hands[player], player_cards=players[player])

   # print(player_hand_rankings)
    # Find the player with highest hand
    highest_hand = sorted(
        player_hand_rankings,
        key=lambda hand: player_hand_rankings[hand].hand_ranking,
        reverse=True)[0]
    return player_hand_rankings, highest_hand, two_cards


def make_the_winner(players_csv_file, first_three_community_cards, the_winner,debug=False,quiet=True,max_iteration=MAX_ITERATION):
    """
    This function will take in a players_csv_file,
    a list of first_three_community_cards, and the winner.
    It will the return the two cards that needs to be drawn from the deck
    to make sure the designated winner wins the game.
    This is not an idempotent function and is based on random sampling.
    Hence given the same set of inputs its not guranteed to produce
    same results.

    Arguments:
        players_csv_file: a csv file with players and their hands.
        first_three_community_cards: a list of the first three community cards.
        the_winner: the winner of the game.
        debug: A flag to print out info regarding the function run 
            setting this flag also returns the number of iteration it took to get the result
        quiet: A flag to prevent the function from printing outputs
        max_iteration: max number of iterations you want to run before failing this function
            default set to 1000
    """
    # A new card deck is intialised with each function run.
    card_deck = [Card( suit, rank) for suit in ['C','D','H','S']  \
        for rank in [ 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]


    # Open the players_csv_file and read the lines.
    with open(players_csv_file, 'r') as f:
        lines = f.readlines()[1:]
        # Create a list of players.
        players = {}
        for line in lines:
            if len(line.split(','))>2: # if there are enough cards
                player_name = line.split(',')[0]
                cards_str = line.strip().split(',')[1:]
                player_cards = []
                for card_str in cards_str:
                    card_suit = card_str[0]
                    card_rank = "10" if  len(card_str[1:])>=2 else card_str[1]
                    player_cards.append(Card(card_suit,card_rank))
                    try:
                        # try remove the cards from card deck
                        card_deck.remove(Card(card_suit,card_rank))

                    except ValueError as e:
                        # terminate the program if the card is not in the deck
                        print("Error: {}".format(e))
                        print("{} not in Card deck".format(Card(card_suit,card_rank)))
                        sys.exit(1)
                players[player_name] = player_cards



    community_cards = []

    for comm_card in first_three_community_cards:
        card_suit = comm_card[0]
        card_rank = "10" if  len(comm_card[1:])>=2 else comm_card[1]
        community_cards.append(Card(card_suit,card_rank))
    try:
        # take card out of the deck
        for comm_card in community_cards:
            card_deck.remove(comm_card)

    except BaseException:
        # terminate the program if the card is not in the deck
        print("Error: {}".format(e))
        print(f'Error!! {comm_card} Card not in deck')
        sys.exit(1)

    iteration = 1
    all_possible_two_cards = list(combinations(card_deck, 2))

    SUCCESS = 0

    player_hand_rankings, highest_hand, two_cards = try_two_cards(
        players, community_cards, two_cards=all_possible_two_cards.pop())

    while highest_hand != the_winner and len(all_possible_two_cards) > 0 and iteration < max_iteration:
        # iterate until we get the right winner
        #print("Iteration: ",iteration)
        player_hand_rankings, highest_hand, two_cards = try_two_cards(
            players, community_cards, two_cards= all_possible_two_cards.pop())
        iteration += 1

    if highest_hand == the_winner:
        SUCCESS=1

    if debug:
        if not quiet:
            print("\n")
            print(f"It took {iteration} iterations to find the required cards ")
            print(f'Winner: {the_winner}')
            print(f'Cards:')
            print(f'All Community cards: \t {community_cards} {two_cards}')
            print("_" * 100)
            print(
                f'{"Player":10}|{"Card in Hand":20}|{"Hands":30}|{"Hand Type":20}|{"Hand Ranking":10}')
            print("_" * 100)
            for player in player_hand_rankings.keys():
                print(
                    f'{player:10}|{str(players[player]):20}|{str(player_hand_rankings[player]):10}')
            print("_" * 100)
            print(f'Required Cards: {two_cards}')
            print("\n")
        return two_cards,iteration,SUCCESS
    
    if len(all_possible_two_cards)==0:
        print("Unable to find a Win for the given inputs")
        return None
    if iteration==max_iteration:
        print("Unable to find a Win for the given inputs max_iteration reached Terminating...")
        return None
    return [str(card) for card in two_cards]


def main():
    if "-d" in sys.argv[1:] or "--debug" in sys.argv[1:]:
        two_cards = make_the_winner('players.csv', ['S2', 'C9', 'C4'], 'utur',debug=True)
    else:
        two_cards = make_the_winner('players.csv', ['S2', 'C9', 'C4'], 'utur',debug=False)

    print(two_cards)


if __name__ == "__main__":
    main()
