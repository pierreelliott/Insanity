# Ink Spill (a Flood It clone)
# http://inventwithpython.com/pygame
# By Al Sweigart al@inventwithpython.com
# Released under a "Simplified BSD" license

import random, sys, webbrowser, copy, pygame
from pygame.locals import *
import time;

# There are different box sizes, number of boxes, and
# life depending on the "board size" setting selected.
SMALLBOXSIZE  = 80 # size is in pixels
MEDIUMBOXSIZE = 40
LARGEBOXSIZE  = 20

SMALLBOARDSIZE  = 4 # size is in boxes
MEDIUMBOARDSIZE = 8
LARGEBOARDSIZE  = 12

SMALLMAXLIFE  = 10 # number of turns
MEDIUMMAXLIFE = 20
LARGEMAXLIFE  = 40

FPS = 30
WINDOWWIDTH = 720
WINDOWHEIGHT = 480
boxSize = SMALLBOXSIZE
PALETTEGAPSIZE = 10
PALETTESIZE = 45
EASY = 0   # arbitrary but unique value
MEDIUM = 1 # arbitrary but unique value
HARD = 2   # arbitrary but unique value

difficulty = EASY # game starts in "easy" mode
maxLife = SMALLMAXLIFE
boardWidth = SMALLBOARDSIZE
boardHeight = SMALLBOARDSIZE


#            R    G    B
WHITE    = (255, 255, 255)
DARKGRAY = ( 70,  70,  70)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)

# The first color in each scheme is the background color, the next six are the palette colors.
COLORSCHEMES = (((150, 200, 255), RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE),
                ((0, 155, 104),  (97, 215, 164),  (228, 0, 69),  (0, 125, 50),   (204, 246, 0),   (148, 0, 45),    (241, 109, 149)),
                ((195, 179, 0),  (255, 239, 115), (255, 226, 0), (147, 3, 167),  (24, 38, 176),   (166, 147, 0),   (197, 97, 211)),
                ((85, 0, 0),     (155, 39, 102),  (0, 201, 13),  (255, 118, 0),  (206, 0, 113),   (0, 130, 9),     (255, 180, 115)),
                ((191, 159, 64), (183, 182, 208), (4, 31, 183),  (167, 184, 45), (122, 128, 212), (37, 204, 7),    (88, 155, 213)),
                ((200, 33, 205), (116, 252, 185), (68, 56, 56),  (52, 238, 83),  (23, 149, 195),  (222, 157, 227), (212, 86, 185)))
for i in range(len(COLORSCHEMES)):
    assert len(COLORSCHEMES[i]) == 7, 'Color scheme %s does not have exactly 7 colors.' % (i)
bgColor = COLORSCHEMES[0][0]
paletteColors =  COLORSCHEMES[0][1:]

