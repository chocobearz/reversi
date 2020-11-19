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
from statistics import mean
import operator
import argparse
import pandas as pd

#Variable setup
nodes = 0
depth = 4
moves = 0
pmctimes = []
abtimes = []
mctactimes = []
pmcscaledtimes = []
mctacscaledtimes = []

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

parser = argparse.ArgumentParser()
parser.add_argument(
  "model1",
  help="the AI model to use for player1: PMC, MC, AB"
)
parser.add_argument(
  "model2",
  help="the AI model to use for player2: PMC, MC, AB"
)
parser.add_argument(
  "playouts",
  help="number of playouts for monte carlo models to run and depth for alpha beta"
)
args = parser.parse_args()

playouts = int(args.playouts)
depth = int(args.playouts)

# depth is not the same as playouts and needs to be scaled down
if depth == 5:
  depth = 2
elif depth == 10:
  depth = 5
elif depth == 50:
  depth = 6
elif depth == 100:
  depth = 7
elif depth == 150:
  depth = 7
elif depth == 175:
  depth = 7
elif depth == 200:
  depth = 7

if args.model1 == "PMC":
  P0d = 1
elif args.model1 == "MC":
  P0d = 4
elif args.model1 == "AB":
  P0d = 6
else:
  print("this is not a correct model, please enter one of the following:\n"
  "\"PMC\" : pure monte carlo tree search\n"
  "\"MC\" : monte carlo tree search with heuristics\n"
  "\"AB\" : alpha beta\n")

difficulty = P0d

if args.model2 == "PMC":
  P1d = 1
elif args.model2 == "MC":
  P1d = 4
elif args.model2 == "AB":
  P1d = 6
else:
  print("this is not a correct model, please enter one of the following:\n"
  "\"PMC\" : pure monte carlo tree search\n"
  "\"MC\" : monte carlo tree search with heuristics\n"
  "\"AB\" : alpha beta\n")

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

