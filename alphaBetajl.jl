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

  if depth==0 || isempty(getPlaysResult[1]) == true
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
      board = boards[i]
      boardValue = alphaBeta(
        board,
        depth-1,
        alpha,
        beta,
        0,
        nodes,
        moves,
        player,
      )[1]
      if boardValue>v
        v = boardValue
        bestBoard = board
        bestChoice = choices[i]
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
      board = boards[i]
      boardValue = alphaBeta(
        board,
        depth-1,
        alpha,
        beta,
        0,
        nodes,
        moves,
        player,
      )[1]
      if boardValue<v
        v = boardValue
        bestBoard = board
        bestChoice = choices[i]
      end
      beta = min(beta,v)
      if beta<=alpha
        break
      end
    end
    #fix for python index at 0
    winningMoveX = bestChoice[1] - 1
    winningMoveY = bestChoice[2] - 1
    winningMove = [winningMoveX, winningMoveY]
    #println(bestBoard,bestChoice)
    return([v,bestBoard,winningMove])
  end
end
