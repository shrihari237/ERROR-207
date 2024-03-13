#-----------------Boilerplate Code Start-----------
import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image


screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
dice = None

winning_function_call = 0
winningMessage = None
resetButton = None
player1ScoreLabel = None
player2ScoreLabel = None

player1Score = 0
player2Score = 0










def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xPos = 20
    for box in range(0,11):
        if(box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="red")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            leftBoxes.append(boxLabel)
            xPos +=60
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2- 100)
            leftBoxes.append(boxLabel)
            xPos +=60


def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xPos = 870
    for box in range(0,11):
        if(box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="yellow")
            boxLabel.place(x=xPos, y=screen_height/2-100)
            rightBoxes.append(boxLabel)
            xPos +=60
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xPos +=60


def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 109, y=screen_height/2 -160)

def checkColorPosition(boxes, color):
    for box in boxes:
        boxColor = box.cget('bg')
        if boxColor == color:
            return boxes.index(box)
    return False

def movePlayer1(steps):
    global leftBoxes
    global finishingBox
    global SERVER
    global playerName
    global boxPosition

   
    boxPosition = checkColorPosition(leftBoxes[1:],'red') 
    print('box pos: ',boxPosition)   
    if boxPosition:
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        print('remainingSteps:',remainingSteps)
        print('Dice value',diceValue)
        if steps ==remainingSteps:
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            finishingBox.configure(bg='red')  
            msg = 'Red wins the game!'
            SERVER.send(msg.encode())
        elif steps<remainingSteps:
            for box in leftBoxes[1:]:
                box.configure(bg="white")

            nextStep = coloredBoxIndex +1 +diceValue
            leftBoxes[nextStep].configure(bg='red')
        else:
            print('Move False')  
    else:
        leftBoxes[steps].configure(bg="red")                    

def movePlayer2(steps):
    global rightBoxes
    global finishingBox
    global SERVER

    
    boxPosition = checkColorPosition(rightBoxes[0:10],'yellow') 
    print('box pos yellow',boxPosition)
    print('Steps:' ,steps)

    if boxPosition:
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if steps == remainingSteps:
            for box in rightBoxes[0:10]:
                box.configure(bg='white')

            finishingBox.config(bg='yellow')
            msg = 'Yellow wins the game'
            SERVER.send(msg.encode())

        elif steps<remainingSteps:
            for box in rightBoxes[0:10]:
                box.configure(bg='white')

            nextStep = coloredBoxIndex-diceValue
            rightBoxes[nextStep].config(bg='yellow')
    else:
        rightBoxes[-steps-1].configure(bg="yellow")




def rollDice():
    global SERVER,playerType,playerTurn,rollButton
    diceChoices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    value =random.choice(diceChoices)

    rollButton.destroy()
    playerTurn = False
    steps = 0
    if value == '\u2680':
        steps=1
    elif value=='\u2681':
        steps=2  
    elif value=='\u2682':
        steps=3  
    elif value=='\u2683':
        steps=4
    elif value=='\u2684':
        steps=5 
    elif value=='\u2685':
        steps=6

    print('steps:',steps)

    if playerType == 'player1':
        print("Hello")
        SERVER.send(f'{value}player2Turn'.encode())
    elif playerType == 'player2':
        SERVER.send(f'{value}player1Turn'.encode()) 


def gameWindow():

    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global playerTurn
    global playerType
    global playerName
    global rollButton
    global player1ScoreLabel 
    global player2ScoreLabel
    global winningMessage
    global player1Score
    global player2Score
    global resetButton



    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    # Creating Dice with value 1
    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    resetButton = Button(gameWindow,text="Reset the game",fg='black',font=("Chalkboard SE",15),bg='grey',command=resetGame)
    
    # Declaring Wining Message
    winningMessage = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 250, text = "", font=("Chalkboard SE",100), fill='#fff176')

