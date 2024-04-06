import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class Deck:
    def __init__(self, num_decks, shuffle_threshold):
        self.num_decks = num_decks
        self.shuffle_threshold = shuffle_threshold
        self.cards = self.generate_deck()

    def generate_deck(self):
        cards = []
        for _ in range(self.num_decks):
            for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
                for value in range(2, 11):
                    cards.append(Card(suit, str(value)))
                for face in ['Jack', 'Queen', 'King', 'Ace']:
                    cards.append(Card(suit, face))
        random.shuffle(cards)
        return cards

    def deal_card(self):
        if len(self.cards) < self.shuffle_threshold:
            print("Deck is running low. Reshuffling.")
            self.cards = self.generate_deck()
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def get_hand_value(self):
        value = 0
        num_aces = 0
        for card in self.hand:
            if card.value.isdigit():
                value += int(card.value)
            elif card.value in ['Jack', 'Queen', 'King']:
                value += 10
            else:
                num_aces += 1
                value += 11
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

def perfect_strategy(player_hand_value, dealer_upcard_value):
    # Based on the perfect strategy, determine whether to hit or stand
    if player_hand_value >= 17:
        return 's'  # Stand
    elif player_hand_value <= 11:
        return 'h'  # Hit
    elif player_hand_value == 12:
        return 's' if dealer_upcard_value >= 4 and dealer_upcard_value <= 6 else 'h'
    elif player_hand_value >= 13 and player_hand_value <= 16:
        return 's' if dealer_upcard_value >= 2 and dealer_upcard_value <= 6 else 'h'

def play_game(num_decks, num_hands, shuffle_threshold):
    wins = 0
    for _ in range(num_hands):
        deck = Deck(num_decks, shuffle_threshold)
        player = Player("Player")
        dealer = Player("Dealer")
        
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())

        while True:
            choice = perfect_strategy(player.get_hand_value(), int(dealer.hand[1].value) if dealer.hand[1].value.isdigit() else 10)
            if choice == 'h':
                player.add_card(deck.deal_card())
                if player.get_hand_value() > 21:
                    break
            elif choice == 's':
                break
        
        if player.get_hand_value() <= 21:
            while dealer.get_hand_value() < 17:
                dealer.add_card(deck.deal_card())
            if dealer.get_hand_value() > 21 or dealer.get_hand_value() < player.get_hand_value():
                wins += 1
    return wins

def main():
    num_decks = int(input("Enter the number of decks: "))
    num_hands = int(input("Enter the number of hands to play: "))
    shuffle_threshold = int(input("Enter the shuffle threshold: "))

    wins = play_game(num_decks, num_hands, shuffle_threshold)
    win_percentage = (wins / num_hands) * 100
    print(f"\nWin percentage over {num_hands} hands: {win_percentage:.2f}%")

if __name__ == "__main__":
    main()
