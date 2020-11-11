#test individual python calls to Julia utils function

import julia

j = julia.Julia()
valid = j.include("valid.jl")
move = j.include("move.jl")

array = [
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, "b" , None, None, None, None, None, None],
  [None, None, None, "b" , "w" , "w" , None, None, None],
  [None, None, None, "b" , "b" ,  "b", None, None, None],
  [None, None, "w" , "b" ,  "b", None, None, None, None],
  [None, None, None, "w" , None, None, None, None, None],
  [None, None, None, None, "w", None, None, None, None]
]

x = 4
y = 7

print(valid(array,1, x, y))

print(move(array, x, y, 1))