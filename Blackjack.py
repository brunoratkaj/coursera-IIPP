# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
action = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
    # create Hand object

    def __str__(self):
        in_hand = ''
        for card in self.hand:             
            in_hand += card.get_suit() + '' + card.get_rank() + ' ' 
        return 'hand contains ' + in_hand
    # return a string representation of a hand
    
    def add_card(self, card):
        self.hand.append(card)
    # add a card object to a hand

    def get_value(self):
        hand_value = 0
        cards_in_hand = []
        
        # sum the values of cards in hand
        for card in self.hand:
            cards_in_hand.append(card.get_rank())	
            value = VALUES.get(card.get_rank())
            hand_value += value
        
        if 'A' not in cards_in_hand:
            return hand_value
        else:
            if (hand_value + 10) <= 21:
                return hand_value + 10
            else:
                return hand_value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.hand:
            card_loc = (pos[0] + i * CARD_SIZE[0], pos[1])
            card.draw(canvas, card_loc)
            i += 1
        # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank)) 

    def shuffle(self):
        random.shuffle(self.deck)
            # use random.shuffle()

    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card
        # deal a card object from the deck
    
    def __str__(self):
        in_deck = ''
        for card in self.deck:             
            in_deck += card.get_suit() + '' + card.get_rank() + ' ' 
        return 'Deck contains ' + in_deck
        # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, action, score, deal_clicked
    deal_clicked = False	
    outcome = ''
    
    # if deal is clicked player lose 
    if in_play:
        deal_clicked = True
        outcome = 'You lose'
        score -= 1
        in_play = False
    else:
        action = 'Hit or stand?' 
        #create a deck and shuffle it
        deck = Deck()
        deck.shuffle()
        #create player's and dealer's hand
        player = Hand()
        dealer = Hand()
        #add two cards to the player's hand
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        #add two cards to the dealer's hand
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        #player's turn to choose
        in_play = True

def hit():
    global deck, player, dealer, action, outcome, in_play, score
    
    #condition that prevents adding score or hiting 
    #when deal is clicked in the middle of the game
    if not deal_clicked:
        #add card to the player's hand if the sum of card values is 
        #less than 21 and player's turn
        if player.get_value() <= 21 and in_play:
            player.add_card(deck.deal_card())
            # if the sum of card values after the hit is greater than 21 player loses
            if player.get_value() > 21:
                action = 'New deal?'
                outcome = 'You lose'
                in_play = False
                score -= 1

def stand():
    global deck, player, dealer, action, in_play, outcome,score
    #condition that prevents adding score  
    #when deal is clicked in the middle of the game
    if not deal_clicked:
        in_play = False

        if player.get_value() > 21:
            action = 'New deal?'
            outcome = 'You lose'
        else:
            #condition that prevents adding score  
            #when the game is done
            if not outcome:
                #deal the cards until the sum of the cards in dealer's hand 
                #is greater than 17
                while dealer.get_value() < 17:
                    dealer.add_card(deck.deal_card())

                #if the sum of the cards in dealer's hand is greater than 21
                #player wins
                if dealer.get_value() > 21 :
                    outcome = 'You win'
                    action = 'New deal?'
                    score += 1
                else:
                    #if the sum of the cards in dealer's hand is greater than 
                    #the sum of the cards in player's hand dealer wins
                    if dealer.get_value() >= player.get_value():
                        outcome = 'You lose'
                        action = 'New deal?'
                        score -= 1
                    else:
                        outcome = 'You win'
                        action = 'New deal?'
                        score += 1

# draw handler    
def draw(canvas):
    
    global deck, player, dealer, action, in_play, outcome, score
    
    canvas.draw_text("Blackjack", (20, 60), 45, 'Orange')
    
    canvas.draw_text('Score: ' + str(score), (325, 60), 45, 'Black')
    
    canvas.draw_text(action, (325, 160), 40, 'Purple')
    
    canvas.draw_text("Player's hand:", (20, 160), 45, 'Black')
    
    player.draw(canvas,[150, 200])
    
    canvas.draw_text(outcome, (325, 410), 40, 'Purple')
    
    canvas.draw_text("Dealer's hand:", (20, 410), 45, 'Black')
    
    #if it is player's turn hide dealers hole card
    if in_play == True:        
        dealer.draw(canvas,[150, 450])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [150 + CARD_BACK_CENTER[0], 450 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)  
    else:
        dealer.draw(canvas,[150, 450])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


deal()
frame.start()
