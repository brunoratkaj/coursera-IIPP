#"Stopwatch: The Game"

import simplegui

# define global variables
time = 0
stopwatch = '0:00.0'
numstops = 0
numwholesec = 0
milseconds = 0
isrunning = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global stopwatch, milseconds 
    minutes = t / 600
    tensseconds = ((t / 10) % 60) / 10
    seconds = ((t / 10) % 60) % 10
    milseconds = t % 10
    stopwatch = str(minutes) + ':' + str (tensseconds) + str(seconds) + '.' + str(milseconds)    

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()
    
def stop_handler():
    global numstops, numwholesec, isrunning
    timer.stop()
    if isrunning:
        numstops += 1
    if milseconds == 0 and isrunning:
        numwholesec += 1
    isrunning = False    
    
def reset_handler():
    global time, stopwatch, numstops, numwholesec, isrunning

    timer.stop()
    time = 0
    numstops = 0
    numwholesec = 0
    isrunning = False
    stopwatch = '0:00.0'
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time, isrunning
    isrunning = True
    time += 1
    format(time)
    
# define draw handler
def draw_handler(canvas):
    canvas.draw_text(stopwatch, (100, 110), 45, 'White')
    canvas.draw_text(str(numwholesec) + '/' + str(numstops), (250, 30), 28, 'Yellow')
    
# create frame
frame = simplegui.create_frame('Stop watch', 300, 200, 100)
frame.set_canvas_background('Black')

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
start = frame.add_button('Start', start_handler, 100)
stop = frame.add_button('Stop', stop_handler, 100)
reset = frame.add_button('Reset', reset_handler, 100)

# start frame
frame.start()
