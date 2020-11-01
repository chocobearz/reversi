#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Othello Program
# John Fish
# Updated from May 29, 2015 - June 26, 2015
#
# Has both basic AI (random decision) as well as
# educated AI (minimax).
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Library import
from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy
from collections import Counter
import operator

#Variable setup
nodes = 0
depth = 4
difficulty = 0
moves = 0
playouts = 40

#Tkinter setup
root = Tk()
screen = Canvas(
  root,
  width=500,
  height=600,
  background="#222",
  highlightthickness=0
)
screen.pack()

class Board:
  def __init__(self):
    #White goes first (0 is white and player,1 is black and computer)
    self.player = 0
    self.passed = False
    self.won = False
    #Initializing an empty board
    self.array = []
    for x in range(8):
      self.array.append([])
      for y in range(8):
        self.array[x].append(None)

    #Initializing center values
    self.array[3][3]="w"
    self.array[3][4]="b"
    self.array[4][3]="b"
    self.array[4][4]="w"
    #Initializing old values
    self.oldarray = self.array
  #Updating the board to the screen
  def update(self):
    global playouts
    screen.delete("highlight")
    screen.delete("tile")
    for x in range(8):
      for y in range(8):
        #Could replace the circles with images later, if I want
        if self.oldarray[x][y]=="w":
          screen.create_oval(
            54+50*x,54+50*y,96+50*x,96+50*y,
            tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa"
          )
          screen.create_oval(
            54+50*x,52+50*y,96+50*x,94+50*y,
            tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff"
          )

        elif self.oldarray[x][y]=="b":
          screen.create_oval(
            54+50*x,54+50*y,96+50*x,96+50*y,
            tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000"
          )
          screen.create_oval(
            54+50*x,52+50*y,96+50*x,94+50*y,
            tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111"
          )
    #Animation of new tiles
    screen.update()
    for x in range(8):
      for y in range(8):
        #Could replace the circles with images later, if I want
        if self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="w":
          screen.delete("{0}-{1}".format(x,y))
          #42 is width of tile so 21 is half of that
          #Shrinking
          for i in range(21):
            screen.create_oval(
              54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,
              tags="tile animated",fill="#000",outline="#000"
            )
            screen.create_oval(
              54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,
              tags="tile animated",fill="#111",outline="#111"
            )
            if i%3==0:
              sleep(0.01)
            screen.update()
            screen.delete("animated")
          #Growing
          for i in reversed(range(21)):
            screen.create_oval(
              54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,
              tags="tile animated",fill="#aaa",outline="#aaa"
            )
            screen.create_oval(
              54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,
              tags="tile animated",fill="#fff",outline="#fff"
            )
            if i%3==0:
              sleep(0.01)
            screen.update()
            screen.delete("animated")
          screen.create_oval(
            54+50*x,54+50*y,96+50*x,96+50*y,
            tags="tile",fill="#aaa",outline="#aaa"
          )
          screen.create_oval(
            54+50*x,52+50*y,96+50*x,94+50*y,
            tags="tile",fill="#fff",outline="#fff"
          )
          screen.update()

        elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="b":
          screen.delete("{0}-{1}".format(x,y))
          #42 is width of tile so 21 is half of that
          #Shrinking
          for i in range(21):
            screen.create_oval(
              54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,
              tags="tile animated",fill="#aaa",outline="#aaa"
            )
            screen.create_oval(
              54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,
              tags="tile animated",fill="#fff",outline="#fff"
            )
            if i%3==0:
              sleep(0.01)
            screen.update()
            screen.delete("animated")
          #Growing
          for i in reversed(range(21)):
            screen.create_oval(
              54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,
              tags="tile animated",fill="#000",outline="#000"
            )
            screen.create_oval(
              54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,
              tags="tile animated",fill="#111",outline="#111"
            )
            if i%3==0:
              sleep(0.01)
            screen.update()
            screen.delete("animated")

          screen.create_oval(
            54+50*x,54+50*y,96+50*x,96+50*y,
            tags="tile",fill="#000",outline="#000"
          )
          screen.create_oval(
            54+50*x,52+50*y,96+50*x,94+50*y,
            tags="tile",fill="#111",outline="#111"
          )
          screen.update()

    #Drawing of highlight circles
    for x in range(8):
      for y in range(8):
        if self.player == 0:
          if valid(self.array,self.player,x,y):
            screen.create_oval(
              68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),
              tags="highlight",fill="#008000",outline="#008000"
            )