def main(diffic):
    global FPSCLOCK, DISPLAYSURF

    if diffic == 0:
        difficulty = EASY
        maxLife = SMALLMAXLIFE
        boxSize = SMALLBOXSIZE
        boardWidth = SMALLBOARDSIZE
        boardHeight = SMALLBOARDSIZE
        time_limit = 20
    elif diffic == 1:
        difficulty = MEDIUM
        maxLife = MEDIUMMAXLIFE
        boxSize = MEDIUMBOXSIZE
        boardWidth = MEDIUMBOARDSIZE
        boardHeight = MEDIUMBOARDSIZE
        time_limit = 40
    elif diffic == 2:
        difficulty = HARD
        maxLife = LARGEMAXLIFE
        boxSize = LARGEBOXSIZE
        boardWidth = LARGEBOARDSIZE
        boardHeight = LARGEBOARDSIZE
        time_limit = 50
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    mousex = 0
    mousey = 0
    mainBoard = generateRandomBoard(boardWidth, boardHeight, difficulty)
    life = maxLife
    lastPaletteClicked = None

    first_time = time.time()
    myfont = pygame.font.SysFont("monospace", 15)

    while True: # main game loop
        current_time = time.time()
        
        paletteClicked = None
        resetGame = False

        # Draw the screen.
        DISPLAYSURF.fill(bgColor)
        #drawLogoAndButtons()
        drawBoard(mainBoard, boardWidth, boardHeight, boxSize)
        drawLifeMeter(life, maxLife)
        drawPalettes()

        time_play = int(current_time - first_time)
        label = myfont.render(str(time_limit - time_play), 1, (0,0,0))
        DISPLAYSURF.blit(label, (200, 0))

        if time_play >= time_limit:
            return -1

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # check if a palette button was clicked
                paletteClicked = getColorOfPaletteAt(mousex, mousey)
            elif event.type == KEYDOWN:
                # support up to 9 palette keys
                try:
                    key = int(event.unicode)
                except:
                    key = None

                if key != None and key > 0 and key <= len(paletteColors):
                    paletteClicked = key - 1

        if paletteClicked != None and paletteClicked != lastPaletteClicked:
            # a palette button was clicked that is different from the
            # last palette button clicked (this check prevents the player
            # from accidentally clicking the same palette twice)
            lastPaletteClicked = paletteClicked
            floodAnimation(mainBoard, boardWidth, boardHeight, boxSize, paletteClicked)
            life -= 1

            resetGame = False
            if hasWon(mainBoard, boardWidth, boardHeight):
                return 0
        if life == 0:
            return -1
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def checkForQuit():
    # Terminates the program if there are any QUIT or escape key events.
    for event in pygame.event.get(QUIT): # get all the QUIT events
        pygame.quit() # terminate if any QUIT events are present
        sys.exit()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit() # terminate if the KEYUP event was for the Esc key
            sys.exit()
        pygame.event.post(event) # put the other KEYUP event objects back


def hasWon(board, boardWidth, boardHeight):
    # if the entire board is the same color, player has won
    for x in range(boardWidth):
        for y in range(boardHeight):
            if board[x][y] != board[0][0]:
                return False # found a different color, player has not won
    return True








def floodAnimation(board, boardWidth, boardHeight, boxSize, paletteClicked, animationSpeed=254):
    origBoard = copy.deepcopy(board)
    floodFill(board, boardWidth, boardHeight, board[0][0], paletteClicked, 0, 0)


    drawBoard(origBoard, boardWidth, boardHeight, boxSize)
    drawBoard(board, boardWidth, boardHeight, boxSize)
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def generateRandomBoard(width, height, difficulty):
    # Creates a board data structure with random colors for each box.
    board = []
    for x in range(width):
        column = []
        for y in range(height):
            column.append(random.randint(0, len(paletteColors) - 1))
        board.append(column)

    # Make board easier by setting some boxes to same color as a neighbor.

    # Determine how many boxes to change.
    if difficulty == EASY:
        if boxSize == SMALLBOXSIZE:
            boxesToChange = 100
        else:
            boxesToChange = 1500
    elif difficulty == MEDIUM:
        if boxSize == SMALLBOXSIZE:
            boxesToChange = 5
        else:
            boxesToChange = 200
    else:
        boxesToChange = 0

    # Change neighbor's colors:
    for i in range(boxesToChange):
        # Randomly choose a box whose color to copy
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)

        # Randomly choose neighbors to change.
        direction = random.randint(0, 3)
        if direction == 0: # change left and up neighbor
            board[x-1][y] == board[x][y]
            board[x][y-1] == board[x][y]
        elif direction == 1: # change right and down neighbor
            board[x+1][y] == board[x][y]
            board[x][y+1] == board[x][y]
        elif direction == 2: # change right and up neighbor
            board[x][y-1] == board[x][y]
            board[x+1][y] == board[x][y]
        else: # change left and down neighbor
            board[x][y+1] == board[x][y]
            board[x-1][y] == board[x][y]
    return board



