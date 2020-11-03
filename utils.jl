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
    for i in max(1,x-1):min(x+1,8)
      for j in max(1,y-1):min(y+1,8)
        if array[i,j] != nothing
          neighbour=true
          push!(neighbours,[i,j])
        end
      end
    end
    #If there's no neighbours, it's an invalid move
    if !neighbour
      return false
    end
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
    end
end

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

#choose random play
function getPlays(
    self,
    board
)
  #Generates all possible moves
  choices = zeros(0)
  boards = zeros(0)
  for x in 1:8:
    for y in 1:8:
      if valid(board,self.player,x,y):
        test = move(board,x,y)
        append!(boards, test)
        append!(choices, [x,y])
      end
    end
  end
  return[choices, boards]
end
