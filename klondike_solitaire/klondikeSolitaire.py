from tkinter import *
import random
import os
from PIL import Image, ImageTk


def init(data):
    # set dimension info

    data.cardWidth = 90
    data.cardHeight = 150
    data.marginWidth = 40
    data.marginHeight = int(data.cardHeight /5)
    data.boardWidth = data.marginWidth * 8 + data.cardWidth * 7
    data.boardHeight = 32 * int(data.marginHeight)
    # set the basic info of a poker set
    # the card will be represent as a tuple (rank, suit)
    data.rank = list(range(1,14))
    data.suit = ["h","s","c","d"]  # which means "heart","spade","club","diamond"

    # create the deck (top-left of the board)
    data.deck = []
    for i in data.rank:
        for j in data.suit:
            data.deck.append((i,j))
    random.shuffle(data.deck)  # shuffle the cards in deck

    # create the discard pile (to the right of the deck)
    data.discardPile = []

    # create foundations (top-right piles):
    # a ragged 2d list of 4 lists of tuples [[(), ...], [...], [...], [...]]
    data.foundation = [[] for i in range(4)]

    # create face-down cards:
    # a ragged 2d list of 7 lists of tuples [[(), ...], [...], [...], [...], ...]
    data.faceDownCardPile = [[] for i in range(7)]
    for i in range(len(data.faceDownCardPile)):
        for j in range(i):
            data.faceDownCardPile[i].append(data.deck.pop(0))

    # create face-down cards:
    # a ragged 2d list of 7 lists of tuples [[(), ...], [...], [...], [...], ...]
    data.faceUpCardPile = [[] for i in range(7)]
    for i in range(len(data.faceDownCardPile)):
            data.faceUpCardPile[i].append(data.deck.pop(0))

    # set color info
    data.deckInfo = "b"  # back
    data.discardInfo = "e"  # empty

    # set position info
    data.deckPosition = (data.marginWidth,data.marginHeight)
    data.discardPilePosition = (data.marginWidth*2+data.cardWidth,data.marginHeight)
    data.foundationPosition = []
    for i in range(len(data.foundation)):
        data.foundationPosition.append(((data.marginWidth+(3+i)*(data.marginWidth+data.cardWidth)),data.marginHeight))

    # set action info
    data.isPickedUp = False
    data.pickUpCardPosition = None
    data.pickUpCardInfo = None
    data.pickUpLocation = ["discardPile","foundation","faceUpCardPile"]
    data.putDownLocation =["foundation","faceUpCardPile"]
    data.pickUpCardLocation = None
    data.putDownCardLocation = None
    data.multiCard = False
    data.list = None

    # set win info
    data.isGameWin = False


def openImg(title,data):
    abDir = os.getcwd()
    img = Image.open(abDir+"/card/%s.png"%title)
    img.thumbnail((data.imgWidth,data.imgHeight))
    return ImageTk.PhotoImage(img)


def initImg(label,data):
    # store the image of the card
    data.cardImg = dict()
    data.imgWidth = data.cardWidth
    data.imgHeight = data.cardHeight
    # store the face up image
    for i in data.suit:
        for j in data.rank:
            title = i+str(j)
            data.cardImg.update({title: openImg(title,data)})  # store in the dictionary
            label.image = data.cardImg[title]  # store a reference for the future use
    # store the face down image
    data.cardImg.update({"b": openImg("b",data)})  # store in the dictionary
    label.image = data.cardImg["b"]
    # store the empty image
    data.cardImg.update({"e": openImg("e",data)})  # store in the dictionary
    label.image = data.cardImg["e"]

    # store the background image
    data.imgWidth = data.boardWidth
    data.imgHeight = data.boardHeight
    data.cardImg.update({"bg": openImg("bg",data)})  # store in the dictionary
    label.image = data.cardImg["bg"]


def getCard(data):
    # there are some card in deck, put one into the discard pile
    if len(data.deck) != 0:
        data.discardPile.append(data.deck.pop(0))
        rank,suit = data.discardPile[-1]
        data.discardInfo = suit+str(rank)
        # after card-getting process, there is no any card in deck
        if len(data.deck) == 0:
            data.deckInfo = "e"
    # there is no any card in deck
    elif len(data.discardPile) != 0:
        data.deck = data.discardPile
        data.deckInfo = 'b'
        data.discardPile = []
        data.discardInfo = "e"
    else:
        data.deck = []
        data.deckInfo = 'e'
        data.discardPile = []
        data.discardInfo = "e"


