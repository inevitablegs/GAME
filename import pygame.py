import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pop the balloon")
background = pygame.image.load("Images/background.jpg")
# Background Music
mixer.music.load("Sounds/bgm.mp3")
mixer.music.play(-1)
# Time Limit
clock = pygame.time.Clock()
counter = 100
time_text = "100".rjust(3)
pygame.time.set_timer(pygame.USEREVENT,1000)
time_font = pygame.font.Font("freesansbold.ttf",16)
playerImg = pygame.image.load("Images/archery.png")
playerX = 370
playerY = 480
playerX_change = 0
# Multiple Balloons appear randomly
balloonImg = []
balloonX = []
balloonY = []
balloonX_change = []
balloonY_change = []
no_of_balloon = 7
for i in range(no_of_balloon):
    balloonImg.append(pygame.image.load("Images/balloon.png"))
    balloonX.append(random.randint(64,736))
    balloonY.append(random.randint(50,51))
    balloonX_change.append(2)
    balloonY_change.append(20)
arrowImg = pygame.image.load("Images/arrow.png") 
arrowX = 0
arrowY = 480
arrowX_change = 0
arrowY_change = 30
arrow_state = "ready"
# Score Value
score_value = 0
font = pygame.font.Font("freesansbold.ttf",16)
textX = 10
textY = 10
#game_over_text
over_font = pygame.font.Font("freesansbold.ttf",64)

#line
line = pygame.font.Font("freesansbold.ttf",8)

# High Score
high_Score = 0
hs_font = pygame.font.Font("freesansbold.ttf",16)

def limit():
    time_limit = time_font.render(time_text,True,(255,255,255))
    screen.blit(time_limit,(620,10))

def line_limit():
    line_text = line.render(("-")*1000, True, (255,255,255))
    screen.blit(line_text,(0, 250))

def game_over_text():
    over_text = over_font.render("GAME OVER !", True, (255,0,255))
    screen.blit(over_text,(200, 250))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score,(x, y))

def player(x, y):
    screen.blit(playerImg,(x, y))

def balloon(x, y, i):
    screen.blit(balloonImg[i],(x, y))

def leaveArrow(x,y):
    global arrow_state
    arrow_state = "leave"
    screen.blit(arrowImg,(x,y))
    
    
def highScore():
    Highest = hs_font.render("High Score: " + str(high_Score), True, (0,0,0),)
    screen.blit(Highest,(10, 40))
    with open("highestScore.txt","r") as f:
        return f.read()
    
try:
    high_Score = int(highScore())
except:
        high_Score = 0

def popBalloon(balloonX, balloonY, arrowX, arrowY):
    distance = math.sqrt(math.pow(balloonX-arrowX,2)+ math.pow(balloonY-arrowY,2))
    if distance < 27:
        return True
    else:
        return False
    
running = True
while running:
    screen.fill((34, 46, 32))
    screen.blit(background,(0,0))
    line_limit()
    limit()
    highScore()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            counter -= 1
            time_text = str(counter).rjust(3) if counter > 0 else "Time Over!"
        if counter <= 0:
            for k in range(no_of_balloon):
                balloonY[k] = 2000
            game_over_text()
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if arrow_state is "ready":
                    arrow_sound = mixer.Sound("Sounds/arrow.mp3")
                    arrow_sound.play()
                    arrowX = playerX
                    leaveArrow(arrowX,arrowY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
# Balloon Movement
    for i in range(no_of_balloon):
        #Game Over
        if balloonY[i] > 200:
            for j in range(no_of_balloon):
                balloonY[j] = 2000
            game_over_text()
            break
        balloonX[i] += balloonX_change[i]
        if balloonX[i] <= 0:
            balloonX_change[i] = 2
            balloonY[i] += balloonY_change[i]
        elif balloonX[i] >= 736:
            balloonX_change[i] = -2
            balloonY[i] += balloonY_change[i]

        pop = popBalloon(balloonX[i],balloonY[i],arrowX,arrowY)
        if pop:
            pop_sound = mixer.Sound("Sounds/pop.mp3")
            pop_sound.play()
            
            score_value += 5
            balloonX[i] = random.randint(0,735)
            balloonY[i] = random.randint(50,150)

        balloon(balloonX[i], balloonY[i], i) 

    if arrowY <= 0:
        arrowY = 480
        arrow_state = "ready"
    if arrow_state is "leave":
        leaveArrow(arrowX,arrowY)
        arrowY -= arrowY_change
    if (high_Score < score_value):
        high_Score = score_value
    with open("highestScore.txt","w") as f:
        f.write(str(high_Score))

    player(playerX, playerY)
    show_score(textX, textY)   
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()