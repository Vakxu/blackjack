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
result = ""
score = 0

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
        self.contents = []

    def __str__(self):
        s = "Hand contains"
        for card in self.contents:
            s += " " + str(card)
        return s

    def add_card(self, card):
        self.contents.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        has_ace = False
        for card in self.contents:
            rank = card.get_rank()
            value += VALUES[rank]
            if rank == 'A': has_ace = True
        
        if has_ace and value + 10 <= 21: value += 10
        return value
   
    def draw(self, canvas, pos):
        drawpos = list(pos)
        for card in self.contents:
            card.draw(canvas, drawpos)
            drawpos[0] += 75
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [(Card(s, r))for s in SUITS for r in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        s = "Deck contains"
        for card in self.deck:
            s += " " + str(card)
        return s



#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck, dealer, player, result, score
    if in_play:
        result = "you forfeited the last round"
        score -= 1
    else:
        result = ""
    
    in_play = True
    deck = Deck()
    deck.shuffle()
    dealer, player = Hand(), Hand()
    
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())

    outcome = "Hit or stand?"


def hit():
    global in_play, outcome, result, score
    # replace with your code below
 
    # if the hand is in play, hit the player
    # Here we exit this funtion if the hand is not in play -> nothing happens
    if not in_play: return
    
    # If we come here we are still in play! :)
    
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())

    if player.get_value() > 21:
        result = 'You busted and lost the hand'
        score -= 1
        in_play = False
        stand()
       
def stand():
    # replace with your code below
    global in_play, score, result, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    if in_play:
        # Expose the dealer's first card
        in_play = False
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        
        if dealer.get_value() > 21:
            result = 'Dealer busted, you WON!'
            score += 1
        elif player.get_value() <= dealer.get_value():
            result = 'Dealer won'
            score -= 1
        else:
            result = 'You WIN'
            score += 1
        
    outcome = 'New deal?'    
    #print 'dealer', str(dealer), "=", dealer.get_value()
    #print 'player', str(player), '=', player.get_value()
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    #Cards cordinates
    dealer_pos = (40, 150)
    player_pos = (40, 290)
    
    canvas.draw_text('Coursera Blackjack', (5, 40), 48, 'White')
    canvas.draw_text('Score ' + str(score), (15, 80), 24, 'White')
    
    canvas.draw_text('Dealer hand', (40, 140), 24, 'White')
    canvas.draw_text(result, (220, 140), 24, 'White')
    
    dealer.draw(canvas, dealer_pos)
    
    # Hide dealer's first card
    if in_play:
        canvas.draw_image(card_back, 
                      (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0], CARD_BACK_CENTER[1]), 
                      CARD_BACK_SIZE, 
                      [dealer_pos[0] + CARD_BACK_CENTER[0], dealer_pos[1] + CARD_BACK_CENTER[1]], 
                      CARD_BACK_SIZE)
    else:
        canvas.draw_text('Dealer has ' + str(dealer.get_value()), (40, 420), 24, 'White')
        canvas.draw_text('Player has ' + str(player.get_value()), (40, 445), 24, 'White')
    
    canvas.draw_text('Player hand', (40, 280), 24, 'White')
    canvas.draw_text(outcome, (220, 280), 24, 'White')
    
    player.draw(canvas, player_pos)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 480)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
