include("heuristics.jl")
include("utils.jl")
function chooseMove(
  array,
  difficulty,
  playouts,
  passedin,
  player,
  moves,
  won
)
  current_board = array
  current_player = player
  loopTime = zeros(0)

  play_choices = getPlays(current_board, player)
  if isempty(play_choices[1]) == true
    passedin = true
    return (current_board, passedin)
  end
  empty = play_choices[1]
  possible_boards = play_choices[2]
  if size(empty)[1] == 1
    return(possible_boards[1], empty[1], passedin)
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
      passed = passedin
      mustPass = true
      current_board = possible_boards[empty_location]
      player = 1-player
      for y in 1:8
        for x in 1:8
          if valid(current_board,player,x,y)
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

      # all subsequent plays random for both players until game over
      #= time the while loop, majority of computation is here, the rest is
      fairly negligible =#
      loopCounter = 0
      time = @timed while won != true
        play_choices = []
        # choose randomly from empty locations
        play_choices = getPlays(current_board, player)
        if isempty(play_choices[1]) == true
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
        if difficulty == 1
          chosen = rand(1:size(temp_possible_boards)[1])
        #use gameplay tactics
        else
          bestScore = -Inf
          chosen = 0
          for i in 1:size(temp_possible_boards)[1]
            score= finalHeuristicjl(temp_possible_boards[i],player,moves,valid)
            if score>bestScore
              chosen=i
            end
          end
        end
        current_board = temp_possible_boards[chosen]
        player = 1-player
        mustPass = true
        for y in 1:8
          for x in 1:8
            if valid(current_board,player,x,y)
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
        loopCounter +=1
      end
      # in order to account for some plays having more or less choices
      if loopCounter > 0
        append!(loopTime, (time[2]/(loopCounter)))
      else
        append!(loopTime, 0)
      end
      #flat_board = Iterators.flatten(current_board)
      #println(flat_board)
      tiles = ['w','b']
      tile_counts=Dict([(i,count(x->x==i,current_board)) for i in tiles])
      #number of black tiles
      if haskey(tile_counts, 'b')
        black = tile_counts['b']
      else
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
    end

    #print(
    # "square: {}, wins: {}, draws: {}, losses : {}".format(
    # empty_location,wins, draws, losses
    # )
    #)
    score = wins + draws*2 - losses*5
    result_tracker[empty_location] = score
  end

  playtime = ((sum(loopTime)/length(loopTime)))
  # choose the maximum of the linear combination
  winning_move = findmax(result_tracker)[2]
  #print(winning_move)
  #print("run results are: {}".format(result_tracker))
  #print("move choice: {}".format(winning_move))
  # return location with max wins

  #fix for python index at 0
  winningMoveX = empty[winning_move][1] - 1
  winningMoveY = empty[winning_move][2] - 1
  winningMove = [winningMoveX, winningMoveY]

  return [
    possible_boards[winning_move],
    winningMove,
    passedin,
    playtime
  ]
end