######## MODIFIED BY ME ##############################
    if not self.won:
      #Draw the scoreboard and update the screen
      self.drawScoreBoard()
      screen.update()
      #If the computer is AI, make a move (Other AI is slightly better)
      if self.player==1:
        startTime = time()
        self.oldarray = self.array
        #easy : pure MCTS
        if difficulty == 1 or difficulty == 4:
          simpleMove = self.chooseMove(difficulty)
          if len(simpleMove) == 2:
            self.array = simpleMove[0]
            position = simpleMove[1]
            self.oldarray[position[0]][position[1]]="b"
          else:
            self.array = simpleMove
          #reset player incase it got changed by the playouts
          self.player = 1
        #smartest AI with alpha beta min max pruneing and knowledge of tactics
        else:
          alphaBetaResult = self.alphaBeta(
            self.array,
            depth,
            -float("inf"),
            float("inf"),
            1
          )
          end = time()
          self.array = alphaBetaResult[1]

          if len(alphaBetaResult)==3:
            position = alphaBetaResult[2]
            self.oldarray[position[0]][position[1]]="b"

        self.player = 1-self.player
        deltaTime = round((time()-startTime)*100)/100
        if deltaTime<2:
          sleep(2-deltaTime)
        nodes = 0
        #Player must pass?
        self.passTest()
    else:
      screen.create_text(
        250,550,anchor="c",
        font=("Consolas",15), text="The game is done!"
      )
#### END OF MODIFIED BY ME ####################################

  #Moves to position
  def boardMove(self,x,y):
    global nodes
    #Move and update screen
    self.oldarray = self.array
    self.oldarray[x][y]="w"
    self.array = move(self.array,x,y)
    
    #Switch Player
    self.player = 1-self.player
    self.update()

    #Check if ai must pass
    self.passTest()
    self.update()

  #METHOD: Draws scoreboard to screen
  def drawScoreBoard(self):
    global moves
    #Deleting prior score elements
    screen.delete("score")

    #Scoring based on number of tiles
    player_score = 0
    computer_score = 0
    for x in range(8):
      for y in range(8):
        if self.array[x][y]=="w":
          player_score+=1
        elif self.array[x][y]=="b":
          computer_score+=1

    if self.player==0:
      player_colour = "green"
      computer_colour = "gray"
    else:
      player_colour = "gray"
      computer_colour = "green"

    screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
    screen.create_oval(
      380,540,400,560,
      fill=computer_colour,
      outline=computer_colour
    )

    #Pushing text to screen
    screen.create_text(
      30,550,anchor="w", tags="score",
      font=("Consolas", 50),fill="white",text=player_score
    )
    screen.create_text(
      400,550,anchor="w", tags="score",
      font=("Consolas", 50),fill="black",text=computer_score
    )

    moves = player_score+computer_score

  #METHOD: Test if player must pass: if they do, switch the player
  def passTest(self):
    mustPass = True
    for x in range(8):
      for y in range(8):
        if valid(self.array,self.player,x,y):
          mustPass=False
    if mustPass:
      self.player = 1-self.player
      if self.passed==True:
        self.won = True
      else:
        self.passed = True
      self.update()
    else:
      self.passed = False

  #choose random play
  def getPlays(self, board):
    #Generates all possible moves
    choices = []
    boards = []
    for x in range(8):
      for y in range(8):
        if valid(board,self.player,x,y):
          test = move(board,x,y)
          boards.append(test)
          choices.append([x,y])
    return[choices, boards]

