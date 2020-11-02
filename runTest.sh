#!/bin/bash

#number of playouts to run
declare -a playouts=(1 5 10 50 100)

#models to use
declare -a models=("PMC MC" "PMC AB" "MC AB")


for i in "${models[@]}"
do
  for j in "${playouts[@]}"
  do
    for run in {1..50}
    do
      venv/Scripts/python.exe reversiAI.py $i $j python
      venv/Scripts/python.exe reversijlAI.py $i $j julia
    done
  done
done
