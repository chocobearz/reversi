include("heuristics.jl")
function chooseMove(
  array,
  depth,
  playouts,
  valid,
  passed,
  player,
  moves,
  getPlays,
  won
)
  current_board = array
  current_player = player
  play_choices = getPlays(current_board)
  if isassigned(play_choices, 1) == false
    passed = true
    return (current_board, passed)
  end
  empty = play_choices[1]
  possible_boards = play_choices[2]
  if size(empty)[1] == 1
    return(possible_boards[1,:,:], empty[1,:], passed)
  end

  len = size(empty)[1]

  #set up dict for the locations and their win statistics
  result_tracker = Dict(i => 100 for i in 1:len)

  for (empty_location, value) in result_tracker
    wins = 0
    losses = 0
    draws = 0
    # set number of random playouts
    for playout in 1:playouts
      #incase the player gets changed in the playouts (eg. passing)
      player = current_player
      won = false
      passed = passed
      mustPass = true
      current_board = possible_boards[empty_location,:,:]
      player = 1-player
      for x in 1:8
        for y in 1:8
          if valid(current_board,player,x-1,y-1)
            mustPass=false
          end
        end
      end
      if mustPass
        if passed
          won = true
        else
          passed = true
        end
        player = 1-player
      end
    end

    # all subsequent plays random for both players until game over
    while won != true
      play_choices = []
      # choose randomly from empty locations
      play_choices = getPlays(current_board)
      if isassigned(play_choices, 1) == false
        if passed
          won = true
        else
          passed = true
        end
        player = 1-player
        continue
      end
      temp_possible_boards = play_choices[2]
      #pure MCTS
      if depth == 1
        chosen = rand(1:size(temp_possible_boards)[1])
      #use gameplay tactics
      else
        bestScore = -Inf
        chosen = 0
        for i in 1:size(temp_possible_boards)[1]
          score= finalHeuristicjl(temp_possible_boards[i,:,:],player,moves,valid)
          if score>bestScore
            chosen=i
          end
        end
      end
      current_board = temp_possible_boards[chosen,:,:]
      player = 1-player
      mustPass = true
      for x in 1:8
        for y in 1:8
          if valid(current_board,player,x-1,y-1)
            mustPass=false
          end
        end
      end
      if mustPass
        if passed
          won = true
        else
          passed = true
        end
        player = 1-player
      end
    end
    #flat_board = Iterators.flatten(current_board)
    #println(flat_board)
    tiles = ['w','b']
    tile_counts=Dict([(i,count(x->x==i,current_board)) for i in tiles])
    #number of black tiles
    if haskey(tile_counts, 'b')
      black = 0
    end
    #number of white tiles
    if haskey(tile_counts, 'w')
      white = tile_counts['w']
    else
      white = 0
    end
    #increment the relevant stat
    #allowe AI to play against eachother
    if current_player == 1
      if black > white
        wins += 1
      elseif black == white
        draws += 1
      elseif black < white
        losses += 1
      end
    else
      if white > black
        wins += 1
      elseif black == white
        draws += 1
      elseif white < black
        losses += 1
      end
    end
    #print(
    # "square: {}, wins: {}, draws: {}, losses : {}".format(
    # empty_location,wins, draws, losses
    # )
    #)
    score = wins + draws*2 - losses*5
    result_tracker[empty_location] = score
  end

  # choose the maximum of the linear combination
  winning_move = findmax(result_tracker)[2]
  #print(winning_move)
  #print("run results are: {}".format(result_tracker))
  #print("move choice: {}".format(winning_move))
  # return location with max wins
  return [possible_boards[winning_move,:,:], empty[winning_move,:], passed]
end
