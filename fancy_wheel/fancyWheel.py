from tkinter import *
from math import *


def init(data):
    # set height of window
    data.height = int(data.width/20*21)

    # set the radius of a fancy wheel
    data.radius = int(data.width/(data.number*5+1))*2

    # set the margin of canvas
    data.margin = int((data.width - data.number*data.radius*2)/(data.number+1))

    # set rows and cols of the fancy wheels
    data.rows = list(range(data.number))
    data.cols = list(range(data.number))

    # set the button width
    data.buttonWidth = int(data.width/100)

    # set button margin
    data.buttonMargin = int((data.width-data.buttonWidth*8*10)/2)    # 7 buttons and 1 label

    # set time delay
    data.timerDelay=100

    # set basic color
    data.colorCode = list("0123456789abcdef")
    data.colorMargin = int((len(data.colorCode)-1)/(data.number-1))
    data.colorCodeSelected = []
    for i in range(data.number):
        data.colorCodeSelected.append(data.colorCode[0+data.colorMargin*i])
    data.wheelColors = []
    for i in data.rows:
        temp = []
        for j in data.cols:
            c1=data.colorCodeSelected[i]
            c2=data.colorCodeSelected[-j-1]
            c3=data.colorCodeSelected[-i-1]
            temp.append("#"+str(c1*2+c2*2+c3*2))
        data.wheelColors.append(temp)

    # set start angle
    data.startAngle = 0

    # set auto status
    data.go = False

    # set step info
    data.stepCounter = 0

class fancyWheel(object):
    def __init__(self,data,row,col):
        self.radius = data.radius
        self.centX = data.margin*(1+col) + data.radius*(1+2*col)
        self.centY = data.margin*(1+row) + data.radius*(1+2*row)
        self.side = 4 + row + col
        self.angle = 360/self.side
        self.color = data.wheelColors[row][col]
        self.clockWise = True if (row+col)%2 == 0 else False

    def getVertexLocation(self,startAngle):
        if not self.clockWise:
            startAngle = -1*startAngle
        self.vertexLocation = []
        for i in range(self.side):
            tempX = self.centX + self.radius * cos(radians(startAngle+self.angle*i))
            tempY = self.centY + self.radius * sin(radians(startAngle+self.angle*i))
            self.vertexLocation.append((tempX,tempY))

    def drawLine(self,data):
        for i in range(self.side-1):
            for j in range(self.side):
                x0,y0,x1,y1 = self.vertexLocation[j] + self.vertexLocation[(j+i)%self.side]
                data.canvas.create_line(x0,y0,x1,y1,fill=self.color,width=0)

    def drawWheel(self,data,startAngle=0):
        self.getVertexLocation(startAngle)
        self.drawLine(data)


def go(data):
    data.go = True


def pause(data):
    data.go = False


def backward(data):
    data.startAngle -= 10
    data.stepCounter -= 1


def forward(data):
    data.startAngle += 10
    data.stepCounter += 1


def reset(data):
    data.go = False
    data.timeDelay = 100
    data.startAngle = 0
    data.stepCounter = 0


def faster(data):
    if data.timerDelay > 10:
        data.timerDelay -= 10


def slower(data):
    data.timerDelay += 10


def mousePressed(event, data):
    pass


def keyPressed(event, data):
    if event.keysym == "plus":
        if data.number<16:
            data.number += 1
            init(data)
            return

    if event.keysym == "minus":
        if data.number>2:
            data.number -= 1
            init(data)
            return

    if event.keysym == "Up":
        faster(data)
        return

    if event.keysym == "Down":
        slower(data)
        return

    if event.keysym == "Left":
        backward(data)
        return

    if event.keysym == "Right":
        forward(data)
        return

    if event.keysym == "space":
        if data.go:
            data.go = False
            return
        data.go = True
        return


def timerFired(data):
    forward(data)


def drawCanvas(data):
    # draw the background
    drawBackground(data)
    # draw the board
    drawBoard(data)
    # draw button district
    drawButtonDistrict(data)
    # draw step counter
    drawStepCounter(data)