def getFaceUpPilePosition(data):
    data.faceUpCardPilePosition = []
    for i in range(len(data.faceUpCardPile)):
        pileLength = len(data.faceDownCardPile[i])+len(data.faceUpCardPile[i])
        data.faceUpCardPilePosition.append((data.marginWidth+(data.marginWidth+data.cardWidth)*i,
                                            (7+pileLength)*data.marginHeight))


def putDownCard(data):
    if data.pickUpCardLocation in data.pickUpLocation or\
       data.pickUpCardLocation[0:-3] in data.pickUpLocation and\
       data.putDownCardLocation[0:-3] in data.putDownLocation:
        if data.cardPiece == 1:
            exec("data."+data.putDownCardLocation+".append(data."+data.pickUpCardLocation+".pop())")
        else:
            temp = []
            for i in range(data.cardPiece):
                exec("temp.append(data."+data.pickUpCardLocation+".pop())")
            for i in range(data.cardPiece):
                exec("data."+data.putDownCardLocation+".append(temp.pop())")


def checkWin(data):
    # check deck and discard pile
    if len(data.deck) != 0 or len(data.discardPile) != 0: return

    # check foundation
    for i in range(len(data.foundation)):
        if len(data.foundation[i]) != 0: return

    # check game card piles
    t = 0
    for i in range(len(data.faceUpCardPile)):
        if len(data.faceUpCardPile[i]) == 13:
            t += 1
    if t == 4:
        data.isGameWin = True



def checkBoard(data):
    if len(data.discardPile)==0:
        data.discardInfo = "e"
    else:
        rank,suit = data.discardPile[-1]
        data.discardInfo = suit+str(rank)
    for i in range(len(data.faceUpCardPile)):
        if len(data.faceUpCardPile[i])==0 and len(data.faceDownCardPile[i])!=0:
            data.faceUpCardPile[i].append(data.faceDownCardPile[i].pop())
    getFaceUpPilePosition(data)
    checkWin(data)


def compareSuit(suit,suitF):
    black = ["s","c"]
    red = ["h","d"]
    if (suit in black and suitF in red) or (suitF in black and suit in red): return True
    return False


def isClickLegal(x,y,xCard,yCard,data):
    if data.multiCard == False:
        if xCard <= x <= xCard+data.cardWidth and yCard <= y <= yCard+data.cardHeight: return True
        else: return False
    else:
        if xCard <= x <= xCard+data.cardWidth and yCard <= y <= yCard+data.marginHeight: return True
        else: return False


