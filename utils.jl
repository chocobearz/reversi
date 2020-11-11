#Checks if a move is valid for a given array.
function valid(
  array,
  player,
  x,
  y
)
  #Sets player colour
  if player==0
    colour="w"
  else
    colour="b"
  end

  #If there's already a piece there, it's an invalid move
  if array[x,y] != nothing
    return false
  else
    #Generating the list of neighbours
    neighbour = false
    neighbours = Any[]
    for  j in max(1,y-1):min(y+1,8)
      for i in max(1,x-1):min(x+1,8)
        if array[i,j] != nothing
          neighbour=true
          push!(neighbours,[i,j])
        end
      end
    end

    #If there's no neighbours, it's an invalid move
    if !neighbour
      return false
    else
      #Iterating through neighbours to determine if at least one line is formed
      valid = false
      for neighbour in neighbours

        neighX = neighbour[1]
        neighY = neighbour[2]
        #If the neighbour colour is equal to your colour, it doesn't form a line
        #Go onto the next neighbour
        if array[neighX,neighY]==colour
          continue
        else
          #Determine the direction of the line
          deltaX = neighX-x
          deltaY = neighY-y
          tempX = neighX
          tempY = neighY
          while 1<=tempX<=8 && 1<=tempY<=8
            #If an empty space, no line is formed
            if array[tempX,tempY]==nothing
              break
            end
            #If it reaches a piece of the player's colour, it forms a line
            if array[tempX,tempY]==colour
              valid=true
              break
            end
            #Move the index according to the direction of the line
            tempX+=deltaX
            tempY+=deltaY
          end
        end
      end
      return valid
    end
  end
end

#FUNCTION: Returns a board after making a move according to rules
#Assumes the move is valid
function move(
  passedArray,
  x,
  y,
  player
)
  #Must copy the passedArray so we don't alter the original
  array = deepcopy(passedArray)
  #Set colour and set the moved location to be that colour
  if player==0
    colour = "w"
  else
    colour="b"
  end

  array[x,y]=colour

  #Determining the neighbours to the square
  neighbours = Any[]
  for j in max(1,y-1):min(y+1,8)
    for i in max(1,x-1):min(x+1,8)
      if array[i,j] != nothing
        push!(neighbours,[i,j])
      end
    end
  end

  #Which tiles to convert
  convert = Any[]

  #For all the generated neighbours, determine if they form a line
  #If a line is formed, we will add it to the convert array
  for neighbour in neighbours
    neighX = neighbour[1]
    neighY = neighbour[2]
    #Check if the neighbour is of a different colour - it must be to form a line
    if array[neighX,neighY]!=colour
      #The path of each individual line
      path = Any[]
      #Determining direction to move
      deltaX = neighX-x
      deltaY = neighY-y

      tempX = neighX
      tempY = neighY

      #While we are in the bounds of the board
      while 1<=tempX<=8 && 1<=tempY<=8
        push!(path,[tempX,tempY])
        value = array[tempX,tempY]
        #If we reach a blank tile, we're done and there's no line
        if value==nothing
          break
        end
        #If we reach a tile of the player's colour, a line is formed
        if value==colour
          #Append all of our path nodes to the convert array
          for node in path
            push!(convert,node)
          end
          break
        end
        #Move the tile
        tempX+=deltaX
        tempY+=deltaY
      end
    end
  end

  #Convert all the appropriate tiles
  for node in convert
    array[node[1],node[2]]=colour
  end
  return array
end

#choose random play
function getPlays(
  board,
  player
)
#Generates all possible moves
choices = Any[]
boards = Any[]
for y in 1:8
  for x in 1:8
    if valid(board,player,x,y)
      test = move(board,x,y, player)
      push!(boards, test)
      push!(choices, [x,y])
    end
  end
end
return[choices, boards]
end
