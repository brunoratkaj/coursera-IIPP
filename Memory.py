# implementation of card game - Memory

# FOR SOME REASON IF YOU START THE GAME, CHANGE THE TAB (FOR EXAMPLE GO BACK TO OLD WINDOW), 
# AND RETURN TO THE OPENED WINDOW OF THE GAME, IT WON'T REACT ON CLICKS (I'M USING CHROME).
# SO IF YOU PLAY THE GAME WITHOUT CLICKING OUT OF IT'S WINDOW IN BROWSER IT WILL WORK

import simplegui
import random

# create list of cards with doubles of numbers 0 to 7
cards = range(0,8) + range(0,8)


# helper function to initialize globals
def new_game():
    # list exsposed
    global exposed  
    exposed = [False] * 16
    # list of cards that is exact copy of starting card list
    global card_list
    card_list = cards
    # shuffling the cards
    random.shuffle(card_list)
    # variable state for later determination of flipped cards
    global state
    state = 0
    # variable Turns for counting turns
    global Turns
    Turns = 0
    label.set_text("Turns = "+ str(Turns))
    
    
# define event handlers
def mouseclick(pos):
    global card_index
    # determining what card is clicked
    card_index = pos[0] // 50
    global card_one
    global card_two
    global state
    global Turns
    # first click
    if state == 0:
        global first_index
        # zero_index will be used once, index of the first clicked card
        first_index = card_index
        # save the value of that card
        card_one = card_list[first_index]
        # signify what card will be/is flipped over
        exposed[first_index] = True
        state = 1
        
    elif state == 1:
        if not exposed[card_index]:         
            #flip over card that was clicked second
            global second_index
            # saving that index so I can use it later
            second_index = card_index
            # saving value of that card
            card_two = card_list[second_index]
            # notice that card can be/is flipped over
            exposed[second_index] = True
            state = 2
            # increment Turns
            Turns += 1
            label.set_text("Turns = "+ str(Turns))
    else:
        if not exposed[card_index]:
            #if the cards are the same, remain to be flipped over
            if card_one == card_two:
                exposed[first_index] = True
                exposed[second_index] = True
            # or not
            else:
                exposed[first_index] = False
                exposed[second_index] = False
            state = 1  
            # flip over the clicked card
            first_index = card_index
            card_one = card_list[first_index]
            exposed[first_index] = True

def draw(canvas):
        for card_indx in range(len(card_list)):
            card_pos = 50 * card_indx
            if exposed[card_indx] == True:
                canvas.draw_text(str(card_list[card_indx]), [card_pos + 15, 60], 40, 'White')
            else:
                canvas.draw_polygon([(card_pos, 0), (card_pos, 100), (card_pos + 47, 100),(card_pos + 47, 0)], 1, 'Green', 'Green')
           
            
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = ")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
