#file for testing the valid function
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
    else
      #Iterating through neighbours to determine if at least one line is formed
      valid = false
      for neighbour in neighbours

        neighX = neighbour[1]
        neighY = neighbour[2]
        print(neighbour)
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