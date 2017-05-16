import tkinter
from tkinter import *
from tkinter import messagebox, Tk
from time import sleep
from random import randint
import Client

"""If the game was in a class, this docstring would be below it. As we learnt about classes far into the devlopment of the game, implementing the code into a class would have required
large code rewrites which would have pushed us over the allocated time to complete this coursework project. As such, use of 3/4 global variables to access variables that were outside the
local scope for most functions is used, apologies for the poor programming technique"""

try:
    c = Client.Client() #Accesses the client file and connects to the server
finally:
    
    clientNo = 10 #Default client value to differentiate between game move messages when sending/receiving from the server

    bclick = [True] #Value used to change between 'X' and 'O'. X is true, O is false.
    AISelectionBool = [False] #Value used to determine if player wishes to play against the AI in a later function
    yourTurn = [False] #Bool to determine if it's your turn or not when playing against another player over a server

    master = Tk() #The main board frame
    master.withdraw() #Hides the main board so only the game type selection window is shown
    master.resizable(0,0) #Disables window maximise button
    master.minsize(500,600) #Makes the window non-resizable
    master.maxsize(500,600) #Makes the window non-resizable
    master.attributes("-topmost", True) #Moves the game window to the top
    frame = Frame(master, bg="", colormap="new") #Formatting
    frame.pack()
    master.title("Tic Tac Toe") 

    xCurrentScore = StringVar() #Label has to be updated with a textvariable, so score must be a string variable
    oCurrentScore = StringVar() #Label has to be updated with a textvariable, so score must be a string variable

    xCurrentScoreList = [0] #Stores X score value in an array so it can be updated from within a function
    oCurrentScoreList = [0] #Stores O score value in an array so it can be updated from within a function

    LabelX = Label(textvariable = xCurrentScore,font = ('Arial 25')) #Displays the current score for X in the GUI
    LabelX.pack(side = LEFT, padx = 10) 

    LabelO = Label(textvariable = oCurrentScore,font = ('Arial 25')) #Displays the current score for O in the GUI
    LabelO.pack(side = RIGHT, padx = 20) 

    xCurrentScore.set("X's Score:   " + str(xCurrentScoreList[0])) #Tells LabelX what to display in the GUI 
    oCurrentScore.set("O's Score:   " + str(oCurrentScoreList[0])) #Tells LabelO what to display in the GUI

    buttonsList = [" "," "," "," "," "," "," "," "," "] #Holds the value for each button to be used for game win check comparisons

    #Defining each button to be generated with tkinter

    button1 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button1,0))
    button1.grid(row = 1, column = 0)

    button2 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button2,1))
    button2.grid(row = 1, column = 1)

    button3 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button3,2))
    button3.grid(row = 1, column = 2)

    button4 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button4,3))
    button4.grid(row = 2, column = 0)

    button5 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button5,4))
    button5.grid(row = 2, column = 1)

    button6 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button6,5))
    button6.grid(row = 2, column = 2)

    button7 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button7,6))
    button7.grid(row = 3, column = 0)

    button8 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button8,7))
    button8.grid(row = 3, column = 1)

    button9 = Button(frame, font = ('Arial 30 bold'), text = " ", height = 3, width = 6, command = lambda: tictactoe(button9,8))
    button9.grid(row = 3, column = 2)

    master.geometry('605x710+660+180') #Assings baord position to middle of screen

    sleep(2)

    def computerOrAI():
        """Player chooses whether they wish to play against a random AI computer, or another player over a server"""
        global yourTurn
        modeSelection = Toplevel()
        modeSelection.title("Choose Game Type")
        modeSelection.minsize(320,120) #Makes the window un-resizable
        modeSelection.maxsize(320,120)
        modeSelection.resizable(0,0) #Disables the 'Maximise' button
        modeSelection.geometry('320x120+800+400')
        modeSelection.attributes("-topmost", True) #Keeps the window on the top

        AISelectionBool[0] = False #Resets the bool value after a game has finished
     
        msg = Label(modeSelection, text="Would you like to play against the computer", font = ('Arial 12'))
        msg.pack(pady = 5)

        msg1 = Label(modeSelection, text="or another player?", font = ('Arial 12')) #Probably could've combined msg and msg1 but didn't know 'new line' syntax for labels
        msg1.pack()

        buttonAI = Button(modeSelection, text="Against the AI", font = ('Arial 15 bold'), command = lambda: randomAI()) #On button click runs the randomAI function to play against a random AI
        buttonAI.pack(side = LEFT, padx = 5)

        buttonPlayer = Button(modeSelection, text="Another Player", font = ('Arial 15 bold'), command = lambda: playerOverServer()) #On button click runs the playerOverServer function to play against another player over a server
        buttonPlayer.pack(side = RIGHT, padx = 5)

        def playerOverServer():
            """Player chooses the option to play against another player on a server"""
            global clientNo
            modeSelection.destroy() #Destroys the current window
            playerSelection() #Opens the player selection window so the player can choose between being 'X' or 'O'

            messages = c.poll() #Grabs all messages sent to the client from the server
            
            for message in messages:
                print( "Received \"{}\"".format( message ) )
                if message[0:12] == "Hello client" and (clientNo == 10):
                    clientNo = int(message[13:14]) #Upon first connection to the server, the server will assign the client a value to be able to determine between whos turn in the game it is                 
                
            messages = c.poll() #Clears messages 
            print(clientNo) #Debug

            if clientNo == 0: 
                yourTurn[0] = True #If you're the first person to connect to the server, you will be assigned the client number 0, and so you will go first
                print(yourTurn[0]) #Debug

        def randomAI():
            """Player chooses to play against the random AI bot"""
            global clientNo
            AISelectionBool[0] = True #Changes the AI bool so the game knows you wish to play against the AI
            modeSelection.destroy() #Destroys the current window
            playerSelection() #Opens the player selection window so the player can choose between being 'X' or 'O'

            messages = c.poll() #Grabs all messages sent to the client from the server
            
            for message in messages:
                print( "Received \"{}\"".format( message ) )
                if message[0:12] == "Hello client" and (clientNo == 10):
                    clientNo = int(message[13:14]) #Upon first connection to the server, the server will assign the client a value to be able to determine between whos turn in the game it is  
                    
            messages = c.poll() #Clears messages
            print(clientNo) #Debug

            if clientNo == 0:
                yourTurn[0] = True #If you're the first person to connect to the server, you will be assigned the client number 0, and so you will go first
                print(yourTurn[0]) #Debug

    def playerSelection():
        """Determines whether the player wishes to be 'X' or 'O' in the game"""
        
        playerSelect = Toplevel() 
        playerSelect.title("X/O")
        playerSelect.minsize(250,100)
        playerSelect.maxsize(250,100)
        playerSelect.resizable(0,0)
        playerSelect.geometry('250x100+800+400')
        playerSelect.attributes("-topmost", True)

        msg = Label(playerSelect, text="Which player will start first?",  font = ('Arial 12'))
        msg.pack(pady = 10)

        buttonX = Button(playerSelect, text="Player 'X'", font = ('Arial 15 bold'), command = lambda: xButtonClick()) #On button click runs the xButtonClick function to choose to be 'X' in the game
        buttonX.pack(side = LEFT, padx = 5)

        buttonO = Button(playerSelect, text="Player 'O'", font = ('Arial 15 bold'), command = lambda: oButtonClick()) #On button click runs the oButtonClick function to choose to be 'O' in the game
        buttonO.pack(side = RIGHT, padx = 5)

        def xButtonClick():
            """Assigns the player the 'X' value for the game and shows the player the main game board"""
            bclick[0] = True #Assigns your game value
            playerSelect.destroy()
            clearBoard() #If game is being run for a second time, ensures the board is cleared to start a new game
            master.update() #Ensures game labels are properly visually updated
            master.deiconify() #Makes the game board visible

        def oButtonClick():
            """Assigns the player the 'O' value for the game and shows the player the main game board"""
            bclick[0] = False #Assigns your game value
            playerSelect.destroy()
            clearBoard() #If game is being run for a second time, ensures the board is cleared to start a new game
            master.update() #Ensures game labels are properly visually updated
            master.deiconify() #Makes the game board visible

    def on_closing():
        """When the player attempts to close the game, generates a message box asking for confirmation"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            master.destroy()

    def tictactoe(button, listValue):
        """The main game code where button values are updated based on game type and game win scenarios are checked"""

        global bclick
        global yourTurn

        def opponentTurn(button, letter):
            """Function to be run when the game/client receives a message from the server telling the client what move the opponent has made"""
            if button == 0:
                button1["text"] = letter #Updates visual game for player
                buttonsList[0] = letter #Updates button list which is used for game win check comparisons
            elif button == 1:
                button2["text"] = letter
                buttonsList[1] = letter
            elif button == 2:
                button3["text"] = letter
                buttonsList[2] = letter
            elif button == 3:
                button4["text"] = letter
                buttonsList[3] = letter
            elif button == 4:
                button5["text"] = letter
                buttonsList[4] = letter
            elif button == 5:
                button6["text"] = letter
                buttonsList[5] = letter
            elif button == 6:
                button7["text"] = letter
                buttonsList[6] = letter
            elif button == 7:
                button8["text"] = letter
                buttonsList[7] = letter
            elif button == 8:
                button9["text"] = letter
                buttonsList[8] = letter
        
        def AIRunCheck():
            """All the checks/moves made if the player is playing against the random AI bot"""

            def buttonCheckAssignment(letter, number):
                """Changes the value displayed on the game board visually to the player"""
                if number == 0:
                    button1["text"] = letter #Updates visual game for player
                    buttonsList[0] = letter #Updates button list which is used for game win check comparisons
                elif number == 1:
                    button2["text"] = letter
                    buttonsList[1] = letter
                elif number == 2:
                    button3["text"] = letter
                    buttonsList[2] = letter
                elif number == 3:
                    button4["text"] = letter
                    buttonsList[3] = letter
                elif number == 4:
                    button5["text"] = letter
                    buttonsList[4] = letter
                elif number == 5:
                    button6["text"] = letter
                    buttonsList[5] = letter
                elif number == 6:
                    button7["text"] = letter
                    buttonsList[6] = letter
                elif number == 7:
                    button8["text"] = letter
                    buttonsList[7] = letter
                elif number == 8:
                    button9["text"] = letter
                    buttonsList[8] = letter

            
            def buttonNumAssignment(buttonValU):
                """Checks whether the AI has an 'X' or 'O' game value before assigning values to the game board"""
                if bclick[0] == True:
                    buttonCheckAssignment("X", buttonValU)
                    bclick[0] = False
                else:
                    buttonCheckAssignment("O", buttonValU)
                    bclick[0] = True
                
            if scoreChecker() == None: #If the scorechecker has returned None, means that no win conditions have been met AND the board isn't full, so the AI can make a move           
                if AISelectionBool[0] == True:
                    randNum = randint(0,8) #Generates a random number between 0 and 8 and assigns it to randNum
                    randomButton = buttonsList[randNum] #Grabs the value stored in the list position from the randomly generated number             
                    if randomButton != " ": #Compares the value in the game values list, looking for an empty space to play the random move
                        AIRunCheck() #If the value is not empty, runs all the code again, to generate another random number and will repeat until it does
                    else:
                        buttonNumAssignment(randNum) #As the code makes it to here, it means it has found an empty value to put the random AI's move.
                            
        if buttonsList[listValue] == " " and bclick[0] == True:           
            
            if AISelectionBool[0] == True: #If playing against the AI, no other checks have to be made and so can straight away assign the players move to the board and the game win check list

                button["text"] = "X" #Assigns the button value visually to the player as 'X'
                buttonsList[listValue] = "X" #Assings the value in the game win check list to 'X' for comparisons later
                bclick[0] = False #After making a move, changes the bool value which determines whether an 'X' or 'O' is placed on the board to the opposite value for the opponent move
                AIRunCheck() #Makes it the AI's turn to make a move
                scoreChecker() #Checks for a win condition after AI's move has been made
                print(buttonsList) #Debug
                print(bclick) #Debug

            elif clientNo == 10:
                button["text"] = "X" #Assigns the button value visually to the player as 'X'
                buttonsList[listValue] = "X" #Assings the value in the game win check list to 'X' for comparisons later
                bclick[0] = False #After making a move, changes the bool value which determines whether an 'X' or 'O' is placed on the board to the opposite value for the opponent move
                scoreChecker() #Checks for a win condition after players move has been made
                print(buttonsList) #Debug
                print(bclick) #Debug

            else:
                if yourTurn[0] == False: #Waits for opponents move
                    print(yourTurn) #Debug
                    messages = c.poll() #Grabs all messages sent to the client from the server
                    sleep(2)
                    print(messages) #Debug
                    sleep(3) #Gives the server time to send a message back  
                    if len(messages) == 0: #If the server hasn't sent a message to update the game tiles and player move, it can be the users turn
                        messagebox.showinfo("IT IS NOT YOUR TURN","PLEASE WAIT FOR IT TO BE YOUR TURN. TO RECEIVE AN UPDATE FROM YOUR OPPONENT, TRY TO MAKE A MOVE")
                    else:
                        firstMessage = messages[0]
                        print(yourTurn) #Debug
                        if clientNo == 0:
                            if(firstMessage[36:37] == '1'): #Checks if last message received was from opponent, and if so, runs the opponent board game updates
                                opponentButtonVal = (int(firstMessage[49:50])-1) #Which button the opponent chose
                                opponentLetter = firstMessage[16:17] #What game value the other player is (X or O)
                                opponentTurn(opponentButtonVal, opponentLetter) #Runs the opponentTurn function with their inputs
                                scoreChecker() #Checks if the opponents move made them win
                                yourTurn[0] = True #Makes it your turn
                                messages = c.poll()
                        elif clientNo == 1:
                            if(firstMessage[36:37] == '0'): #Checks if last message received was from opponent, and if so, runs the opponent board game updates
                                opponentButtonVal = (int(firstMessage[49:50])-1) #Which button the opponent chose
                                opponentLetter = firstMessage[16:17] #What game value the other player is (X or O)
                                opponentTurn(opponentButtonVal, opponentLetter) #Runs the opponentTurn function with their inputs
                                scoreChecker() #Checks if the opponents move made them win
                                yourTurn[0] = True #Makes it your turn
                                messages = c.poll()
                                
                else: #If this runs, it means it's your turn
                    print(yourTurn) #Debug
                    c.send_message("SENDING X VALUE FOR BUTTON " + str((listValue + 1))) #Sends your move to the server
                    print(clientNo) #Debug
                    yourTurn[0] = False #Makes it not your turn

                    messages = c.poll() #Grabs all messages sent to the client from the server
                    sleep(3) #Gives the server time to send a message back           
                    messages = c.poll() #Clears messages
                    print(messages) #Debug
                    
                    button["text"] = "X" #Visually updates the board to the player with their value
                    buttonsList[listValue] = "X" #Updates the game win check list with their value
                    scoreChecker() #Checks if your move made you win the game
            
        elif buttonsList[listValue] == " " and bclick[0] == False: #Checks if the button has a value in it or not
            
            if AISelectionBool[0] == True:
                
                button["text"] = "O" #Assigns the button value visually to the player as 'O'
                buttonsList[listValue] = "O" #Assings the value in the game win check list to 'O' for comparisons later
                bclick[0] = True #After making a move, changes the bool value which determines whether an 'X' or 'O' is placed on the board to the opposite value for the opponent move
                AIRunCheck() #Makes it the AI's turn to make a move
                scoreChecker() #Checks for a win condition after AI's move has been made
                print(buttonsList) #Debug
                print(bclick) #Debug

            elif clientNo == 10:
                button["text"] = "O" #Assigns the button value visually to the player as 'O'
                buttonsList[listValue] = "O" #Assings the value in the game win check list to 'O' for comparisons later
                bclick[0] = True #After making a move, changes the bool value which determines whether an 'X' or 'O' is placed on the board to the opposite value for the opponent move
                scoreChecker() #Checks for a win condition after players move has been made
                print(buttonsList) #Debug
                print(bclick) #Debug

            else:
                if yourTurn[0] == False: #Waits for opponents move
                    print(yourTurn) #Debug
                    messages = c.poll() #Grabs all messages sent to the client from the server
                    sleep(2)
                    print(messages) #Debug
                    sleep(3) #Gives the server time to send a message back        
                    if len(messages) == 0: #If the server hasn't sent a message to update the game tiles and player move, it can be the users turn
                        messagebox.showinfo("IT IS NOT YOUR TURN","PLEASE WAIT FOR IT TO BE YOUR TURN. TO RECEIVE AN UPDATE FROM YOUR OPPONENT, TRY TO MAKE A MOVE")
                    else:
                        firstMessage = messages[0]
                        print(yourTurn) #Debug
                        if clientNo == 0:
                            if(firstMessage[36:37] == '1'):  #Checks if last message received was from opponent, and if so, runs the opponent board game updates
                                opponentButtonVal = (int(firstMessage[49:50]) - 1) #Which button the opponent chose
                                opponentLetter = firstMessage[16:17] #What game value the other player is (X or O)
                                opponentTurn(opponentButtonVal, opponentLetter) #Runs the opponentTurn function with their inputs
                                scoreChecker() #Checks if the opponents move made them win
                                yourTurn[0] = True #Makes it your turn
                                messages = c.poll()
                        elif clientNo == 1:
                            if(firstMessage[36:37] == '0'):  #Checks if last message received was from opponent, and if so, runs the opponent board game updates
                                opponentButtonVal = (int(firstMessage[49:50])-1) #Which button the opponent chose
                                opponentLetter = firstMessage[16:17] #What game value the other player is (X or O)
                                opponentTurn(opponentButtonVal, opponentLetter) #Runs the opponentTurn function with their inputs
                                scoreChecker() #Checks if the opponents move made them win
                                yourTurn[0] = True #Makes it your turn
                                messages = c.poll()
                  
                else: #If this runs, it means it's your turn
                    print(yourTurn) #Debug
                    c.send_message("SENDING O VALUE FOR BUTTON " + str((listValue + 1))) #Sends your move to the server
                    yourTurn[0] = False #Makes it not your turn

                    messages = c.poll() #Grabs all messages sent to the client from the server
                    sleep(3) #Gives the server time to send a message back       
                    messages = c.poll() #Clears messages
                    print(messages) #Debug
                    
                    button["text"] = "O" #Visually updates the board to the player with their value
                    buttonsList[listValue] = "O" #Updates the game win check list with their value
                    scoreChecker() #Checks if your move made you win the game
     
    def scoreChecker(): #Checks all possible combinations for a win
        """Checks all possible combinations for a win condition, alongside updating the score label visually to the player"""
        if(buttonsList[0] == "X" and buttonsList[1] == "X" and buttonsList[2] == "X" or
             buttonsList[0] == "X" and buttonsList[4] == "X" and buttonsList[8] == "X" or
             buttonsList[0] == "X" and buttonsList[3] == "X" and buttonsList[6] == "X" or
             buttonsList[3] == "X" and buttonsList[4] == "X" and buttonsList[5] == "X" or
             buttonsList[6] == "X" and buttonsList[7] == "X" and buttonsList[8] == "X" or
             buttonsList[2] == "X" and buttonsList[4] == "X" and buttonsList[6] == "X" or
             buttonsList[1] == "X" and buttonsList[4] == "X" and buttonsList[7] == "X" or
             buttonsList[2] == "X" and buttonsList[5] == "X" and buttonsList[8] == "X" ):
             messagebox.showinfo("THE WINNER IS X","PLAYER X WON THE GAME")
             xCurrentScoreList[0] = xCurrentScoreList[0] + 1 #Gives a point to the player playing with the 'X' value
             clearBoard() #Resets the board
             xCurrentScore.set("X's Score:   " + str(xCurrentScoreList[0])) #Updates the 'X' score label
             master.withdraw() #Makes the game board invisible so player can't update any board values and potentially break the game while trying to determine game type
             computerOrAI() #Runs the window which determines whether the player wishes to play against the random AI computer or another player
             
        elif(buttonsList[0] == "O" and buttonsList[1] == "O" and buttonsList[2] == "O" or
            buttonsList[0] == "O" and buttonsList[4] == "O" and buttonsList[8] == "O" or
            buttonsList[0] == "O" and buttonsList[3] == "O" and buttonsList[6] == "O" or
            buttonsList[3] == "O" and buttonsList[4] == "O" and buttonsList[5] == "O" or
            buttonsList[6] == "O" and buttonsList[7] == "O" and buttonsList[8] == "O" or
            buttonsList[2] == "O" and buttonsList[4] == "O" and buttonsList[6] == "O" or
            buttonsList[1] == "O" and buttonsList[4] == "O" and buttonsList[7] == "O" or
            buttonsList[2] == "O" and buttonsList[5] == "O" and buttonsList[8] == "O" ):
            messagebox.showinfo("THE WINNER IS O","PLAYER O WON THE GAME")
            oCurrentScoreList[0] = oCurrentScoreList[0] + 1 #Gives a point to the player playing with the 'O' value
            clearBoard() #Resets the board
            oCurrentScore.set("O's Score:   " + str(oCurrentScoreList[0])) #Updates the 'O' score label
            master.withdraw() #Makes the game board invisible so player can't update any board values and potentially break the game while trying to determine game type
            computerOrAI() #Runs the window which determines whether the player wishes to play against the random AI computer or another player
             
        elif((buttonsList[0] == "O" or buttonsList[0] == "X") and (buttonsList[1] == "O" or
             buttonsList[1] == "X") and (buttonsList[2] == "O" or buttonsList[2] == "X") and
             (buttonsList[3] == "O" or buttonsList[3] == "X") and (buttonsList[4] == "O" or
             buttonsList[4] == "X") and (buttonsList[5] == "O" or buttonsList[5] == "X") and
             (buttonsList[6] == "O" or buttonsList[6] == "X") and (buttonsList[7] == "O" or
             buttonsList[7] == "X") and (buttonsList[8] == "O" or buttonsList[8] == "X") ):
             messagebox.showinfo("NOBODY WINS","THE GAME IS A TIE")
             clearBoard() #Resets the board
             master.withdraw() #Makes the game board invisible so player can't update any board values and potentially break the game while trying to determine game type
             computerOrAI() #Runs the window which determines whether the player wishes to play against the random AI computer or another player

        else:
            return None #If win conditions haven't been met, None value is passed up to be used in earlier functions

    def clearBoard():
        """Resets the board to a default state in the list and the actual button text"""
        buttonsList[0] = " " #Resets each value in the game win check list back to nothing so the game can reset
        buttonsList[1] = " " # - A for loop could have probably been used here, but time constraits just made it easier to change each individual list value
        buttonsList[2] = " " # If there were more values in the list, a for loop would have been used but due to the small, fixed length of the list this approach was taken
        buttonsList[3] = " "
        buttonsList[4] = " "
        buttonsList[5] = " "
        buttonsList[6] = " "
        buttonsList[7] = " "
        buttonsList[8] = " "
        button1["text"] = " " #Resets each visual button value back to nothing so the game can reset
        button2["text"] = " " #Couldn't figure out how to append each button number to the word 'button', e.g. button+1+["text"], etc . so each button is manually reset
        button3["text"] = " "
        button4["text"] = " "
        button5["text"] = " "
        button6["text"] = " "
        button7["text"] = " "
        button8["text"] = " "
        button9["text"] = " "

    computerOrAI() #Runs the window which determines whether the player wishes to play against the random AI computer or another player

    master.protocol("WM_DELETE_WINDOW", on_closing) #Generates an event for when the user presses the close button on the window
    master.mainloop() #Runs the first initial loop for the game