def mousePressed(event,data):

    x,y = event.x, event.y

    if data.marginWidth*3+data.cardWidth*2 <= x <= data.marginWidth*3+data.cardWidth*3 and\
       data.marginHeight*3 <= y <= data.marginHeight*4:
        init(data)
        getFaceUpPilePosition(data)

    if data.isGameWin:
        return

    # get a new card
    xCard,yCard = data.deckPosition
    if isClickLegal(x,y,xCard,yCard,data):
        getCard(data)

    # pick up the card
    if data.isPickedUp == False:
        # pick up card in discard pile
        xCard,yCard = data.discardPilePosition
        if isClickLegal(x,y,xCard,yCard,data):
            if len(data.discardPile) != 0:
                data.isPickedUp = True
                data.multiCard = False
                data.pickUpCardPosition = data.discardPilePosition
                data.pickUpCardInfo = data.discardPile[-1]
                data.pickUpCardLocation = "discardPile"
                data.cardPiece = 1
                return

        # pick card in foundation
        for i in range(len(data.foundationPosition)):
            xCard,yCard = data.foundationPosition[i]
            if isClickLegal(x,y,xCard,yCard,data):
                if len(data.foundation[i]) != 0:
                    data.isPickedUp = True
                    data.multiCard = False
                    data.pickUpCardPosition = data.foundationPosition[i]
                    data.pickUpCardInfo = data.foundation[i][-1]
                    data.pickUpCardLocation = "foundation[%s]"%i
                    data.cardPiece = 1
                    return

        # pick card in face-up card pile
        for i in range(len(data.faceUpCardPilePosition)):
            xCard,yCard = data.faceUpCardPilePosition[i]
            if isClickLegal(x,y,xCard,yCard,data):
                if len(data.faceUpCardPile[i]) != 0:
                    data.isPickedUp = True
                    data.multiCard = False
                    data.pickUpCardPosition = data.faceUpCardPilePosition[i]
                    data.pickUpCardInfo = data.faceUpCardPile[i][-1]
                    data.pickUpCardLocation = "faceUpCardPile[%s]"%i
                    data.cardPiece = 1
                    return

        # try pick up multi-cards
        # pick up multi-cards in face-up card pile
        data.multiCard = True
        for i in range(len(data.faceUpCardPilePosition)):
            xCard,yCard = data.faceUpCardPilePosition[i]
            if len(data.faceUpCardPile[i]) != 0:
                cards = len(data.faceUpCardPile[i])
                for j in range(len(data.faceUpCardPile[i])-1,0,-1):
                    yCard = yCard-data.marginHeight*(j)
                    if isClickLegal(x,y,xCard,yCard,data):
                        data.isPickedUp = True
                        data.pickUpCardPosition = (xCard,yCard)
                        data.pickUpCardInfo = data.faceUpCardPile[i][-cards]
                        data.pickUpCardLocation = "faceUpCardPile[%s]"%i
                        data.cardPiece = cards
                        data.list = i
                        return
                    xCard,yCard = data.faceUpCardPilePosition[i]
                    cards -= 1
        data.multiCard = False

    # after pick action
    else:
        # try put down the card
        # process multi-card in the first place
        if data.multiCard:
            # only put multi-card in face-up card pile
            for i in range(len(data.faceUpCardPile)):
                xCard,yCard = data.faceUpCardPilePosition[i]
                data.multiCard = False
                if isClickLegal(x,y,xCard,yCard,data):
                    data.multiCard = True
                    rank,suit = data.pickUpCardInfo
                    if len(data.faceUpCardPile[i]) != 0:
                        rankF,suitF = data.faceUpCardPile[i][-1]
                        if rank == rankF-1 and compareSuit(suit,suitF):
                            data.putDownCardLocation = "faceUpCardPile[%s]"%i
                            putDownCard(data)
                            checkBoard(data)
                            data.isPickedUp = False
                            data.multiCard = False
                            return
                    else:
                        if rank==13:
                            data.putDownCardLocation = "faceUpCardPile[%s]"%i
                            putDownCard(data)
                            checkBoard(data)
                            data.isPickedUp = False
                            data.multiCard = False
                            return

        else:
            # put down card in foundation
            for i in range(len(data.foundation)):
                xCard,yCard = data.foundationPosition[i]
                if isClickLegal(x,y,xCard,yCard,data):
                    rank,suit = data.pickUpCardInfo
                    if len(data.foundation[i]) == 0:
                        if rank == 1:
                            data.putDownCardLocation = "foundation[%s]"%i
                            putDownCard(data)
                            checkBoard(data)
                            data.isPickedUp = False
                            data.multiCard = False
                            return
                    else:
                        rankF,suitF = data.foundation[i][-1]
                        if rank==rankF+1 and suit==suitF:
                            data.putDownCardLocation = "foundation[%s]"%i
                            putDownCard(data)
                            checkBoard(data)
                            data.isPickedUp = False
                            data.multiCard = False
                            return

            # put down card in face-up card pile
            for i in range(len(data.faceUpCardPile)):
                xCard,yCard = data.faceUpCardPilePosition[i]
                if isClickLegal(x,y,xCard,yCard,data):
                    rank,suit = data.pickUpCardInfo
                    if len(data.faceUpCardPile[i]) != 0:
                        rankF,suitF = data.faceUpCardPile[i][-1]
                        if rank == rankF-1 and compareSuit(suit,suitF):
                            data.putDownCardLocation = "faceUpCardPile[%s]"%i
                            putDownCard(data)
                            checkBoard(data)
                            data.isPickedUp = False
                            data.multiCard = False
                            return
                    else:
                        if rank==13:
                            data.putDownCardLocation = "faceUpCardPile[%s]"%i
                            putDownCard(data)
                            checkBoard(data)
                            data.isPickedUp = False
                            data.multiCard = False
                            return

        # try pick up again
        # pick up card in discard pile
        xCard,yCard = data.discardPilePosition
        if isClickLegal(x,y,xCard,yCard,data):
            if len(data.discardPile) != 0:
                data.isPickedUp = True
                data.multiCard = False
                data.pickUpCardPosition = data.discardPilePosition
                data.pickUpCardInfo = data.discardPile[-1]
                data.pickUpCardLocation = "discardPile"
                data.cardPiece = 1
                return

        # pick card in foundation
        for i in range(len(data.foundationPosition)):
            xCard,yCard = data.foundationPosition[i]
            if isClickLegal(x,y,xCard,yCard,data):
                if len(data.foundation[i]) != 0:
                    data.isPickedUp = True
                    data.multiCard = False
                    data.pickUpCardPosition = data.foundationPosition[i]
                    data.pickUpCardInfo = data.foundation[i][-1]
                    data.pickUpCardLocation = "foundation[%s]"%i
                    data.cardPiece = 1
                    return

        # pick card in face-up card pile
        for i in range(len(data.faceUpCardPilePosition)):
            xCard,yCard = data.faceUpCardPilePosition[i]
            if isClickLegal(x,y,xCard,yCard,data):
                if len(data.faceUpCardPile[i]) != 0:
                    data.isPickedUp = True
                    data.multiCard = False
                    data.pickUpCardPosition = data.faceUpCardPilePosition[i]
                    data.pickUpCardInfo = data.faceUpCardPile[i][-1]
                    data.pickUpCardLocation = "faceUpCardPile[%s]"%i
                    data.cardPiece = 1
                    return

        # try pick up multi-cards(undone)
        # pick up multi-cards in face-up card pile
        data.multiCard = True
        for i in range(len(data.faceUpCardPilePosition)):
            xCard,yCard = data.faceUpCardPilePosition[i]
            if len(data.faceUpCardPile[i]) != 0:
                cards = len(data.faceUpCardPile[i])
                for j in range(len(data.faceUpCardPile[i])-1,0,-1):
                    yCard = yCard-data.marginHeight*(j)
                    if isClickLegal(x,y,xCard,yCard,data):
                        data.isPickedUp = True
                        data.pickUpCardPosition = (xCard,yCard)
                        data.pickUpCardInfo = data.faceUpCardPile[i][-cards]
                        data.pickUpCardLocation = "faceUpCardPile[%s]"%i
                        data.cardPiece = cards
                        data.list = i
                        return
                    xCard,yCard = data.faceUpCardPilePosition[i]
                    cards -= 1
        data.multiCard = False

    data.isPickedUp = False



