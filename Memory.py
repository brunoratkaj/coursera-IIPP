# implementation of card game - Memory

import simplegui
import random

cards =[i for i in range(0,8)]
cards.extend([i for i in range(0,8)])

# helper function to initialize globals
def new_game():
    global state, cards, exposed, turn
    random.shuffle(cards)
    turn = 0
    state = 0
    cards_clicked = []
    exposed = [False for i in range(16)]
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, card1, card2, turn
    card_clicked = list(pos)[0] / 50
    if state == 0:
        state = 1
        card1 = card_clicked
        exposed[card_clicked] = True
    elif state == 1:
        if not exposed[card_clicked]:
            card2 = card_clicked
            if card2 != card1:
                state = 2
                exposed[card_clicked] = True
                turn += 1
    else:
        if not exposed[card_clicked]:
            state = 1
            exposed[card_clicked] = True            
            if cards[card1] != cards[card2]:
                exposed[card1] = False
                exposed[card2] = False
            card1 = card_clicked
            
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card_ind in range(len(cards)):
        if exposed[card_ind]:
            canvas.draw_text(str(cards[card_ind]), (10 + card_ind * 50, 75), 70, "White")
        else:
            canvas.draw_polygon([[card_ind*50, 0], [card_ind*50 + 50, 0], [card_ind*50 + 50, 100],
                                 [card_ind*50, 100]], 1, "Black", "Green")
    label.set_text("Turns: " + str(turn))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns: 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