#################this code was written by me#################
  
  #pure mote carlo tree search, level 1 and 2
  def chooseMove(self, difficulty):
    """Choose Move determines what the next optimal move should be, based on the
    maximizing the linear combination from the play statistics of random playouts

    Parameters:

    difficulty(int): difficulty 0 will do pure MCTS and difficulty 4 will use
      tactics to choose the next play

    Returns:

    list : list with the new chosen board and the chosen tile to play
    """
    global playouts
    result_tracker = {}
    current_board = self.array
    current_player = self.player

    play_choices = self.getPlays(current_board)
    empty = play_choices[0]
    #remove empty lists
    empty = [x for x in empty if x != []]
    possible_boards = play_choices[1]
    if len(empty) == 0:
      self.passed = True
      return self.array
    elif len(empty) == 1:
      return(possible_boards[0], empty[0])

    #set up dict for the locations and their win statistics
    for location in range(0, len(empty)):
      result_tracker.setdefault(location, None)

    for empty_location in result_tracker:
      wins = 0
      losses = 0
      draws = 0
      # set number of random playouts
      for playout in range(playouts):
        #incase the player gets changed in the playouts (eg. passing)
        self.player = current_player
        won = False
        passed = self.passed
        mustPass = True
        current_board = possible_boards[empty_location]
        self.player = 1-self.player
        for x in range(8):
          for y in range(8):
            if valid(current_board,self.player,x,y):
              mustPass=False
        if mustPass:
          if passed:
            won = True
          else:
            passed = True
          self.player = 1-self.player

        # all subsequent plays random for both players until game over
        while not won:
          # choose randomly from empty locations
          play_choices = self.getPlays(current_board)
          play_choices = [x for x in play_choices if x != []]
          if len(play_choices) == 0:
            if passed:
              won = True
            else:
              passed = True
            self.player = 1-self.player
            continue
          temp_possible_boards = play_choices[1]
          #pure MCTS
          if difficulty == 1:
            chosen = randint(0,((len(temp_possible_boards))-1))
          #use gameplay tactics
          else:
            bestScore = -float("inf")
            chosen = 0
            for i in range(len(temp_possible_boards)):
              score= finalHeuristic(temp_possible_boards[i],self.player)
              if score>bestScore:
                chosen=i
          current_board = temp_possible_boards[chosen]
          self.player = 1-self.player
          mustPass = True
          for x in range(8):
            for y in range(8):
              if valid(current_board,self.player,x,y):
                mustPass=False
          if mustPass:
            if passed:
              won = True
            else:
              passed = True
            self.player = 1-self.player
        flat_board = [item for sublist in current_board for item in sublist]
        tile_counts = {i:flat_board.count(i) for i in flat_board}
        #number of black tiles
        if 'b' in tile_counts:
          black = tile_counts['b']
        else:
          black = 0
        #number of white tiles
        if 'w' in tile_counts:
          white = tile_counts['w']
        else:
          white = 0

        #increment the relevant stat
        #allowe AI to play against eachother
        if self.player == 1:
          if black > white:
            wins += 1
          elif black == white:
            draws += 1
          elif black < white:
            losses += 1
        else:
          if white > black:
            wins += 1
          elif black == white:
            draws += 1
          elif white < black:
            losses += 1

      #print(
      # "square: {}, wins: {}, draws: {}, losses : {}".format(
      # empty_location,wins, draws, losses
      # )
      #)
      result_tracker[empty_location] = wins + draws*2 - losses*5

    # choose the maximum of the linear combination
    winning_move = max(result_tracker.items(), key=operator.itemgetter(1))[0]
    #print(winning_move)
    #print("run results are: {}".format(result_tracker))
    #print("move choice: {}".format(winning_move))
    # return location with max wins
    return [possible_boards[(winning_move)-1], empty[(winning_move)-1]]

  #alphaBeta pruning on the minimax tree, level 3
  def alphaBeta(self,node,depth,alpha,beta,maximizing):
    """Choose Move determines what the next optimal move should be, based alpha
    beta pruning on a minimax tree

    Parameters:

    node(list): current play board
    depth(int): number of playouts
    alpha(int): previous alpha value
    beta(int): previous beta value
    maximizing(bool): if this playout will minimize or maximize

    Returns:

    list : list with the new chosen board and the chosen tile to play
    """
    global nodes
    nodes += 1
    boards = []
    choices = []

    for x in range(8):
      for y in range(8):
        if valid(self.array,self.player,x,y):
          test = move(node,x,y)
          boards.append(test)
          choices.append([x,y])

    if depth==0 or len(choices)==0:
      return ([finalHeuristic(node,maximizing),node])

    if maximizing:
      v = -float("inf")
      bestBoard = []
      bestChoice = []
      for board in boards:
        boardValue = self.alphaBeta(board,depth-1,alpha,beta,0)[0]
        if boardValue>v:
          v = boardValue
          bestBoard = board
          bestChoice = choices[boards.index(board)]
        alpha = max(alpha,v)
        if beta <= alpha:
          break
      return([v,bestBoard,bestChoice])
    else:
      v = float("inf")
      bestBoard = []
      bestChoice = []
      for board in boards:
        boardValue = self.alphaBeta(board,depth-1,alpha,beta,1)[0]
        if boardValue<v:
          v = boardValue
          bestBoard = board
          bestChoice = choices[boards.index(board)]
        beta = min(beta,v)
        if beta<=alpha:
          break
      return([v,bestBoard,bestChoice])

