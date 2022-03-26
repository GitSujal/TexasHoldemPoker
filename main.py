from card import Card
import random
import sys
from poker import TexasPokerHand
from itertools import combinations

card_deck = [Card(suit, rank) for suit in ['C', 'D', 'H', 'S'] for rank in ['A',\
     '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]



def find_highest_hand(cards, player_cards):
    """
    This function will take in a list of cards and
        return the highest hand possible from the combinations.
    """
    # Create a list of possible hands.
    possible_hands = make_possible_hands(cards,player_cards)

    # Find the highest hand.
    highest_hand = sorted(possible_hands, key=lambda hand: hand.hand_ranking, reverse=True)[0]

    return highest_hand

def make_possible_hands(cards,player_cards):
    """
    This function will take in a list of cards 
    and return a list of possible hands.
    It includes 2 card on the hand, 3 community card and 2 cards from deck.
    Possible combinations are: 5!/3!*2! = 120
    """
    # Create a list of possible hands.
    
    possible_cards =  combinations(cards, 3)
    possible_hands = [TexasPokerHand(*possible_cards,*player_cards) for \
         possible_cards in possible_cards]
    return possible_hands


def try_two_cards(players,community_cards,card_deck):
    """
    This function will randomly pick two cards 
    from the deck and try to find the highest hand based on the 
    cards on players hand and the community cards.
    """
    # Choose two cards at a time randomly from the deck without replacement
    two_cards = random.sample(card_deck,k=2)
    
    player_hands = {}
    # Create a list of players and their hands. Hand icludes two cards 
    # and community cards and cards in players hand.
    for player in players:
        player_hands[player] = [*community_cards, *two_cards]

    # Given the 7 set of cards for each player find the highest
    # hand possible from the combination    
    player_hand_rankings = {}    
    for player in player_hands:
        player_hand_rankings[player] = find_highest_hand(player_hands[player],\
            player_cards=players[player])

   #print(player_hand_rankings)
    # Find the player with highest hand
    highest_hand = sorted(player_hand_rankings, key=lambda \
        hand: player_hand_rankings[hand].hand_ranking, reverse=True)[0]
    return player_hand_rankings,highest_hand,two_cards

def make_the_winner(players_csv_file, first_three_community_cards, the_winner):
    """
    This function will take in a players_csv_file, 
    a list of first_three_community_cards, and the winner.
    It will return a list of the players and their winnings.
    """

    # Open the players_csv_file and read the lines.
    with open(players_csv_file, 'r') as f:
        lines = f.readlines()[1:]     
        # Create a list of players.
        players = {}
        for line in lines:
            players[line.split(',')[0]]=[Card(line.strip().split(',')[1][0],\
                line.strip().split(',')[1][1]),\
                 Card(line.strip().split(',')[2][0],\
                     line.strip().split(',')[2][1])]
            
            try:
                # take cards out of the deck
                card_deck.remove(players[line.split(',')[0]][0])
                card_deck.remove(players[line.split(',')[0]][1])
            except ValueError as e:
                print("Card not in deck")
                

    community_cards = [Card(comm_card[0],comm_card[1]) for comm_card in first_three_community_cards]
    try:
        # take card out of the deck
        for comm_card in community_cards:
            card_deck.remove(comm_card)
    
    except:
        print(f'Error!! {comm_card} Card not in deck')
        quit()

    iteration = 1
    player_hand_rankings,highest_hand,two_cards = try_two_cards(players,community_cards,card_deck)
    
    while highest_hand != the_winner:
        # iterate until we get the right winner
        #print("Iteration: ",iteration)
        player_hand_rankings,highest_hand,two_cards = try_two_cards(players,community_cards,card_deck)
        iteration += 1

    if "-d" in sys.argv[1:]:
        print("\n")
        print(f"It took {iteration} iterations to find the required cards ")
        print(f'Winner: {the_winner}')
        print(f'Cards:')
        print(f'All Community cards: \t {community_cards} {two_cards}')
        print("_"*120)
        print(f'{"Player":10}|{"Card in Hand":20}|{"Hands":50}|{"Hand Type":20}|{"Hand Ranking":10}')
        print("_"*120)
        for player in player_hand_rankings.keys():
            
            print(f'{player:10}|{str(players[player]):20}|{str(player_hand_rankings[player]):10}')
        print("_"*120)
        print(f'Required Cards: {two_cards}')
        print("\n")
    return [str(card) for card in two_cards]

def main():
    two_cards = make_the_winner('players.csv', ['S2', 'C9', 'C4'], 'utur')
    #print(two_cards)

if __name__ == "__main__":
    main()