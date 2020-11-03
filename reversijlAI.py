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
import julia

j = julia.Julia()
chooseMovejl = j.include("chooseMovejl.jl")
alphaBetajl = j.include("alphaBetajl.jl")

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
        simpleMove = chooseMovejl(
          self.array,
          difficulty,
          playouts,
          self.passed,
          self.player,
          moves,
          self.won
        )
        end = time()
        if len(simpleMove) == 4 or len(simpleMove) == 3:
          self.array = simpleMove[0]
          position = simpleMove[1]
          self.passed = simpleMove[2]
          if player == 1:
            self.oldarray[position[0]][position[1]]="b"
            #reset player incase it got changed by the playouts
            self.player = 1
          else:
            self.oldarray[position[0]][position[1]]="w"
            #reset player incase it got changed by the playouts
            self.player = 0
          if len(simpleMove) == 4:
            if difficulty == 1:
              pmctimes.append(end - start)
              pmcscaledtimes.append(simpleMove[3])
            if difficulty == 4:
              mctactimes.append(end - start)
              mctacscaledtimes.append(simpleMove[3])
        else:
          self.array = simpleMove[0]
          self.passed = simpleMove[1]
        #smartest AI with alpha beta min max pruneing and knowledge of tactics
      else:
        start = time()
        alphaBetaResult = alphaBetajl(
          self.array,
          depth,
          -float("inf"),
          float("inf"),
          1,
          nodes,
          move,
          moves,
          self.player
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
      print(pmctimes)
      print(pmcscaledtimes)
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
          "Language" : ["Julia"]
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
          "Language" : ["Julia"]
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
          "Language" : ["Julia"]
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
          "Language" : ["Julia"]
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
          "Language" : ["Julia"]
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
          "Language" : ["Julia"]
        }
        resultsdf = pd.DataFrame(data=results)
        resultsdf.to_csv('results.csv', mode='a', header=False)
      #exit()
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
