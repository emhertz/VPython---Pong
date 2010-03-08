from visual import *
from visual.controls import *

#Constants for the computer's paddle motion
COMP_VELOCITY = 10
V_CONST = 0.005

#Creates the graphical objects
human = box( pos = (-4, 0, 0), size = (0.2, 2, 3), color = color.white)
computer = box( pos = (4, 0, 0), size = (0.2, 2, 3), color = color.white)

wallL = box( pos = (-5, 0, 0), size = (0.2, 8, 7), color = color.blue)
wallR = box( pos = (5, 0, 0), size = (0.2, 8, 7), color = color.blue)
wallT = box( pos = (0, 4, 0), size = (10, 0.2, 7), color = color.blue)
wallB = box( pos = (0, -4, 0), size = (10, 0.2, 7), color = color.blue)

ball = sphere( pos = (-3, 0, 0), radius = 0.2, color = color.green)

#Sets up other gameplay constants
dt = 0
inc = 1
vscale = 0.005
playerScore = 0
computerScore = 0
targetScore = 21

gameStart = False
gameFinished = False

#Function returns true if ball hit either paddle, false otherwise
def hitPaddle(direction):
    if direction > 0 and \
    ball.pos.x + ball.radius >= computer.pos.x - computer.size.x and \
    ball.pos.y <= computer.pos.y + (computer.size.y / 2) and \
    ball.pos.y >= computer.pos.y - (computer.size.y / 2):
        return true
    if direction < 0 and \
    ball.pos.x - ball.radius < human.pos.x + human.size.x and \
    ball.pos.y <= human.pos.y + (human.size.y / 2) and \
    ball.pos.y >= human.pos.y - (human.size.y / 2):
        return true
    return false

#Function returns 1 if passed the computer paddle, -1 if passed the
#human's paddle. Otherwise it returns 0.
def passedPaddle(direction):
    if direction >= 0 and \
    ball.pos.x + ball.radius >= computer.pos.x - computer.size.x and \
    (ball.pos.y >= computer.pos.y + (computer.size.y / 2) or \
    ball.pos.y <= computer.pos.y - (computer.size.y / 2)):
        return 1
    if direction < 0 and \
    ball.pos.x - ball.radius < human.pos.x + human.size.x and \
    (ball.pos.y >= human.pos.y + (human.size.y / 2) or \
    ball.pos.y <= human.pos.y - (human.size.y / 2)):
        return -1
    return 0

#Pre-game set-up routine
while gameStart == False:
    rate(100)
    if scene.mouse.pos.y - (human.size.y / 2) > wallB.pos.y + wallB.size.y and \
    scene.mouse.pos.y + (human.size.y / 2) < wallT.pos.y - wallT.size.y:
        human.pos.y = scene.mouse.pos.y
        ball.pos.y = scene.mouse.pos.y
    if scene.mouse.clicked:
        ball.velocity = vector(10, 5, 0)
        gameStart = True

#Game main loop - updates the position of the ball and records score
while gameFinished == False:
    rate(100)
    if scene.mouse.pos.y - (human.size.y / 2) > wallB.pos.y + wallB.size.y and \
    scene.mouse.pos.y + (human.size.y / 2) < wallT.pos.y - wallT.size.y:
        human.pos.y = scene.mouse.pos.y
    if ball.pos.y > computer.pos.y and  ball.velocity.x > 0:
        computer.pos.y = computer.pos.y + COMP_VELOCITY * V_CONST
    elif ball.pos.y < computer.pos.y and ball.velocity.x > 0:
        computer.pos.y = computer.pos.y - COMP_VELOCITY * V_CONST
    if hitPaddle(ball.velocity.x):
        ball.velocity.x = -ball.velocity.x
        ball.velocity += (ball.velocity*0.01)
    if ball.pos.y + ball.radius > wallT.pos.y - wallT.size.y or \
    ball.pos.y - ball.radius < wallB.pos.y + wallB.size.y:
        ball.velocity.y = -ball.velocity.y
    if passedPaddle(ball.velocity.x) == 1 and ball.velocity.x > 0:
        playerScore += 1
        if playerScore >= targetScore:
            gameFinished = True
            print "You win!"
    elif passedPaddle(ball.velocity.x) == -1 and ball.velocity.x < 0:
        computerScore += 1
        if computerScore >= targetScore:
            gameFinished = True
            print "You lose!"
    ball.pos = ball.pos + ball.velocity * vscale
