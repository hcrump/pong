# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH /2,HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [random.randrange(2,4),-random.randrange(2,4)]
    else:
        ball_vel = [-random.randrange(2,4),-random.randrange(2,4)]
                              
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    a = random.choice([LEFT,RIGHT])
    spawn_ball(a)
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "white")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "white")
        
    # update ball
    if ball_pos[1]<=BALL_RADIUS or ball_pos[1]>=HEIGHT-BALL_RADIUS:
        #print ball_pos[1]
        ball_vel[1] *= -1
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,'white','white')
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos+paddle1_vel>=0) and (paddle1_pos+paddle1_vel<=HEIGHT-PAD_HEIGHT): 
        paddle1_pos += paddle1_vel
    if (paddle2_pos+paddle2_vel>=0) and (paddle2_pos+paddle2_vel<=HEIGHT-PAD_HEIGHT):
        paddle2_pos += paddle2_vel
    #print paddle1_pos
    
    # draw paddles
    canvas.draw_polygon([[0,paddle1_pos],
                         [PAD_WIDTH,paddle1_pos],
                         [PAD_WIDTH,paddle1_pos+PAD_HEIGHT],
                         [0,paddle1_pos+PAD_HEIGHT]],
                         1,'white','white')
    canvas.draw_polygon([[WIDTH-PAD_WIDTH,paddle2_pos],
                         [WIDTH,paddle2_pos],
                         [WIDTH,paddle2_pos+PAD_HEIGHT],
                         [WIDTH-PAD_WIDTH,paddle2_pos+PAD_HEIGHT]],
                         1,'white','white')
    
    # determine whether paddle and ball collide    
    if ball_pos[0]<=PAD_WIDTH+BALL_RADIUS:
        if ball_pos[1]<paddle1_pos or ball_pos[1]>paddle1_pos+PAD_HEIGHT:
            score2 += 1
            spawn_ball(RIGHT)
        else:
            ball_vel[0] *= -1.1
    if ball_pos[0]>=WIDTH-PAD_WIDTH-BALL_RADIUS:
        if ball_pos[1]<paddle2_pos or ball_pos[1]>paddle2_pos+PAD_HEIGHT:
            score1 += 1
            spawn_ball(LEFT)
        else: 
            ball_vel[0] *= -1.1
    # draw scores
    canvas.draw_text(str(score1),[WIDTH*.35,HEIGHT*.25],40,'white')    
    canvas.draw_text(str(score2),[WIDTH*.65,HEIGHT*.25],40,'white')   
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:       
        paddle1_vel -= 4
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 4
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += 4
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += 4
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('RESTART',restart)

# start frame
new_game()
frame.start()