######## MODIFIED BY ME ##############################
    if not self.won:
      global difficulty
      player = self.player
      #Draw the scoreboard and update the screen
      self.drawScoreBoard()
      screen.update()
      self.oldarray = self.array
      #print(difficulty)
      if difficulty == 1 or difficulty == 4:
        start = time()
        simpleMove = self.chooseMove(difficulty)
        end = time()
        if len(simpleMove) == 3 or len(simpleMove) == 2 :
          self.array = simpleMove[0]
          position = simpleMove[1]
          if player == 1:
            self.oldarray[position[0]][position[1]]="b"
            #reset player incase it got changed by the playouts
            self.player = 1
          else:
            self.oldarray[position[0]][position[1]]="w"
            #reset player incase it got changed by the playouts
            self.player = 0
          if len(simpleMove) == 3:
            if difficulty == 1:
              pmctimes.append(end - start)
              pmcscaledtimes.append(simpleMove[2])
            if difficulty == 4:
              mctactimes.append(end - start)
              mctacscaledtimes.append(simpleMove[2])
        else:
          self.array = simpleMove[0]
      #smartest AI with alpha beta min max pruneing and knowledge of tactics
      else:
        start = time()
        alphaBetaResult = self.alphaBeta(
          self.array,
          depth,
          -float("inf"),
          float("inf"),
          1
        )
        end = time()
        abtimes.append(end-start)
        self.array = alphaBetaResult[1]

        if len(alphaBetaResult)==3:
          position = alphaBetaResult[2]
          if self.player == 1:
            self.oldarray[position[0]][position[1]]="b"
          else:
            self.oldarray[position[0]][position[1]]="w"

      if self.player == 1:
        self.player = 0
        difficulty = P0d
      else:
        self.player = 1
        difficulty = P1d
      nodes = 0
      #Player must pass
      self.passTest()
    else:
      screen.create_text(
        250,550,anchor="c",
        font=("Consolas",15), text="The game is done!"
      )
      #if len(pmctimes):
      #  print(
      #    "time per PMCTS play : {}".format(
      #      (mean(pmctimes))
      #    )
      #  )
      #if len(mctactimes):
      #  print(
      #    "time per MC tactics play : {}".format(
      #      (mean(mctactimes))
      #    )
      #  )
      #if len(abtimes):
      #  print(
      #    "time per alpha beta play : {}".format(
      #      (mean(abtimes))
      #    )
      #  )
      #if len(pmcscaledtimes):
      #  print(
      #    "time per PMCTS playout : {}".format(
      #      (mean(pmcscaledtimes))
      #    )
      #  )
      #if len(mctacscaledtimes):
      #  print(
      #    "time per MC tactics playout : {}".format(
      #      (mean(mctacscaledtimes))
      #    )
      #  )
      if (P0d == 1 and P1d == 4) or (P0d == 4 and P1d == 1):
        pmctimesavg = mean(pmctimes)
        pmcscaledtimesavg = mean(pmcscaledtimes)
        mctactimesavg = mean(mctactimes)
        mctacscaledtimesavg = mean(mctacscaledtimes)
        if P0d == 1:
          if player_score > computer_score:
            winner = "PMC"
          else:
            winner = "MC"
        else:
          if player_score > computer_score:
            winner = "MC"
          else:
            winner = "PMC"
        results = {
          "PMCTS full play" : [pmctimesavg],
          "PMCTS Playout" : [pmcscaledtimesavg],
          "MCTS full play" : [mctactimesavg],
          "MCTS Playout" : [mctacscaledtimesavg],
          "AB full play" : ["NA"],
          "MC vs PMC" : [winner],
          "PMC vs AB" : ["NA"],
          "MC vs AB" : ["NA"],
          "Playouts" : [playouts],
          "Language" : ["Python"]
        }
        resultsdf = pd.DataFrame(data=results)
        resultsdf.to_csv('results.csv', mode='a', header=False)
      elif P0d == 1 and P1d == 1:
        pmctimesavg = mean(pmctimes)
        pmcscaledtimesavg = mean(pmcscaledtimes)
        results = {
          "PMCTS full play" : [pmctimesavg],
          "PMCTS Playout" : [pmcscaledtimesavg],
          "MCTS full play" : ["NA"],
          "MCTS Playout" : ["NA"],
          "AB full play" : ["NA"],
          "MC vs PMC" : ["NA"],
          "PMC vs AB" : ["NA"],
          "MC vs AB" : ["NA"],
          "Playouts" : [playouts],
          "Language" : ["Python"]
        }
        resultsdf = pd.DataFrame(data=results)
        resultsdf.to_csv('results.csv', mode='a', header=False)
      elif (P0d == 1 and P1d == 6) or (P0d == 6 and P1d == 1):
        pmctimesavg = mean(pmctimes)
        pmcscaledtimesavg = mean(pmcscaledtimes)
        abtimesavg = mean(abtimes)
        abscaledtimesavg = 0
        if P0d == 1:
          if player_score > computer_score:
            winner = "PMC"
          else:
            winner = "AB"
        else:
          if player_score > computer_score:
            winner = "AB"
          else:
            winner = "PMC"
        results = {
          "PMCTS full play" : [pmctimesavg],
          "PMCTS Playout" : [pmcscaledtimesavg],
          "MCTS full play" : ["NA"],
          "MCTS Playout" : ["NA"],
          "AB full play" : [abtimesavg],
          "MC vs PMC" : ["NA"],
          "PMC vs AB" : [winner],
          "MC vs AB" : ["NA"],
          "Playouts" : [playouts],
          "Language" : ["Python"]
        }
        resultsdf = pd.DataFrame(data=results)
        resultsdf.to_csv('results.csv', mode='a', header=False)
      elif P0d == 4 and P1d == 4:
        mctactimesavg = mean(mctactimes)
        mctacscaledtimesavg = mean(mctacscaledtimes)
        results = {
          "PMCTS full play" : ["NA"],
          "PMCTS Playout" : ["NA"],
          "MCTS full play" : [mctactimesavg],
          "MCTS Playout" : [mctacscaledtimesavg],
          "AB full play" : ["NA"],
          "MC vs PMC" : ["NA"],
          "PMC vs AB" : ["NA"],
          "MC vs AB" : ["NA"],
          "Playouts" : [playouts],
          "Language" : ["Python"]
        }
        resultsdf = pd.DataFrame(data=results)
        resultsdf.to_csv('results.csv', mode='a', header=False)
      elif (P0d == 4 and P1d == 6) or (P0d == 6 and P1d == 4):
        mctactimesavg = mean(mctactimes)
        mctacscaledtimesavg = mean(mctacscaledtimes)
        abtimesavg = mean(abtimes)
        abscaledtimesavg = 0
        if P0d == 4:
          if player_score > computer_score:
            winner = "MC"
          else:
            winner = "AB"
        else:
          if player_score > computer_score:
            winner = "AB"
          else:
            winner = "MC"
        results = {
          "PMCTS full play" : ["NA"],
          "PMCTS Playout" : ["NA"],
          "MCTS full play" : [mctactimesavg],
          "MCTS Playout" : [mctacscaledtimesavg],
          "AB full play" : [abtimesavg],
          "MC vs PMC" : ["NA"],
          "PMC vs AB" : ["NA"],
          "MC vs AB" : [winner],
          "Playouts" : [playouts],
          "Language" : ["Python"]
        }
        resultsdf = pd.DataFrame(data=results)
        resultsdf.to_csv('results.csv', mode='a', header=False)
      elif (P0d == 6 and P1d == 6):
        abtimesavg = mean(abtimes)
        abscaledtimesavg = 0
        results = {
          "PMCTS full play" : ["NA"],
          "PMCTS Playout" : ["NA"],
          "MCTS full play" : ["NA"],
          "MCTS Playout" : ["NA"],
          "AB full play" : [abtimesavg],
          "MC vs PMC" : ["NA"],
          "PMC vs AB" : ["NA"],
          "MC vs AB" : ["NA"],
          "Playouts" : [playouts],
          "Language" : ["Python"]
        }
        resultsdf = pd.DataFrame(data=results)
        resultsdf.to_csv('results.csv', mode='a', header=False)
      exit()
      #root.destroy()

    if not self.won:
      root.after(0, self.update)
