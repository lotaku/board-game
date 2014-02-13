import random,\
        pygame,\
        sys,\
        socket,\
        struct

from pygame.locals import *

FPS=30
WINDOWWIDTH = 680
WINDOWHEIGHT=580
BOXSIZE=85
GAPSIZE=10
BOARDWIDTH = 5
BOARDHEIGHT = 5

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
userName = ''
host = ''
port = 51423
serverAddr = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
def main():
    global FPSCLOCK, DISPLAYSURF,catImg,boyImg,userName
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Board Game')
    DISPLAYSURF.fill(NAVYBLUE)

    revealedBoxes = generateRevealedBoxesData(False)

    pygame.display.update()

    while True:
        global userName,closeLoginWindow
        closeLoginWindow = False
        showEnterHint()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #elif event.type == pygame.KEYDOWN and event.key != K_y: # K_KP_ENTER
            elif event.type == pygame.KEYDOWN and event.key != K_RETURN and event.key != K_ESCAPE: # K_KP_ENTER
                EnterUserName(event)
            elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                #closeLoginWindow = True
                #if (enterWorld(userName, closeLoginWindow)):
                    #closeLoginWindow = True
                enterWorld(userName)

        if closeLoginWindow:
            break
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(revealedBoxes)
        showWellcomUser(userName)

        catImg = pygame.image.load('catgirl.png')
        boyImg = pygame.image.load('boy.png')
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex,mousey =event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                #revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes = generateRevealedBoxesData(False)
                #pygame.display.update()
                drawGirl(boxx, boxy)
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def enterWorld(userNameTemp):
    global closeLoginWindow,userName
    s.settimeout(1)
    userNamePacked = struct.pack("!3s", str(userNameTemp))
    s.sendto(userNamePacked, serverAddr)
    #received = ''
    receivedData = s.recv(1024)
    receivedDataUnpacked = struct.unpack("!4s", receivedData)[0]
    if receivedDataUnpacked == 'True':
        closeLoginWindow = 1
        #userName = receivedDataUnpacked
    #else:
        #closeLoginWindow = 1
        #userName = receivedDataUnpacked
    #return closeLoginWindow
    return


def showWellcomUser(userName):
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userName = 'Wellcom ' + userName
    showWellcomUserSurfaceObj = fontObj.render(userName, True, GREEN, NAVYBLUE)
    #wellcomRectObj = wellcomSurfaceObj.get_rect()
    #wellcomRectObj.center = (200, 150)
    DISPLAYSURF.blit(showWellcomUserSurfaceObj, (15,20))
    #pygame.display.update()
def showEnterHint():
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    wellcomSurfaceObj = fontObj.render('Enter Your UserName (Submit with "ENTER" key)', True, GREEN, NAVYBLUE)
    #wellcomRectObj = wellcomSurfaceObj.get_rect()
    #wellcomRectObj.center = (200, 150)
    DISPLAYSURF.blit(wellcomSurfaceObj, (55,150))
    #pygame.display.update()

def EnterUserName(event):
    global userName
    userName += event.unicode
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userNameSurfaceObj = fontObj.render(userName, True, ORANGE, NAVYBLUE)
    #userNameRectObj = userNameSurfaceObj.get_rect()
    #userNameRectObj.center = (10, 20)
    DISPLAYSURF.blit(userNameSurfaceObj, (255,200))
    #pygame.display.update()
def drawGirl(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    DISPLAYSURF.blit(catImg, (left,top))
    #revealedBoxes = generateRevealedBoxesData(False)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    #pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)
    DISPLAYSURF.blit(catImg, (left,top))

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)



def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


#def drawBoard():
    ## Draws all of the boxes at the beginning of game.
    #for boxx in range(BOARDWIDTH):
        #for boxy in range(BOARDHEIGHT):
            #left, top = leftTopCoordsOfBox(boxx, boxy)
            #pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

def drawBoard(revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                drawGirl(boxx, boxy)
                # Draw the (revealed) icon.
                #shape, color = getShapeAndColor(board, boxx, boxy)
                #drawIcon(shape, color, boxx, boxy)
def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes



if __name__ == '__main__':
    main()


