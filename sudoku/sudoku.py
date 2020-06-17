from tkinter import *
import random
import copy


def init(data):
    # set the basic info of the game
    data.cellColors = ["#ff8080","#ffb366","#ffff80",
                      "#ff99cc","#ffffff","#8cff66",
                      "#bf80ff","#80bfff","#99ffdd"]
    data.numColors = ["#ff3333","#ff8000","#999900",
                      "#ff0080","#bfbfbf","#33cc00",
                      "#6600ff","#0066cc","#00e699"]
    data.legalValues = list(range(1,data.size**2+1))

    # set the block type
    data.block = [[0 for i in range(data.size)] for j in range(data.size)]

    # set the board type
    tempCol = []
    for col in range(data.size):
        tempCol.append(copy.deepcopy(data.block))

    tempRow = []
    for row in range(data.size):
        tempRow.append(copy.deepcopy(tempCol))

    data.board = tempRow

    # set the unchanged cells in the board
    data.stillCells=[]

    # set pick up info
    data.isPickedUp = False

    # set massage info
    data.wrongMessage = None

    # set game status
    data.isGameStarted = False
    data.isGameWon = False


def initBoard(data):

    data.demoBoard = copy.deepcopy(data.board)

    # set the initial board info
    initBlock = copy.deepcopy(data.legalValues)
    random.shuffle(initBlock)

    # set the middle part of the board
    for row in range(data.size):
        for col in range(data.size):
            data.demoBoard[1][1][row][col] = initBlock[row*3+col]

    # set the middle right/left part of the board
    # middle right
    for i in range(data.size):
        for j in range(data.size):
            data.demoBoard[1][0][i][j] = data.demoBoard[1][1][(i+1+j%2)%3][j]
    # middle left
    for i in range(data.size):
        for j in range(data.size):
            data.demoBoard[1][2][i][j] = data.demoBoard[1][1][(i+2-j%2)%3][j]

    # set the top/bottom part of the board
    for k in range(data.size):
        # top part
        for i in range(data.size):
            for j in range(data.size):
                data.demoBoard[0][k][j][i] = data.demoBoard[1][k][j][(i+1+j%2)%3]
        # bottom part
        for i in range(data.size):
            for j in range(data.size):
                data.demoBoard[2][k][j][i] = data.demoBoard[1][k][j][(i+2-j%2)%3]

    # shuffle the board
    def shuffle(board,type,block):

        if type == "col":
            cols = list(range(data.size))
            random.shuffle(cols)
            iCol,jCol,useless = cols
            colBlock = block
            for rowBlock in range(data.size):
                for row in range(data.size):
                    temp = board[rowBlock][colBlock][row][iCol]
                    board[rowBlock][colBlock][row][iCol] = board[rowBlock][colBlock][row][jCol]
                    board[rowBlock][colBlock][row][jCol] = temp

        if type == "row":
            rows = list(range(data.size))
            random.shuffle(rows)
            iRow,jRow,useless = rows
            rowBlock = block
            for colBlock in range(data.size):
                for col in range(data.size):
                    temp = board[rowBlock][colBlock][iRow][col]
                    board[rowBlock][colBlock][iRow][col] = board[rowBlock][colBlock][jRow][col]
                    board[rowBlock][colBlock][jRow][col] = temp

    for i in range(random.randint(20,50)):
        if random.randint(0,1):
            type = "row"
            block = random.randint(0,2)
            shuffle(data.demoBoard,type,block)
        else:
            type = "col"
            block = random.randint(0,2)
            shuffle(data.demoBoard,type,block)

    # keep some cells filled and keep them still
    if isLegalSudoku(data.demoBoard,data):
        for i in range(20):
            unchange = True
            while unchange:
                rowBlock = random.randint(0,2)
                colBlock = random.randint(0,2)
                row = random.randint(0,2)
                col = random.randint(0,2)
                if data.board[rowBlock][colBlock][row][col] == 0:
                    data.board[rowBlock][colBlock][row][col] = data.demoBoard[rowBlock][colBlock][row][col]
                    data.stillCells = data.stillCells+[(rowBlock,colBlock,row,col)]
                    unchange = False


def areLegalValues(board,data):
    for rowBlock in range(data.size):
        for colBlock in range(data.size):
            for row in range(data.size):
                for col in range(data.size):
                    if board[rowBlock][colBlock][row][col] not in data.legalValues and\
                       board[rowBlock][colBlock][row][col] != 0:
                        return False
    return True


def isLegalRow(board,data):
    for rowBlock in range(data.size):
        for row in range(data.size):
            values = []
            for colBlock in range(data.size):
                for col in range(data.size):
                    if board[rowBlock][colBlock][row][col] != 0:
                        values = values + [board[rowBlock][colBlock][row][col]]
            if len(list(set(values)))!=len(values):
                return False
    return True