####### END OF MY CODE #######################

#FUNCTION: Returns a board after making a move according to rules
#Assumes the move is valid
def move(passedArray,x,y):
  #Must copy the passedArray so we don't alter the original
  array = deepcopy(passedArray)
  #Set colour and set the moved location to be that colour
  if board.player==0:
    colour = "w"

  else:
    colour="b"
  array[x][y]=colour

  #Determining the neighbours to the square
  neighbours = []
  for i in range(max(0,x-1),min(x+2,8)):
    for j in range(max(0,y-1),min(y+2,8)):
      if array[i][j]!=None:
        neighbours.append([i,j])

  #Which tiles to convert
  convert = []

  #For all the generated neighbours, determine if they form a line
  #If a line is formed, we will add it to the convert array
  for neighbour in neighbours:
    neighX = neighbour[0]
    neighY = neighbour[1]
    #Check if the neighbour is of a different colour - it must be to form a line
    if array[neighX][neighY]!=colour:
      #The path of each individual line
      path = []

      #Determining direction to move
      deltaX = neighX-x
      deltaY = neighY-y

      tempX = neighX
      tempY = neighY

      #While we are in the bounds of the board
      while 0<=tempX<=7 and 0<=tempY<=7:
        path.append([tempX,tempY])
        value = array[tempX][tempY]
        #If we reach a blank tile, we're done and there's no line
        if value==None:
          break
        #If we reach a tile of the player's colour, a line is formed
        if value==colour:
          #Append all of our path nodes to the convert array
          for node in path:
            convert.append(node)
          break
        #Move the tile
        tempX+=deltaX
        tempY+=deltaY

  #Convert all the appropriate tiles
  for node in convert:
    array[node[0]][node[1]]=colour

  return array

#Method for drawing the gridlines
def drawGridBackground(outline=False):
  #If we want an outline on the board then draw one
  if outline:
    screen.create_rectangle(50,50,450,450,outline="#111")

  #Drawing the intermediate lines
  for i in range(7):
    lineShift = 50+50*(i+1)

    #Horizontal line
    screen.create_line(50,lineShift,450,lineShift,fill="#111")

    #Vertical line
    screen.create_line(lineShift,50,lineShift,450,fill="#111")

  screen.update()

#Simple heuristic. Compares number of each tile.
def simpleScore(array,player):

  score = 0
  #Set player and opponent colours
  if player==1:
    colour="b"
    opponent="w"
  else:
    colour = "w"
    opponent = "b"
  #+1 if it's player colour, -1 if it's opponent colour
  for x in range(8):
    for y in range(8):
      if array[x][y]==colour:
        score+=1
      elif array[x][y]==opponent:
        score-=1
  return score

#Less simple but still simple heuristic. Weights corners and edges as more
def slightlyLessSimpleScore(array,player):
  score = 0
  #Set player and opponent colours
  if player==1:
    colour="b"
    opponent="w"
  else:
    colour = "w"
    opponent = "b"
  #Go through all the tiles  
  for x in range(8):
    for y in range(8):
      #Normal tiles worth 1
      add = 1
      #Edge tiles worth 3
      if (
        (x==0 and 1<y<6) or
        (x==7 and 1<y<6) or
        (y==0 and 1<x<6) or
        (y==7 and 1<x<6)
      ):
        add=3
      #Corner tiles worth 5
      elif (
        (x==0 and y==0) or
        (x==0 and y==7) or
        (x==7 and y==0) or
        (x==7 and y==7)
      ):
        add = 5
      #Add or subtract the value of the tile corresponding to the colour
      if array[x][y]==colour:
        score+=add
      elif array[x][y]==opponent:
        score-=add
  return score

