include("heuristics.jl")
include("utils.jl")
function alphaBeta(
  node,
  depth,
  alpha,
  beta,
  maximizing,
  nodes,
  moves,
  player
)
  nodes += 1
  getPlaysResult = getPlays(node, player)

  if depth==0 || isassigned(getPlaysResult, 1) == false
    return ([finalHeuristicjl(node,maximizing, moves, valid),node])
  end

  choices = getPlaysResult[1]
  boards = getPlaysResult[2]

  boardsLength = size(choices)[1]
  #if size(choices)[1] != 1
  #  boardsLength = trunc(Int32, size(choices)[1]/2)
  #else
  #  boardsLength = 1
  #end
  if maximizing != 1
    v = -Inf
    bestBoard = []
    bestChoice = []
    for i in 1:boardsLength
      board = boards[i, :, :]
      boardValue = alphaBeta(
        board,
        depth-1,
        alpha,
        beta,
        0,
        nodes,
        valid,
        moves,
        player,
        getPlays
      )[1]
      if boardValue>v
        v = boardValue
        bestBoard = board
        bestChoice = choices[i,:]
      end
      alpha = max(alpha,v)
      if beta <= alpha
        break
      end
    end
    #println(bestBoard, bestChoice)
    return([v,bestBoard,bestChoice])
  else
    v = Inf
    bestBoard = []
    bestChoice = []
    for i in 1:boardsLength
      board = boards[i, :, :]
      boardValue = alphaBeta(
        board,
        depth-1,
        alpha,
        beta,
        0,
        nodes,
        valid,
        moves,
        player,
        getPlays
      )[1]
      if boardValue<v
        v = boardValue
        bestBoard = board
        bestChoice = choices[i,:]
      end
      beta = min(beta,v)
      if beta<=alpha
        break
      end
    end
    #println(bestBoard,bestChoice)
    return([v,bestBoard,bestChoice])
  end
end