def drawBoard(board, boardWidth, boardHeight, boxSize, transparency=255):
    # The colored squares are drawn to a temporary surface which is then
    # drawn to the DISPLAYSURF surface. This is done so we can draw the
    # squares with transparency on top of DISPLAYSURF as it currently is.
    tempSurf = pygame.Surface(DISPLAYSURF.get_size())
    tempSurf = tempSurf.convert_alpha()
    tempSurf.fill((0, 0, 0, 0))

    for x in range(boardWidth):
        for y in range(boardHeight):
            left, top = leftTopPixelCoordOfBox(x, y, boardWidth, boardHeight, boxSize)
            r, g, b = paletteColors[board[x][y]]
            pygame.draw.rect(tempSurf, (r, g, b, transparency), (left, top, boxSize, boxSize))
    left, top = leftTopPixelCoordOfBox(0, 0, boardWidth, boardHeight, boxSize)
    pygame.draw.rect(tempSurf, BLACK, (left-1, top-1, boxSize * boardWidth + 1, boxSize * boardHeight + 1), 1)
    DISPLAYSURF.blit(tempSurf, (0, 0))


def drawPalettes():
    # Draws the six color palettes at the bottom of the screen.
    numColors = len(paletteColors)
    xmargin = int((WINDOWWIDTH - ((PALETTESIZE * numColors) + (PALETTEGAPSIZE * (numColors - 1)))) / 2)
    for i in range(numColors):
        left = xmargin + (i * PALETTESIZE) + (i * PALETTEGAPSIZE)
        top = WINDOWHEIGHT - PALETTESIZE - 10
        pygame.draw.rect(DISPLAYSURF, paletteColors[i], (left, top, PALETTESIZE, PALETTESIZE))
        pygame.draw.rect(DISPLAYSURF, bgColor,   (left + 2, top + 2, PALETTESIZE - 4, PALETTESIZE - 4), 2)


def drawLifeMeter(currentLife, maxLife):
    lifeBoxSize = int((WINDOWHEIGHT - 40) / maxLife)

    # Draw background color of life meter.
    pygame.draw.rect(DISPLAYSURF, bgColor, (20, 20, 20, 20 + (maxLife * lifeBoxSize)))

    for i in range(maxLife):
        if currentLife >= (maxLife - i): # draw a solid red box
            pygame.draw.rect(DISPLAYSURF, RED, (20, 20 + (i * lifeBoxSize), 20, lifeBoxSize))
        pygame.draw.rect(DISPLAYSURF, WHITE, (20, 20 + (i * lifeBoxSize), 20, lifeBoxSize), 1) # draw white outline


def getColorOfPaletteAt(x, y):
    # Returns the index of the color in paletteColors that the x and y parameters
    # are over. Returns None if x and y are not over any palette.
    numColors = len(paletteColors)
    xmargin = int((WINDOWWIDTH - ((PALETTESIZE * numColors) + (PALETTEGAPSIZE * (numColors - 1)))) / 2)
    top = WINDOWHEIGHT - PALETTESIZE - 10
    for i in range(numColors):
        # Find out if the mouse click is inside any of the palettes.
        left = xmargin + (i * PALETTESIZE) + (i * PALETTEGAPSIZE)
        r = pygame.Rect(left, top, PALETTESIZE, PALETTESIZE)
        if r.collidepoint(x, y):
            return i
    return None # no palette exists at these x, y coordinates


def floodFill(board, boardWidth, boardHeight, oldColor, newColor, x, y):
    # This is the flood fill algorithm.
    if oldColor == newColor or board[x][y] != oldColor:
        return

    board[x][y] = newColor # change the color of the current box

    # Make the recursive call for any neighboring boxes:
    if x > 0:
        floodFill(board, boardWidth, boardHeight, oldColor, newColor, x - 1, y) # on box to the left
    if x < boardWidth - 1:
        floodFill(board, boardWidth, boardHeight, oldColor, newColor, x + 1, y) # on box to the right
    if y > 0:
        floodFill(board, boardWidth, boardHeight, oldColor, newColor, x, y - 1) # on box to up
    if y < boardHeight - 1:
        floodFill(board, boardWidth, boardHeight, oldColor, newColor, x, y + 1) # on box to down


def leftTopPixelCoordOfBox(boxx, boxy, boardWidth, boardHeight, boxSize):
    # Returns the x and y of the left-topmost pixel of the xth & yth box.
    xmargin = int((WINDOWWIDTH - (boardWidth * boxSize)) / 2)
    ymargin = int((WINDOWHEIGHT - (boardHeight * boxSize)) / 2)
    return (boxx * boxSize + xmargin, boxy * boxSize + ymargin)


if __name__ == '__main__':
    main(1)
