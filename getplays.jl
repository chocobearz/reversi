#file for testing getplays function
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