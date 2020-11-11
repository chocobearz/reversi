#File for testing the move function
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
    for i in max(1,x-1):min(x+1,8)
      for j in max(1,y-1):min(y+1,8)
        if array[i,j] != nothing
          push!(neighbours,[i,j])
        end
      end
    end
    neighbour = false
    neighbours = Any[]
    for i in max(1,x-1):min(x+1,8)
      for j in max(1,y-1):min(y+1,8)
        if array[i,j]!=nothing
          neighbour=true
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