#Heuristic that weights corner tiles and edge tiles as positive
#adjacent to corners (if the corner is not yours) as negative
#Weights other tiles as one point
def decentHeuristic(array,player):
  score = 0
  cornerVal = 25
  adjacentVal = 5
  sideVal = 5
  #Set player and opponent colours
  if player==1:
    colour="b"
    opponent="w"
  else:
    colour = "w"
    opponent = "b"
  #Go through all the tiles
  for x in range(8):
    for y in range(8):
      #Normal tiles worth 1
      add = 1

      #Adjacent to corners are worth -5
      if (x==0 and y==1) or (x==1 and 0<=y<=1):
        if array[0][0]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      elif (x==0 and y==6) or (x==1 and 6<=y<=7):
        if array[7][0]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      elif (x==7 and y==1) or (x==6 and 0<=y<=1):
        if array[0][7]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      elif (x==7 and y==6) or (x==6 and 6<=y<=7):
        if array[7][7]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      #Edge tiles worth 5
      elif (
        (x==0 and 1<y<6) or
        (x==7 and 1<y<6) or
        (y==0 and 1<x<6) or
        (y==7 and 1<x<6)
      ):
        add=sideVal

      #Corner tiles worth 25
      elif (
        (x==0 and y==0) or
        (x==0 and y==7) or
        (x==7 and y==0) or
        (x==7 and y==7)
      ):
        add = cornerVal

      #Add or subtract the value of the tile corresponding to the colour
      if array[x][y]==colour:
        score+=add

      elif array[x][y]==opponent:
        score-=add

  return score

### MY ALTERED CODE############################################################
def earlyGame(array,player):
  """Provide a score for a resulting board after a move, use game play tactics
    so that early on you care more about power pieces which allow access to
    corners

  Parameters:

    array(list): the current board
    player(int): current player number

    Returns:

    int : score of the board
    """
  score = 0
  powerSpotVal = 50
  cornerVal = 25
  adjacentVal = 5
  sideVal = 5
  #Set player and opponent colours
  if player==1:
    colour="b"
    opponent="w"
  else:
    colour = "w"
    opponent = "b"
    #Go through all the tiles  
  for x in range(8):
    for y in range(8):
      #Normal tiles worth 1
      add = 1

      #Adjacent to corners are worth -5
      if (x==0 and y==1) or (x==1 and 0<=y<=1):
        if array[0][0]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      elif (x==0 and y==6) or (x==1 and 6<=y<=7):
        if array[7][0]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      elif (x==7 and y==1) or (x==6 and 0<=y<=1):
        if array[0][7]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      elif (x==7 and y==6) or (x==6 and 6<=y<=7):
        if array[7][7]==colour:
          add = sideVal
        else:
          add = -adjacentVal

      #Edge tiles worth 5
      elif (
        (x==0 and 1<y<6) or
        (x==7 and 1<y<6) or
        (y==0 and 1<x<6) or
        (y==7 and 1<x<6)
      ):
        add=sideVal

      #Corner tiles worth 25
      elif (
        (x==0 and y==0) or
        (x==0 and y==7) or
        (x==7 and y==0) or
        (x==7 and y==7)
      ):
        add = cornerVal

      #Power tiles are worth 50
      elif (
        (x==2 and y==2) or
        (x==2 and y==5) or 
        (x==5 and y==2) or
        (x==5 and y==5)
      ):
        add = powerSpotVal

      #Add or subtract the value of the tile corresponding to the colour
      if array[x][y]==colour:
        score+=add
      elif array[x][y]==opponent:
        score-=add
  return score

def finalHeuristic(array,player):
  """Heuristic that takes into account the stage of the game, early on you care
    about power pieces, then corners and eventually gaining the most tiles

  Parameters:

    array(list): the current board
    player(int): current player number

    Returns:

    int : score of the board
    """
  #early game you want the power spots
  if moves<=4:
    numMoves = 0
    for x in range(8):
      for y in range(8):
        if valid(array,player,x,y):
          numMoves += 1
    return numMoves+earlyGame(array,player)
  if moves<=8:
    numMoves = 0
    for x in range(8):
      for y in range(8):
        if valid(array,player,x,y):
          numMoves += 1
    return numMoves+decentHeuristic(array,player)
  elif moves<=52:
    return decentHeuristic(array,player)
  elif moves<=58:
    return slightlyLessSimpleScore(array,player)
  else:
    return simpleScore(array,player)

##### END MY ALTERED CODE####################################################