def keyPressed(event, data):
    pass


def timerFired(data):
    pass


def drawGame(canvas, data):
    # draw the background
    drawBackground(canvas, data)
    # draw the game board
    drawBoard(canvas,data)
    # draw keyboard instruction
    drawInstruction(canvas, data)
    # draw game over massage
    drawGameWin(canvas, data)


def drawBackground(canvas, data):
    canvas.create_image(0,0,image=data.cardImg["bg"],anchor='nw')


def drawBoard(canvas, data):
    drawDeck(canvas,data)
    drawDiscardPile(canvas,data)
    drawFoundation(canvas,data)
    drawFaceDownCardPile(canvas, data)
    drawFaceUpCardPile(canvas, data)
    drawPickedUpCard(canvas,data)
    drawRestartButton(canvas,data)


def drawDeck(canvas,data):
    canvas.create_image(data.marginWidth,data.marginHeight,
                        image=data.cardImg[data.deckInfo],anchor='nw')


def drawDiscardPile(canvas,data):
    canvas.create_image(data.marginWidth*2+data.cardWidth,data.marginHeight,
                        image=data.cardImg[data.discardInfo],anchor='nw')


def drawFoundation(canvas,data):
    for i in range(len(data.foundation)):
        if len(data.foundation[i]) != 0 :
            rank,suit = data.foundation[i][-1]
            canvas.create_image(data.marginWidth+(data.marginWidth+data.cardWidth)*(3+i),data.marginHeight,
                                image=data.cardImg[(suit+str(rank))],anchor='nw')
        else:
            canvas.create_image(data.marginWidth+(data.marginWidth+data.cardWidth)*(3+i),data.marginHeight,
                                image=data.cardImg["e"],anchor='nw')