def isLegalCol(board,data):
    for colBlock in range(data.size):
        for col in range(data.size):
            values = []
            for rowBlock in range(data.size):
                for row in range(data.size):
                    if board[rowBlock][colBlock][row][col] != 0:
                        values = values + [board[rowBlock][colBlock][row][col]]
            if len(list(set(values)))!=len(values):
                return False
    return True


def isLegalBlock(board,data):
    for rowBlock in range(data.size):
        for colBlock in range(data.size):
            values = []
            for row in range(data.size):
                for col in range(data.size):
                    if board[rowBlock][colBlock][row][col] != 0:
                        values = values + [board[rowBlock][colBlock][row][col]]
            if len(list(set(values)))!=len(values):
                return False
    return True


def isLegalSudoku(board,data):
    if not areLegalValues(board,data):
        data.wrongMessage = "Wrong Value!"
        return False
    if not isLegalRow(board,data):
        data.wrongMessage = "Duplicated (Row)!"
        return False
    if not isLegalCol(board,data):
        data.wrongMessage = "Duplicated (Col)!"
        return False
    if not isLegalBlock(board,data):
        data.wrongMessage = "Duplicated (Block)!"
        return False
    return True


def clearValue(data):
    for rowBlock in range(data.size):
        for colBlock in range(data.size):
            for row in range(data.size):
                for col in range(data.size):
                    if (rowBlock,colBlock,row,col) not in data.stillCells:
                        data.board[rowBlock][colBlock][row][col] = 0


def checkGame(data):
    for rowBlock in range(data.size):
        for colBlock in range(data.size):
            for row in range(data.size):
                for col in range(data.size):
                    if data.board[rowBlock][colBlock][row][col] == 0:
                        data.isGameWon = False
                        return

    data.isGameWon = True


def mousePressed(event, data):
    if not data.isGameStarted:
        return

    if data.isGameWon:
        return
    x, y = event.x, event.y

    data.wrongMessage = None

    if (data.margin)<x<(data.margin+data.cellSize*data.size**2) and\
       (data.margin)<y<(data.margin+data.cellSize*data.size**2):
        data.rowBlock = (y-data.margin)//(data.cellSize*data.size)
        data.colBlock = (x-data.margin)//(data.cellSize*data.size)
        data.row = (y-data.margin-(data.cellSize*data.size*data.rowBlock))//data.cellSize
        data.col = (x-data.margin-(data.cellSize*data.size*data.colBlock))//data.cellSize
        if (data.rowBlock,data.colBlock,data.row,data.col) not in data.stillCells:
            data.isPickedUp = True
            return

    data.isPickedUp = False


def keyPressed(event, data):
    if event.keysym.lower() == "r":
        init(data)
        return

    if not data.isGameStarted:
        if event.keysym.lower() == "s":
            initBoard(data)
            data.isGameStarted = True
            return
        else:
            return

    if data.isGameWon:
        return

    data.wrongMessage = None
    if data.isPickedUp:
        try:
            # assign the value of the picked-up cell
            if int(event.keysym) in data.legalValues:
                temp = data.board[data.rowBlock][data.colBlock][data.row][data.col]
                data.board[data.rowBlock][data.colBlock][data.row][data.col] = int(event.keysym)
                if not isLegalSudoku(data.board,data):
                    data.board[data.rowBlock][data.colBlock][data.row][data.col] = temp
                checkGame(data)
                return
            # clear the value of the picked-up cell
            elif event.keysym == "0":
                data.wrongMessage = "Wrong Value!"
                return
        except:
            # clear the value of the picked-up cell
            if event.keysym.lower() == "d":
                data.board[data.rowBlock][data.colBlock][data.row][data.col] = 0
                return
            # clear the value of the picked-up cell
            if event.keysym == "Return":
                data.isPickedUp = False
                return
            # clear all the value
            if event.keysym.lower() == "c":
                clearValue(data)
                return

    data.wrongMessage = "Wrong Key"


def timerFired(data):
    pass


def drawGame(canvas, data):
    # draw the background
    drawBackground(canvas, data)
    # draw the board
    drawBoard(canvas,data)
    # draw the picked-up cell
    drawPickedUpCell(canvas,data)
    # draw message
    drawMessage(canvas,data)
    # draw game won massage
    drawGameWin(canvas, data)
    # draw keyboard instruction
    drawInstruction(canvas, data)


def drawBackground(canvas, data):
    canvas.create_rectangle(0, 0, data.width+data.margin*6, data.height, fill="#FFFFFF")