#### END OF MODIFIED BY ME ####################################

  #METHOD: Draws scoreboard to screen
  def drawScoreBoard(self):
    global moves
    global player_score
    global computer_score
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

  #pure monte carlo tree search, level 1 and 2
  def chooseMove(self, difficulty):
    """Choose Move determines what the next optimal move should be, based on the
    maximizing the linear combination from the play statistics of random playouts

    Parameters:

    difficulty(int): difficulty 0 will do pure MCTS and difficulty 4 will use
      tactics to choose the next play

    Returns:

    list : list with the new chosen board, the chosen tile to play and time
    """
    global playouts
    result_tracker = {}
    current_board = self.array
    current_player = self.player
    loopTime = []

    play_choices = self.getPlays(current_board)
    empty = play_choices[0]
    #remove empty lists
    empty = [x for x in empty if x != []]
    possible_boards = play_choices[1]
    if len(empty) == 0:
      self.passed = True
      return [self.array]
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
        ''' time the while loop, majority of computation is here, the rest is
        fairly negligible'''
        start = time()
        loopCounter = 0
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
          loopCounter +=1
        end = time()
        # in order to account for some plays having more or less choices
        if loopCounter:
          loopTime.append((end-start)/(loopCounter))
        else:
          loopTime.append(0)
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
        if current_player == 1:
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
    
    playtime = ((sum(loopTime)/len(loopTime)))
    # choose the maximum of the linear combination
    winning_move = max(result_tracker.items(), key=operator.itemgetter(1))[0]
    #print(winning_move)
    #print("run results are: {}".format(result_tracker))
    #print("move choice: {}".format(winning_move))
    # return location with max wins
    return [
      possible_boards[(winning_move)-1],
      empty[(winning_move)-1],
      playtime
    ]

####### END OF MY CODE #######################

  #alphaBeta pruning on the minimax tree
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
# screen.bind("<Button-1>", clickHandle)
playGame()
screen.bind("<Key>",keyHandle)
screen.focus_set()

#Run forever
###modified###################################
root.wm_title("Reversi")
root.after(0, board.update)
root.mainloop()
