"""
  simpleScorejl(array, player)

  Counts the number of tiles belonging to a player after a play has been made.
  Penalizes for number of tiles beloning to the opposite player.

  Parameters
  array : the current board
  player : the current player

  Returns
  Score of the board
"""
function simpleScorejl(array, player)
  score = 0
  #Set player and opponent colours

  if player==1
    colour="b"
    opponent="w"
  else
    colour = "w"
    opponent = "b"
  end
  #+1 if it's player colour, -1 if it's opponent colour
  for x in 1:8
    for y in 1:8
      if array[x,y]==colour
        score+=1
      elseif array[x,y]==opponent
        score-=1
      end
    end
  end
  return score
end

"""
  slightyLessSimpleScorejl(array, player)

  Counts the number of tiles belonging to a player after a play has been made.
  Puts more weight on owning edges and corners.

  Parameters
  array : the current board
  player : the current player

  Returns
  Score of the board
"""
function slightlyLessSimpleScorejl(array,player)
  score = 0
  #Set player and opponent colours
  if player==1
    colour="b"
    opponent="w"
  else
    colour = "w"
    opponent = "b"
  end
  #Go through all the tiles  
  for x in 1:8
    for y in 1:8
      #Normal tiles worth 1
      add = 1
      #Edge tiles worth 3
      if (
        (x==1 && 2<y<7) ||
        (x==8 && 2<y<7) ||
        (y==1 && 2<x<7) ||
        (y==8 && 2<x<7)
      )
        add=3
      #Corner tiles worth 5
      elseif (
        (x==1 && y==1) ||
        (x==1 && y==8) ||
        (x==8 && y==1) ||
        (x==8 && y==8)
      )
        add = 5
      end
      #Add or subtract the value of the tile corresponding to the colour
      if array[x,y]==colour
        score+=add
      elseif array[x,y]==opponent
        score-=add
      end
    end
  end
  return score
end

"""
  decentHuristicjl(array, player)

  Counts the number of tiles belonging to a player after a play has been made.
  Puts more weight on owning edges and corners and penalizses tiles next to
  corners.

  Parameters
  array : the current board
  player : the current player

  Returns
  A score that is the count of tiles held by the current player
"""
function decentHeuristicjl(array,player)
  score = 0
  cornerVal = 25
  adjacentVal = 5
  sideVal = 5
  #Set player && opponent colours
  if player==1
    colour="b"
    opponent="w"
  else
    colour = "w"
    opponent = "b"
  end
  #Go through all the tiles
  for x in 1:8
    for y in 1:8
      #Normal tiles worth 1
      add = 1

      #Adjacent to corners are worth -5
      if (x==1 && y==2) || (x==2 && 1<=y<=2)
        if array[1,1]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      elseif (x==1 && y==7) || (x==2 && 6<=y<=8)
        if array[8,1]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      elseif (x==8 && y==2) || (x==7 && 0<=y<=2)
        if array[1,8]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      elseif (x==8 && y==7) || (x==7 && 7<=y<=8)
        if array[8,8]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      #Edge tiles worth 5
      elseif (
        (x==1 && 2<y<7) ||
        (x==8 && 2<y<7) ||
        (y==1 && 2<x<7) ||
        (y==8 && 2<x<7)
      )
        add=sideVal

      #Corner tiles worth 25
      elseif (
        (x==1 && y==1) ||
        (x==1 && y==8) ||
        (x==8 && y==1) ||
        (x==8 && y==8)
      )
        add = cornerVal
      end
      #Add or subtract the value of the tile corresponding to the colour
      if array[x,y]==colour
        score+=add

      elseif array[x,y]==opponent
        score-=add
      end
    end
  end
  return score
end

"""
  earlyGamejl(array,player)

  Provide a score for a resulting board after a move, use game play tactics
  so that early on you care more about power pieces which allow access to
  corners

  Parameters
  array : the current board
  player : current player number

  Returns:

  score of the board
"""
function earlyGamejl(array,player)
  score = 0
  powerSpotVal = 50
  cornerVal = 25
  adjacentVal = 5
  sideVal = 5
  #Set player and opponent colours
  if player==1
    colour="b"
    opponent="w"
  else
    colour = "w"
    opponent = "b"
  end
  #Go through all the tiles  
  for x in 1:8
    for y in 1:8
      #Normal tiles worth 1
      add = 1

      #Adjacent to corners are worth -5
      if (x==1 && y==2) || (x==2 && 1<=y<=2)
        if array[1,1]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      elseif (x==1 && y==7) || (x==2 && 7<=y<=8)
        if array[8,1]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      elseif (x==8 && y==2) || (x==7 && 1<=y<=2)
        if array[1,8]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      elseif (x==8 && y==7) || (x==7 && 6<=y<=8)
        if array[8,8]==colour
          add = sideVal
        else
          add = -adjacentVal
        end

      #Edge tiles worth 5
      elseif (
        (x==1 && 2<y<7) ||
        (x==8 && 2<y<7) ||
        (y==1 && 2<x<7) ||
        (y==8 && 2<x<7)
      )
        add=sideVal

      #Corner tiles worth 25
      elseif (
        (x==1 && y==1) ||
        (x==2 && y==8) ||
        (x==8 && y==1) ||
        (x==8 && y==8)
      )
        add = cornerVal

      #Power tiles are worth 50
      elseif (
        (x==3 && y==3) ||
        (x==3 && y==6) || 
        (x==6 && y==3) ||
        (x==6 && y==6)
      )
        add = powerSpotVal
      end

      #Add or subtract the value of the tile corresponding to the colour
      if array[x,y]==colour
        score+=add
      elseif array[x,y]==opponent
        score-=add
      end
    end
  end
  return score
end

"""
  finalHeuristic(array,player, moves, valid)

  Heuristic that takes into account the stage of the game, early on you care
  about power pieces, then corners and eventually gaining the most tiles

  Parameters
  array : the current board
  player : current player number
  moves : number of availible moves
  valid : valid function from Python

  Returns:

  score of the board
"""
function finalHeuristicjl(array,player, moves, valid)
  #early game you want the power spots
  if moves<=4
    numMoves = 0
    for x in 1:8
      for y in 1:8
        if valid(array,player,x-1,y-1)
          numMoves += 1
        end
      end
    end
    return numMoves+earlyGamejl(array,player)
  end
  if moves<=8
    numMoves = 0
    for x in 1:8
      for y in 1:8
        if valid(array,player,x-1,y-1)
          numMoves += 1
        end
      end
    end
    return numMoves+decentHeuristicjl(array,player)
  elseif moves<=52
    return decentHeuristicjl(array,player)
  elseif moves<=58
    return slightlyLessSimpleScorejl(array,player)
  else
    return simpleScorejl(array,player)
  end
end

#choose random play
#function getPlays(board, player, move, valid)
#  #Generates all possible moves
#  choices = []
#  boards = []
#  for x in 1:8
#    for y in 1:8
#      if valid(board,player,x-1,y-1)
#        test = move(board,x-1,y-1)
#        append!(boards,test)
#        append!(choices,[x,y])
#      end
#    end
#  end
#  return[choices, boards]
#end