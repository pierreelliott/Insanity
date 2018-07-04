import random, sys, time, pygame, simulate, bipo_main, inkspill
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 720
WINDOWHEIGHT = 480
FLASHSPEED = 500 # in milliseconds
FLASHDELAY = 200 # in milliseconds
BUTTONSIZEW = 128
BUTTONSIZEH = 48
BUTTONGAPSIZE = 30
TIMEOUT = 4 # seconds before game over if no button is pushed.


def main():

    global buttonPlay_rect, buttonQuit_rect, BASICFONT, DISPLAYWINDOW, bgColor, buttonPlay, buttonQuit

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('assets/gameicon.png'))
    DISPLAYWINDOW = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Insanity')

    # Load the sound files
    """BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')"""

    # Initialize some variables
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0
    bgColor = pygame.image.load("assets/menubackground.jpg").convert()

    # Load images of the buttons
    init_button_img()
    init_img()

    # Create buttons for the menu
    buttonPlay = pygame.image.load("assets/menubutton_play.bmp").convert_alpha()
    buttonQuit = pygame.image.load("assets/menubutton_quit.bmp").convert_alpha()

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

    isPlaying = False



    while True: # main game loop

        checkForQuit()
        if isPlaying == False:
            isPlaying = menu()

        lives = 3
        difficulty = 0
        result = 0
        gamesPlayed = []

        while isPlaying and lives > 0:
            resetGameFrame()
            checkForQuit()
            difficulty = random.randint(0,2)

            gameChoice = random.choice(('Arinoid','Tetris', 'Maze','Simulate','Inkspill'))
            if(gameChoice not in gamesPlayed):
                difficulty = 0

            print(gameChoice + ", difficulty : " + str(difficulty))
            if(gameChoice == "Simulate"):
                result = simulate.main(difficulty)
            elif(gameChoice == "Arinoid"):
                continue # Not implemented
            elif(gameChoice == "Tetris"):
                continue # Not implemented
            elif(gameChoice == "Maze"):
                result = bipo_main.main(difficulty)
            elif(gameChoice == "Inkspill"):
                result = inkspill.main(difficulty)

            gamesPlayed.append(gameChoice)

			# 'result' is either 0 (if the game has been won) or -1 (if the game has been lost)
            lives = lives + result
            score = score + result +1

            if lives > 0:
                displayScore(score,lives)
                pygame.time.wait(2000)

        isPlaying = gameOver(score)


        pygame.display.update()
        FPSCLOCK.tick(FPS)


def gameOver(score):

    gameOverAnimation()

    gameOverEndRect = gameOverEnd.get_rect()
    gameOverEndRect.center = (DISPLAYWINDOW.get_rect().center[0],DISPLAYWINDOW.get_rect().center[1]-50)
    DISPLAYWINDOW.blit(gameOverEnd, gameOverEndRect)
    pygame.display.update()
    pygame.time.wait(1000)

    resetGameFrame()
    displayScore(score, 0, 80)

    DISPLAYWINDOW.blit(imgTryAgain,buttonTryAgain_rect)
    DISPLAYWINDOW.blit(imgEndGame,buttonEndGame_rect)

    clickedButton = None

    while True:
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                buttonFocus(mousex, mousey, "gameOver")

        if clickedButton == "TryAgain":
            isPlaying = True
            return isPlaying
        elif clickedButton == "EndGame":
            isPlaying = False
            return isPlaying

    pygame.display.update()
    pygame.time.wait(5000)

    return False

def displayScore(score, lives, *pos):
    resetGameFrame()

    if lives > 0:
        scoreSurf = BASICFONT.render('Your score : ' + str(score) + ' / Your lives : ' + str(lives), 1, (255, 255, 255))
    else:
        scoreSurf = BASICFONT.render('Your score : ' + str(score), 1, (255, 255, 255))
    scoreRect = scoreSurf.get_rect()

    if len(pos) <= 0:
        scoreRect.center = DISPLAYWINDOW.get_rect().center
    elif len(pos) == 1:
        scoreRect.center = (DISPLAYWINDOW.get_rect().center[0],DISPLAYWINDOW.get_rect().center[1]-pos[0])

    DISPLAYWINDOW.blit(scoreSurf, scoreRect)
    pygame.display.update()


def menu():
    clickedButton = None
    isPlaying = False

    DISPLAYWINDOW.blit(bgColor,(0,0))
    DISPLAYWINDOW.blit(buttonPlay,(WINDOWWIDTH/2-BUTTONSIZEW/2,WINDOWHEIGHT/2-BUTTONGAPSIZE/2-BUTTONSIZEH))
    DISPLAYWINDOW.blit(buttonQuit,(WINDOWWIDTH/2-BUTTONSIZEW/2,WINDOWHEIGHT/2+BUTTONGAPSIZE/2+BUTTONSIZEH))

    buttonPlay_rect = buttonPlay.get_rect().move((WINDOWWIDTH/2-BUTTONSIZEW/2,WINDOWHEIGHT/2-BUTTONGAPSIZE/2-BUTTONSIZEH))
    buttonQuit_rect = buttonQuit.get_rect().move((WINDOWWIDTH/2-BUTTONSIZEW/2,WINDOWHEIGHT/2+BUTTONGAPSIZE/2+BUTTONSIZEH))

    pygame.display.update()

    while True:
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and isPlaying == False:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                buttonFocus(mousex, mousey, "menu")

        if clickedButton == "Play" and isPlaying == False:
            isPlaying = True
            return isPlaying
        elif clickedButton == "Quit" and isPlaying == False:
            terminate()