#Checks if a move is valid for a given array.
def valid(array,player,x,y):
  #Sets player colour
  if player==0:
    colour="w"
  else:
    colour="b"

  #If there's already a piece there, it's an invalid move
  if array[x][y]!=None:
    return False

  else:
    #Generating the list of neighbours
    neighbour = False
    neighbours = []
    for i in range(max(0,x-1),min(x+2,8)):
      for j in range(max(0,y-1),min(y+2,8)):
        if array[i][j]!=None:
          neighbour=True
          neighbours.append([i,j])
    #If there's no neighbours, it's an invalid move
    if not neighbour:
      return False
    else:
      #Iterating through neighbours to determine if at least one line is formed
      valid = False
      for neighbour in neighbours:

        neighX = neighbour[0]
        neighY = neighbour[1]
        
        #If the neighbour colour is equal to your colour, it doesn't form a line
        #Go onto the next neighbour
        if array[neighX][neighY]==colour:
          continue
        else:
          #Determine the direction of the line
          deltaX = neighX-x
          deltaY = neighY-y
          tempX = neighX
          tempY = neighY

          while 0<=tempX<=7 and 0<=tempY<=7:
            #If an empty space, no line is formed
            if array[tempX][tempY]==None:
              break
            #If it reaches a piece of the player's colour, it forms a line
            if array[tempX][tempY]==colour:
              valid=True
              break
            #Move the index according to the direction of the line
            tempX+=deltaX
            tempY+=deltaY
      return valid

#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
  global difficulty
  xMouse = event.x
  yMouse = event.y
  if running:
    if xMouse>=450 and yMouse<=50:
      root.destroy()
    elif xMouse<=50 and yMouse<=50:
      playGame()
    else:
      #Is it the player's turn?
      if board.player==0:
        #Delete the highlights
        x = int((event.x-50)/50)
        y = int((event.y-50)/50)
        #Determine the grid index for where the mouse was clicked
        
        #If the click is inside the bounds and the move is valid, move to that
        #location
        if 0<=x<=7 and 0<=y<=7:
          if valid(board.array,board.player,x,y):
            board.boardMove(x,y)
  else:
    #Difficulty clicking
    if 300<=yMouse<=350:
      #One star
      if 25<=xMouse<=155:
        difficulty = 1
        playGame()
      #Two star
      elif 180<=xMouse<=310:
        difficulty = 4
        playGame()
      #Three star
      elif 335<=xMouse<=465:
        difficulty = 6
        playGame()

def keyHandle(event):
  symbol = event.keysym
  if symbol.lower()=="r":
    playGame()
  elif symbol.lower()=="q":
    root.destroy()

def create_buttons():
    #Restart button
    #Background/shadow
    screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
    screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")

    #Arrow
    screen.create_arc(
      5,5,45,45,fill="#000088",
      width="2",style="arc",outline="white",extent=300
    )
    screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")

    #Quit button
    #Background/shadow
    screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
    screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")
    #"X"
    screen.create_line(455,5,495,45,fill="white",width="3")
    screen.create_line(495,5,455,45,fill="white",width="3")

def runGame():
  global running
  running = False
  #Title and shadow
  screen.create_text(
    250,203,anchor="c",
    text="Reversi",
    font=("Consolas", 50),fill="#aaa"
  )
  screen.create_text(
    250,200,anchor="c",
    text="Reversi",
    font=("Consolas", 50),fill="#fff"
  )

  #Creating the difficulty buttons
  for i in range(3):
    #Background
    screen.create_rectangle(
      25+155*i, 310, 155+155*i, 355,
      fill="#000", outline="#000"
    )
    screen.create_rectangle(
      25+155*i, 300, 155+155*i, 350,
      fill="#111", outline="#111"
    )

    spacing = 130/(i+2)
    for x in range(i+1):
      #Star with double shadow
      screen.create_text(
        25+(x+1)*spacing+155*i,326,
        anchor="c",text="\u2605",
        font=("Consolas", 25),fill="#b29600"
      )
      screen.create_text(
        25+(x+1)*spacing+155*i,327,
        anchor="c",text="\u2605",
        font=("Consolas",25),fill="#b29600"
      )
      screen.create_text(
        25+(x+1)*spacing+155*i,325,
        anchor="c",text="\u2605",
        font=("Consolas", 25),fill="#ffd700"
      )

  screen.update()

def playGame():
  global board, running
  running = True
  screen.delete(ALL)
  create_buttons()
  board = 0

  #Draw the background
  drawGridBackground()

  #Create the board and update it
  board = Board()
  board.update()

runGame()

#Binding, setting
screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()

#Run forever
root.wm_title("Reversi")
root.mainloop()
