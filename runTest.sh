#!/bin/bash

#number of playouts to run
declare -a playouts=(1 5 10, 50, 100)
#playouts too high for python
declare -a playouts2=(150 175 200)

#models to use
declare -a models=("PMC MC" "PMC AB" "MC AB")

for i in "${models[@]}"
do
  for j in "${playouts2[@]}"
  do
    for run in {1..20}
    do
      venv/Scripts/python.exe reversiAI.py $i $j
      venv/Scripts/python.exe reversijlAI.py $i $j
    done
  done
done

for i in "${models[@]}"
do
  for j in "${playouts2[@]}"
  do
    for run in {1..20}
    do
      venv/Scripts/python.exe reversijlAI.py $i $j
    done
  done
done
