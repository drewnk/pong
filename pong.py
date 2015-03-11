# Drew Nagy-Kato

## NOTES
#   - Paddles bounded by window
#   - Improved collision detection
#   - Ball speed may be changed in-game (d, f keys)
#   - Game now displays live scoring! For both players!
#   - Now utilizes THREE colors!!


## TODO
#   + Restructure Paddle and Ball classes as Rect objects
#   - Implement dynamic bounce angles
#       - Angle changes when based on where you hit the paddle
#       - Ball respawns at a random angle moving towards
#           last point's winner.
#           + Alter ball speed changer to keep current angle
#   - Remodel with vector-based movement
#
#   - Paddle collision occasionally still sticky
#
#   Game Over:
#       - Condition/key press to end game. (first to 10?)
#       - Splash page flashing GAME OVER
#       - Declaration of winner as player1 or player2
#
#   Player Names:
#       - Ask user for names
#       - Display names alongside score


#imports the pygame library, and sys library.
import pygame, sys, random
#import all your key names
from pygame.locals import *

# dimensions of the game window
WIDTH = 1024
HEIGHT = 768
# game constants
MINBALLSPEED = 1
MAXBALLSPEED = 15
PADDLE_SPEED = 13
PADDLE_HEIGHT = 100
# vertical offset of scoreboard: %5 of total window height from top
SB_YOFFSET = HEIGHT * 0.05

class Paddle:    
    def __init__(self, x, y, paddleColor):
        self.rect = Rect(x, y, 10, PADDLE_HEIGHT)
        self.color = paddleColor
        
    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)
    def overlaps(self, otherObject):
        return otherObject.rect.colliderect(self.rect)

class Ball:
    def __init__(self, x, y, ballColor):
        #position of ball
        self.rect = Rect(x, y, 10, 10)
        self.color = ballColor
        
        #speed of ball
        self.dx = 5
        self.dy = 5
         
    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)
       
    def reset(self):
        # move ball back to center
        self.rect.move_ip(WIDTH/2 - self.rect.x, HEIGHT/2 - self.rect.y)

        # flip x-direction, generate dy randomly
        self.dx = -self.dx
        self.dy *= random.triangular(0.2, 2, 1)

class Scoreboard:
    def __init__(self, score, boardFont, scoreColor):
        #font of the scoreboard
        self.boardFont = boardFont
        #string containing the score
        self.score = score
        self.color = scoreColor

    def update(self):
        self.score = str(playerOneScore) + " - " + str(playerTwoScore)

    def draw(self, canvas):
        #(height,width) of rect needed to render string
        textBox = self.boardFont.size(self.score)
        position = ((WIDTH - textBox[0])/2, SB_YOFFSET)
        board = self.boardFont.render(self.score, 0, self.color, None)
        canvas.blit(board, Rect(position, textBox))


def main():
    #initialize the library and start a clock, just in case we want it.
    pygame.init()

    #seed the random generator
    random.seed()

    #initialize the clock that will determine how often we render a frame
    clock = pygame.time.Clock()
    done = False

    #create our canvas that will be draw on.
    resolution = (WIDTH, HEIGHT)
    canvas = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Pong 2.0')

    #Pick our background color with R,G,B values between 0 and 255
    backgroundColor = pygame.Color(0,0,0)
    greenColor = pygame.Color(0, 255, 0)
    whiteColor = pygame.Color(255, 255, 255)

    #initialize the scores of each player
    global playerOneScore
    playerOneScore = 0
    global playerTwoScore
    playerTwoScore = 0

    #prep scoreboard
    boardFont = pygame.font.Font(pygame.font.get_default_font(), 24)
    score = str(playerOneScore) + " - " + str(playerTwoScore)
    
    #create/initialize a paddle for each side
    paddle1 = Paddle(5, HEIGHT/2, greenColor)
    paddle2 = Paddle(WIDTH-15, HEIGHT/2, greenColor)

    #create a ball
    ball = Ball(WIDTH/2, HEIGHT/2, greenColor)

    #create a scoreboard
    scoreboard = Scoreboard(score, boardFont, whiteColor)
    
    #keep track of all the keys which are currently pressed
    keysPressed = []

    #for ever and ever, keep rendering a new frame of our game.
    #this is where code that needs to be run every single frame belongs
    while not done:
        #get all of our input events that have happened since the last frame
        for event in pygame.event.get():

            #deal with key presses
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                    continue
                else:
                    keysPressed.append(event.key) 
                    
            #deal with key releases
            elif event.type == KEYUP:
                keysPressed.remove(event.key)
            #deal with window closing
            elif event.type == QUIT:
                done = True
                continue
        

        #paddle physics (bound by screen)
        if K_UP in keysPressed:
            if paddle2.rect.y < 0:
                paddle2.rect.y = 0
            elif paddle2.rect.y != 0:
                paddle2.rect.y -= PADDLE_SPEED
                
        if K_DOWN in keysPressed:
            bottom = HEIGHT - paddle2.rect.height
            if paddle2.rect.y > bottom:
                paddle2.rect.y = bottom
            elif paddle2.rect.y != bottom:
                paddle2.rect.y += PADDLE_SPEED
                
        if K_a in keysPressed:
            if paddle1.rect.y < 0:
                paddle1.rect.y = 0
            elif paddle1.rect.y != 0:
                paddle1.rect.y -= PADDLE_SPEED
                
        if K_z in keysPressed:
            bottom = HEIGHT - paddle1.rect.height
            if paddle1.rect.y > bottom:
                paddle1.rect.y = bottom
            elif paddle1.rect.y != bottom:
                paddle1.rect.y += PADDLE_SPEED

        # change ball speed (without reversing direction)
        if K_f in keysPressed and abs(ball.dx) < MAXBALLSPEED:
            #increase speed
            if ball.dx > 0:
                ball.dx += 1
            else:
                ball.dx -= 1
            if ball.dy > 0:
                ball.dy += 1
            else:
                ball.dy -= 1
        if K_d in keysPressed and abs(ball.dx) > MINBALLSPEED:
            #decrease speed
            if ball.dx > 0:
                ball.dx -= 1
            else:
                ball.dx += 1
            if ball.dy > 0:
                ball.dy -= 1
            else:
                ball.dy += 1
            
        #Paddle-Ball collision
        if paddle1.overlaps(ball) or paddle2.overlaps(ball):
            ball.dx = -ball.dx
            
           
        #Wall collision - Right
        if ball.rect.x >= WIDTH:
            ball.reset()
            playerOneScore = playerOneScore + 1
            scoreboard.update()
        #Wall collision - Left
        if ball.rect.x <= 0:
            ball.reset()
            playerTwoScore = playerTwoScore + 1
            scoreboard.update()
        # Wall collision - Top/Bottom
        if ball.rect.y + ball.dy >= HEIGHT or ball.rect.y + ball.dy <= 0:
            ball.dy = -ball.dy
            
        #update ball position
        ball.rect.move_ip(ball.dx, ball.dy)
        
        #Done dealing with events, lets draw updated things on our canvas
        #fill our canvas with a background color, effectively erasing the last frame
        canvas.fill(backgroundColor)

        #draw objects on our canvas
        paddle1.draw(canvas)
        paddle2.draw(canvas)
        ball.draw(canvas)
        scoreboard.draw(canvas)
        
        #done drawing all the stuff on our canvas, now lets show it to the user
        pygame.display.update()
        #pygame.display.set_caption('Pong\t' + scoreboard.score)

        #wait the amount of time which
        clock.tick(30)

    #insert GAME OVER
    
    pygame.quit()
    return

main()
