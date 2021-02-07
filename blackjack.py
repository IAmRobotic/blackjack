from random import shuffle

keys = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']  # note: does not include Ace!
values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # note: does not include Ace!
CARD_VALUES = dict(zip(keys, values))

SUITS = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

SUIT_SYMBOLS = {
    'Spades': u'♠',
    'Diamonds': u'♦',
    'Clubs': u'♣',
    'Hearts': u'♥',
    }


class CommunityCards:

    def __init__(self, num_decks: int = 1):
        self.num_decks = num_decks
        self._pile = self.shuffle_decks()

    def __repr__(self):
        return f"""
        Community card pile object initiated with {self.num_decks} decks.\
        Currently has {len(self._pile)} cards left.
        """

    def __len__(self):
        return len(self._pile)

    def shuffle_decks(self):
        pile = []
        base_deck = [(card, suit) for suit in SUITS for card in VALUES]
        for i in range(self.num_decks):
            pile += base_deck
        shuffle(pile)
        return pile

    def deal(self, num_cards: int = 1):
        deal_list = []
        for i in range(num_cards):
            deal_list.append(self._pile.pop())
        return tuple(deal_list)


class Hand:
    valid_player_types = ("player", "computer", "dealer")

    def __init__(self, player_type: str = "player"):
        """
        Player type must be 'player' (the human), 'dealer' or 'computer'
        This could help determine whether program displays some cards as
        face down or face up.
        """

        self.player_type = player_type.lower()
        self._cards = ()  # empty tuple
        self._score = 0
        self._initial_deal = True  # only used if player_type is 'dealer'

        if self.player_type not in self.valid_player_types:
            raise Exception("Player type must be 'player', 'dealer' or 'computer'")

    def __repr__(self):
        return f"""Card hand object initiated for the {self.player_type.upper()} player.\
        Currently holding {len(self._cards)} cards. """

    def __str__(self):

        player_type = self.player_type.capitalize()
        cards = ""
        msg = ""

        if (self.player_type == 'dealer') and self._initial_deal and (len(self._cards) == 2):
            cards += self._cards[0][0] + SUIT_SYMBOLS[self._cards[0][1]]
            cards += " \U0001F0A0"  # second card for dealer shown face down until player finishes
            return f"{player_type}: {cards}"

        else:
            for card in self._cards:
                cards += card[0] + SUIT_SYMBOLS[card[1]] + " "
            if self._score > 21:
                msg = "***BUST!***"
            elif self._score == 21:
                msg = "***BLACKJACK!!***"

            return f"{player_type}: {cards} | Score: {self._score} {msg}"

    def calculate_score(self):

        score = 0
        num_aces = 0

        for card, suit in self._cards:
            if 'A' in card:
                num_aces += 1
            else:
                score += CARD_VALUES[card]

        if num_aces > 0:
            if score >= 11:
                score += (1 * num_aces)
            else:
                score += 11 + (1 * (num_aces - 1))

        return score

    def draw(self, deck_object, num_cards: int = 1):
        self._cards += deck_object.deal(num_cards)
        self._score = self.calculate_score()


def initial_deal(deck_object, dealer, *players):
    """
    Deals two cards to each player, including the dealer
    """
    for i in range(2):
        for player in players:
            player.draw(deck_object)
        dealer.draw(deck_object)


def main(num_decks = 6):
    valid_inputs = ('h', 's')
    deck = CommunityCards(num_decks)
    player = Hand()
    dealer = Hand('dealer')
    initial_deal(deck, dealer, player)

    print(dealer)
    print(player, '\n')

    if player._score < 21: # player's turn
        active_turn = True
        while player._score < 21 and active_turn:
            invalid_input = True
            while invalid_input:
                hit_or_stand = input("Do you want to H)it or S)tand? -> ").lower()
                if hit_or_stand in valid_inputs:
                    invalid_input = False
                else:
                    print("Please enter 'H' for another card or 'S' to end turn")

            if hit_or_stand == 'h':
                player.draw(deck, 1)
                print(player, '\n')
            else:
                active_turn = False

    if player._score < 22: # dealer's turn
        dealer._initial_deal = False
        print('\n',dealer)
        while dealer._score < 17:
            print("***Dealer draws a card***")
            dealer.draw(deck, 1)
            print(dealer, '\n')

    dealer._initial_deal = False
    print("\nFinal hands:")
    print(dealer)
    print(player, '\n')

    if (22 > player._score > dealer._score) or ((dealer._score > 21) and (player._score < 22)):
        print("!!!You win!!!")
    elif (22 > dealer._score > player._score) or ((player._score > 21) and (dealer._score < 22)):
        print("Dealer wins, you lose :(")
    else:
        print("Tie")

main()