def drawBoard(canvas,data):
    # draw each of the cells
    for rowBlock in range(data.size):
        for colBlock in range(data.size):
            data.cellColor = data.cellColors[rowBlock*3+colBlock]
            for row in range(data.size):
                for col in range(data.size):
                    if (rowBlock,colBlock,row,col) in data.stillCells:
                        data.numColor = "#333333"
                    else:
                        data.numColor = data.numColors[rowBlock*3+colBlock]
                    drawCell(canvas,data,rowBlock,colBlock,row,col)
                    drawNumber(canvas,data,rowBlock,colBlock,row,col)


def drawCell(canvas,data,rowBlock,colBlock,row,col):
    canvas.create_rectangle(data.margin+data.cellSize*(col+colBlock*3),data.margin+data.cellSize*(row+rowBlock*3),
                            data.margin+data.cellSize*(col+colBlock*3+1),data.margin+data.cellSize*(row+rowBlock*3+1),
                            fill=data.cellColor)  # outline=data.cellColor


def drawNumber(canvas,data,rowBlock,colBlock,row,col):
    if data.board[rowBlock][colBlock][row][col]:
        canvas.create_text(data.margin+data.cellSize*(col+colBlock*3+0.5),
                           data.margin+data.cellSize*(row+rowBlock*3+0.5),
                           text=str(data.board[rowBlock][colBlock][row][col]),
                           fill=data.numColor,font="Arial 26 bold")


def drawPickedUpCell(canvas,data):
    if data.isPickedUp:
        data.cellColor = data.cellColors[data.rowBlock*3+data.colBlock]
        data.numColor = data.numColors[data.rowBlock*3+data.colBlock]
        margin = 5
        canvas.create_rectangle(data.margin+data.cellSize*(data.col+data.colBlock*3)-margin,
                                data.margin+data.cellSize*(data.row+data.rowBlock*3)-margin,
                                data.margin+data.cellSize*(data.col+data.colBlock*3+1)+margin,
                                data.margin+data.cellSize*(data.row+data.rowBlock*3+1)+margin,
                                fill=data.numColor,outline=data.numColor)
        canvas.create_rectangle(data.margin+data.cellSize*(data.col+data.colBlock*3),
                                data.margin+data.cellSize*(data.row+data.rowBlock*3),
                                data.margin+data.cellSize*(data.col+data.colBlock*3+1),
                                data.margin+data.cellSize*(data.row+data.rowBlock*3+1),
                                fill=data.cellColor,outline=data.cellColor)
        drawNumber(canvas,data,data.rowBlock,data.colBlock,data.row,data.col)


def drawMessage(canvas,data):
    if data.wrongMessage != None:
        if not data.isPickedUp:
            data.numColor = "#000000"
        canvas.create_text(data.width-data.margin*2.5, data.height/2-data.margin*2,
                           text="Message:\n"+data.wrongMessage, font="Arial 14 bold",fill=data.numColor)


def drawGameWin(canvas, data):
    if data.isGameWon:
        canvas.create_text(data.width/2-data.margin*2, data.height/2, text="You Win!", font="Arial 26 bold")


def drawInstruction(canvas, data):
    if not data.isGameStarted:
        canvas.create_text(data.width/2-data.margin*2, data.height/2, text="Press 'S' to Start Game!", font="Arial 26 bold")
    else:
        canvas.create_text(data.width-data.margin*2.5, data.height/2-data.margin*5,
                           text="Sudoku", font="Arial 24 bold",fill="#000000")
        canvas.create_text(data.width-data.margin*2.5, data.height/2+data.margin*2,
                           text="'R' — Restart\n"
                                "'C' — Clear All\n"
                                "'D' — Delete Value\n"
                                "'Enter' — Confirm\n",
                           font="Arial 16 bold",fill="#000000")


def redrawAll(canvas, data):
    drawGame(canvas, data)


def startNewGame(canvas, data):
    drawBackground(canvas, data)
    drawBoard(canvas,data)
    drawInstruction(canvas, data)


####################################
# use the run function as-is
####################################


def run(margin=40,cellSize=50):

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
        if data.isGameStarted:
            timerFired(data)
            redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # set up data
    class Struct(object): pass
    data = Struct()
    # set the sudoku size
    data.size = 3
    # set rows and cols for the board
    data.rows = list(range(data.size**2))
    data.cols = list(range(data.size**2))
    # set cell size and margin of the board
    data.cellSize = cellSize
    data.margin = margin
    # set board dimensions and margin
    data.width = data.margin*6 + data.cellSize*data.size**2
    data.height = data.margin*2 + data.cellSize*data.size**2

    data.timerDelay=100

    # call initial data
    init(data)

    # create the root and the canvas
    root = Tk()
    # set canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    startNewGame(canvas, data)

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


def playSudoku():
    run()

if __name__ == '__main__':
    playSudoku()