def buttonFocus(x, y, menu):

    if menu == "menu":
        if buttonPlay_rect.collidepoint( (x, y) ):
            DISPLAYWINDOW.blit(imgPlayF,buttonPlay_rect)
        elif buttonQuit_rect.collidepoint( (x, y) ):
            DISPLAYWINDOW.blit(imgQuitF,buttonQuit_rect)
        else:
            DISPLAYWINDOW.blit(imgPlay,buttonPlay_rect)
            DISPLAYWINDOW.blit(imgQuit,buttonQuit_rect)
    elif menu == "gameOver":
        if buttonTryAgain_rect.collidepoint( (x, y) ):
            DISPLAYWINDOW.blit(imgTryAgainF,buttonTryAgain_rect)
        elif buttonEndGame_rect.collidepoint( (x, y) ):
            DISPLAYWINDOW.blit(imgEndGameF,buttonEndGame_rect)
        else:
            DISPLAYWINDOW.blit(imgTryAgain,buttonTryAgain_rect)
            DISPLAYWINDOW.blit(imgEndGame,buttonEndGame_rect)

    pygame.display.update()

def getButtonClicked(x, y):
    if buttonPlay_rect.collidepoint( (x, y) ):
        return "Play"
    elif buttonQuit_rect.collidepoint( (x, y) ):
        return "Quit"
    elif buttonTryAgain_rect.collidepoint( (x, y) ):
        return "TryAgain"
    elif buttonEndGame_rect.collidepoint( (x, y) ):
        return "EndGame"
    return None

def resetGameFrame():
    DISPLAYWINDOW.fill((0,0,0))

def gameOverAnimation():
    resetGameFrame()

    gameOverBgRect = gameOverBackground.get_rect()
    gameOverBgRect.center = DISPLAYWINDOW.get_rect().center
    DISPLAYWINDOW.blit(gameOverBackground, gameOverBgRect)

    gameOverImages = [gameOver1,gameOver2,gameOver3,gameOver4,gameOver5,gameOver4,gameOver6,gameOver4,gameOver3,gameOver2,gameOver1]
    for gameOverSurf in gameOverImages:
        resetGameFrame()
        DISPLAYWINDOW.blit(gameOverBackground, gameOverBgRect)

        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.center = DISPLAYWINDOW.get_rect().center
        DISPLAYWINDOW.blit(gameOverSurf, gameOverRect)
        pygame.display.update()
        pygame.time.wait(200)

    # Trying to make the "Game Over" text appear smoothly
    """for i in 1..255:
        gameOverEndRect = gameOverEnd.get_rect()
        gameOverEndRect.center = (DISPLAYWINDOW.get_rect().center[0],DISPLAYWINDOW.get_rect().center[1]-50)
        DISPLAYWINDOW.blit(gameOverEnd, gameOverEndRect)
        pygame.display.update()"""

def init_button_img():
    global imgPlay, imgPlayF, imgQuit, imgQuitF, imgTryAgain, imgTryAgainF, imgEndGame, imgEndGameF
    global buttonPlay_rect, buttonQuit_rect, buttonTryAgain_rect, buttonEndGame_rect

    imgPlay = pygame.image.load("assets/menubutton_play.bmp").convert_alpha()
    imgPlayF = pygame.image.load("assets/menubutton_playF.bmp").convert_alpha()
    imgQuit = pygame.image.load("assets/menubutton_quit.bmp").convert_alpha()
    imgQuitF = pygame.image.load("assets/menubutton_quitF.bmp").convert_alpha()
    imgTryAgain = pygame.image.load("assets/menubutton_tryagain.bmp").convert_alpha()
    imgTryAgainF = pygame.image.load("assets/menubutton_tryagainF.bmp").convert_alpha()
    imgEndGame = pygame.image.load("assets/menubutton_endgame.bmp").convert_alpha()
    imgEndGameF = pygame.image.load("assets/menubutton_endgameF.bmp").convert_alpha()

    buttonPlay_rect = imgPlay.get_rect().move((WINDOWWIDTH/2-BUTTONSIZEW/2,WINDOWHEIGHT/2-BUTTONGAPSIZE/2-BUTTONSIZEH))
    buttonQuit_rect = imgQuit.get_rect().move((WINDOWWIDTH/2-BUTTONSIZEW/2,WINDOWHEIGHT/2+BUTTONGAPSIZE/2+BUTTONSIZEH))
    buttonTryAgain_rect = imgTryAgain.get_rect().move((DISPLAYWINDOW.get_rect().center[0]-(BUTTONGAPSIZE+BUTTONSIZEW/2),DISPLAYWINDOW.get_rect().center[1]))
    buttonEndGame_rect = imgEndGame.get_rect().move((DISPLAYWINDOW.get_rect().center[0]+BUTTONGAPSIZE+BUTTONSIZEW/2,DISPLAYWINDOW.get_rect().center[1]))


def init_img():
    global gameOver1, gameOver2, gameOver3, gameOver4, gameOver5, gameOver6, gameOverEnd, gameOverBackground

    gameOver1 = pygame.image.load("assets/gameOver1.png").convert_alpha()
    gameOver2 = pygame.image.load("assets/gameOver2.png").convert_alpha()
    gameOver3 = pygame.image.load("assets/gameOver3.png").convert_alpha()
    gameOver4 = pygame.image.load("assets/gameOver4.png").convert_alpha()
    gameOver5 = pygame.image.load("assets/gameOver5.png").convert_alpha()
    gameOver6 = pygame.image.load("assets/gameOver6.png").convert_alpha()
    gameOverEnd = pygame.image.load("assets/gameOverEnd.png").convert_alpha()
    gameOverBackground = pygame.image.load("assets/gameOverBackground.png").convert_alpha()

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


if __name__ == '__main__':
    main()