# Creating Score Board
    player1ScoreLabel = canvas2.create_text(400, screen_height/2 - 160, text = player1Score, font=("Chalkboard SE",80), fill='#fff176' )
    player2ScoreLabel = canvas2.create_text(screen_width - 300, screen_height/2 - 160, text = player2Score, font=("Chalkboard SE",80), fill='#fff176' )

    # Teacher Activity
    leftBoard()
    rightBoard()
    finishingBox()
    


    rollButton = Button(gameWindow,text="Roll Dice",fg="black",bg="grey",font=("Chalkboard SE",15),command=rollDice,width = 20,height=5)

    if(playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
    else:
        rollButton.pack_forget()

    gameWindow.resizable(True, True)
    gameWindow.mainloop()

    



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    # Boilerplate Code
    gameWindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def resetGame():
    global SERVER
    SERVER.send("reset game".encode())

def handleWin(message):
    global playerType
    global rollButton 
    global canvas2 
    global winingMessage 
    global screen_width 
    global screen_height
    global resetButton

    if ('Red' in message):
        if playerType=='player2':
            rollButton.destroy()
    if('Yellow' in message): 
        if playerType =='player1':
            rollButton.destroy()

    canvas2.itemconfigure(winningMessage,text=message)
    resetButton.place(x=screen_width/2 - 80 ,y=screen_height-220 )  
                 

def updateScore(message):
    print('Message: ',message)
    global canvas2
    global player1Score
    global player2Score
    global player1ScoreLabel 
    global player2ScoreLabel

 

    if('Red' in message):
        player1Score += 1
    if('Yellow' in message):
        player2Score += 1    

    canvas2.itemconfigure(player1ScoreLabel,text=player1Score)
    canvas2.itemconfigure(player2ScoreLabel,text=player2Score)

def handleResetGame():
    global canvas2 
    global playerType 
    global gameWindow 
    global rollButton 
    global dice
    global screen_width 
    global screen_height
    global playerTurn 
    global rightBoxes 
    global leftBoxes 
    global finishingBox 
    global resetButton 
    global winningMessage
    global winning_function_call

    canvas2.itemconfigure(dice,text="\u2680")

    if(playerType == 'player1'):
        rollButton = Button(gameWindow,text="Roll Dice",fg="black",bg="grey",font=("Chalkboard SE",15),command=rollDice,width = 20,height=5)
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

        playerTurn = True

    leftBoard()
    rightBoard()

    finishingBox.configure(bg='green')
    canvas2.itemConfigure(winningMessage,text="")

    if playerType == 'player2':
        playerTurn =False

    resetButton.destroy()
    resetButton = Button(gameWindow,text="Reset the game",fg='black',font=("Chalkboard SE",15),bg='grey',command=resetGame)

    winning_function_call = 0



# Boilerplate Code
def recivedMsg():
    global SERVER
    global playerType
    global playerTurn
    global rollButton
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gameWindow
    global winning_function_call


    while True:
        message = SERVER.recv(2048).decode()
        print(message)
    

        if('player_type' in message):
            recvMsg = eval(message)
            playerType = recvMsg['player_type']
            playerTurn = recvMsg['turn']
        elif('⚀' in message):
            # Dice with value 1
            canvas2.itemconfigure(dice, text='\u2680')
        elif('⚁' in message):
            # Dice with value 2
            canvas2.itemconfigure(dice, text='\u2681')
        elif('⚂' in message):
            # Dice with value 3
            canvas2.itemconfigure(dice, text='\u2682')
        elif('⚃' in message):
            # Dice with value 4
            canvas2.itemconfigure(dice, text='\u2683')
        elif('⚄' in message):
            # Dice with value 5
            canvas2.itemconfigure(dice, text='\u2684')
        elif('⚅' in message):
            # Dice with value 6
            canvas2.itemconfigure(dice, text='\u2685')

        if('player1Turn' in message and playerType == 'player1'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

        elif('player2Turn' in message and playerType == 'player2'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 260)
        
        if('player1Turn' in message or 'player2Turn' in message):
            diceChoices = ['⚀','⚁','⚂','⚃','⚄','⚅']
            diceValue = diceChoices.index(message[0])+1

            if 'player2Turn' in message:
                movePlayer1(diceValue)
            elif 'player1Turn' in message:
                movePlayer2(diceValue)

        if ('wins the game!' in message and winning_function_call==0):
            handleWin(message)
            winning_function_call += 1
            updateScore(message)

        if('reset game' in message):
            handleResetGame()    





def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    # Boilerplate Code
    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()




setup()