def drawFaceDownCardPile(canvas, data):
    for i in range(len(data.faceDownCardPile)):
        if len(data.faceDownCardPile[i]) == 0:
            canvas.create_image(data.marginWidth+(data.marginWidth+data.cardWidth)*i,data.marginHeight*(8),
                                    image=data.cardImg["e"],anchor='nw')
        else:
            for j in range(len(data.faceDownCardPile[i])):
                canvas.create_image(data.marginWidth+(data.marginWidth+data.cardWidth)*i,data.marginHeight*(8+j),
                                    image=data.cardImg["b"],anchor='nw')


def drawFaceUpCardPile(canvas, data):
    for i in range(len(data.faceUpCardPile)):
        if len(data.faceUpCardPile[i]) == 0:
            canvas.create_image(data.marginWidth+(data.marginWidth+data.cardWidth)*i,data.marginHeight*(8),
                                    image=data.cardImg["e"],anchor='nw')
        else:
            for j in range(len(data.faceUpCardPile[i])):
                rank,suit = data.faceUpCardPile[i][j]
                offset = len(data.faceDownCardPile[i])+j
                canvas.create_image(data.marginWidth+(data.marginWidth+data.cardWidth)*i,data.marginHeight*(8+offset),
                                    image=data.cardImg[(suit+str(rank))],anchor='nw')


def drawPickedUpCard(canvas,data):
    if data.isPickedUp:
        if data.multiCard == False:
            x,y=data.pickUpCardPosition
            rank,suit=data.pickUpCardInfo
            margin = 5
            canvas.create_rectangle(x-margin,y-margin,x+data.cardWidth+margin,y+data.cardHeight+margin,
                                fill="#FFB5B5",outline="#FFB5B5")
            canvas.create_image(x,y,image=data.cardImg[(suit+str(rank))],anchor='nw')
        else:
            x,y=data.pickUpCardPosition
            margin = 5
            for i in range(data.cardPiece):
                canvas.create_rectangle(x-margin,y+data.marginHeight*i-margin,
                                        x+data.cardWidth+margin,y+data.marginHeight*i+data.cardHeight+margin,
                                        fill="#FFB5B5",outline="#FFB5B5")

            for i in range(data.cardPiece):
                rank,suit=data.faceUpCardPile[data.list][-data.cardPiece+i]
                canvas.create_image(x,y+data.marginHeight*i,image=data.cardImg[(suit+str(rank))],anchor='nw')


def drawRestartButton(canvas,data):
    canvas.create_rectangle(data.marginWidth*3+data.cardWidth*2,data.marginHeight*3,
                            data.marginWidth*3+data.cardWidth*3,data.marginHeight*4,
                                fill="#FFB5B5",outline="#FFB5B5")
    canvas.create_text(data.marginWidth*3+data.cardWidth*2.5, data.marginHeight*3.5, text="Restart",
                       font="Arial 14 bold",fill="#FF7575")


def drawInstruction(canvas, data):
    pass


def drawGameWin(canvas, data):
    if data.isGameWin:
        canvas.create_text(data.width/2, data.height/2, text="You Win!\n\n",
                       font="Arial 40 bold",fill="#FF7575")
        canvas.create_text(data.width/2, data.height/2, text="Click 'Restart' to Start a New Game!",
                       font="Arial 20 bold",fill="#FF7575")


def redrawAll(canvas, data):
    drawGame(canvas, data)


def startNewGame(canvas,label,data):
    initImg(label,data)
    getFaceUpPilePosition(data)

####################################
# use the run function as-is
####################################


def run(width=950,height=960):

    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # set up data
    class Struct(object): pass
    data = Struct()

    data.width = width
    data.height = height

    data.timerDelay=100

    # call initial data
    init(data)

    # create the root and the canvas
    root = Tk()
    # set canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    label = Label(root)
    label.pack()

    startNewGame(canvas, label, data)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

    # end
    print("bye!")


####################################
# playTetris() [calls run()]
####################################


def playSolitaire():
    run()

if __name__ == '__main__':
    playSolitaire()