def drawBackground(data):
    data.canvas.create_rectangle(0,0,data.width,data.width,fill="#000000",width=0)
    pass


def drawWheel(data):
    for i in data.rows:
        for j in data.cols:
            fancyWheel(data,i,j).drawWheel(data,data.startAngle)


def drawButtonDistrict(data):
    data.canvas.create_rectangle(0,data.width+2,data.width,data.height,fill="#000000",width=0)


def drawStepCounter(data):
    data.canvas.create_text(data.buttonMargin+data.buttonWidth*10*7.5,data.width/20*20.5,text="Step %s"%str(data.stepCounter),font="Arial 14",fill="#ffffff")


def drawBoard(data):
    drawWheel(data)
    pass


def redrawAll(data):
    drawCanvas(data)


####################################
# use the run function as-is
####################################


def run():

    def setCanvas(root,data):
        data.canvas = Canvas(root, width=data.width, height=data.height)
        data.canvas.place(x=0, y=0)

    def setLabel(root,data):
        pass

    def setButton(root,data):
        buttonGo = Button(root, text="Go", width=data.buttonWidth, command=lambda: go(data))
        buttonGo.place(x=data.buttonMargin+data.buttonWidth*10*0.5, y=data.width/20*20.5, anchor = CENTER)

        buttonPause = Button(root, text="Pause", width=data.buttonWidth, command=lambda: pause(data))
        buttonPause.place(x=data.buttonMargin+data.buttonWidth*10*1.5, y=data.width/20*20.5, anchor = CENTER)

        buttonStep = Button(root, text="Backward", width=data.buttonWidth, command=lambda: backward(data))
        buttonStep.place(x=data.buttonMargin+data.buttonWidth*10*2.5, y=data.width/20*20.5, anchor = CENTER)

        buttonStep = Button(root, text="Forward", width=data.buttonWidth, command=lambda: forward(data))
        buttonStep.place(x=data.buttonMargin+data.buttonWidth*10*3.5, y=data.width/20*20.5, anchor = CENTER)

        buttonFaster = Button(root, text="Faster+", width=data.buttonWidth, command=lambda: faster(data))
        buttonFaster.place(x=data.buttonMargin+data.buttonWidth*10*4.5, y=data.width/20*20.5, anchor = CENTER)

        buttonSlower = Button(root, text="Slower-", width=data.buttonWidth, command=lambda: slower(data))
        buttonSlower.place(x=data.buttonMargin+data.buttonWidth*10*5.5, y=data.width/20*20.5, anchor = CENTER)

        buttonReset = Button(root, text="Reset", width=data.buttonWidth, command=lambda: reset(data))
        buttonReset.place(x=data.buttonMargin+data.buttonWidth*10*6.5, y=data.width/20*20.5, anchor = CENTER)

    def redrawAllWrapper(data):
        data.canvas.delete(ALL)
        redrawAll(data)
        data.canvas.update()

    def mousePressedWrapper(event, data):
        mousePressed(event, data)
        redrawAllWrapper(data)

    def keyPressedWrapper(event, data):
        keyPressed(event, data)
        redrawAllWrapper(data)

    def timerFiredWrapper(data):
        if data.go:
            timerFired(data)
        redrawAllWrapper(data)
        # pause, then call timerFired again
        data.canvas.after(data.timerDelay,timerFiredWrapper,data)

    # set up data
    class Struct(object): pass
    data = Struct()

    # set the default number of fancy wheels
    data.number = 5

    # set the default width of window
    data.width = 900

    # call initial data
    init(data)

    # create the root and the canvas
    root = Tk()
    root.geometry(str(data.width)+"x"+str(data.height))

    # set canvas
    setCanvas(root,data)

    # set label
    setLabel(root,data)

    # set button
    setButton(root,data)

    # initial canvas
    drawCanvas(data)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event,data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event,data))
    timerFiredWrapper(data)

    # and launch the app
    root.mainloop()  # blocks until window is closed

    # end
    print("bye!")


####################################
# playFancyWheel() [calls run()]
####################################


def playFancyWheel():
    run()



if __name__ == '__main__':
  playFancyWheel()
