#test random making the same game

import julia
from julia import Main
Main.include('chooseMovejl.jl')
Main.include('utils.jl')

chooseMovejl = Main.chooseMove
randomjl = Main.randomTest

array = [
  [None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None],
  [None, None, "b" , None, None, None, None, None],
  [None, None, None, "b" , "w" , "w" , None, None],
  [None, None, None, "b" , "b" ,  "b", None, None],
  [None, None, "w" , "b" ,  "b", None, None, None],
  [None, None, None, "w" , None, None, None, None],
  [None, None, None, None, "w", None, None, None]
]

x = 4
y = 7
difficulty = 1
playouts = 1
passed = False
player = 0
won = False
oldarray = []
moves = 0


for test in range(1,11):
  print(randomjl())
  if test == 6:
    print("New start")
    array = [
      [None, None, None, None, None, None, None, None],
      [None, None, None, None, None, None, None, None],
      [None, None, "b" , None, None, None, None, None],
      [None, None, None, "b" , "w" , "w" , None, None],
      [None, None, None, "b" , "b" ,  "b", None, None],
      [None, None, "w" , "b" ,  "b", None, None, None],
      [None, None, None, "w" , None, None, None, None],
      [None, None, None, None, "w", None, None, None]
    ]
  oldarray = array
  simpleMove = chooseMovejl(
    array,
    difficulty,
    playouts,
    passed,
    player,
    moves,
    won
  )
  
  if len(simpleMove) == 4 or len(simpleMove) == 3:
    array = simpleMove[0]
    position = simpleMove[1]
    print(f"the player is {player} and the chosen play position is {position}")
    passed = simpleMove[2]
    if player == 1:
      oldarray[position[0]][position[1]]="b"
      #reset player incase it got changed by the playouts
      player = 0
    else:
      oldarray[position[0]][position[1]]="w"
      #reset player incase it got changed by the playouts
      player = 1
  else:
    array = simpleMove[0]
    passed = simpleMove[1]
