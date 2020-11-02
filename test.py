import julia
#julia.install()
from julia import api
import time
import numpy
start_time = time.time()
num_rows = 6000
num_columns = 6000
array1 = numpy.random.random((num_rows, num_columns))
array2 = numpy.random.random((num_rows, num_columns))
y = numpy.dot(array1,array2)
print(f"--- {time.time() - start_time} seconds ---")
start_time = time.time()
array1 @ array2
print(f"--- {time.time() - start_time} seconds ---")
j = julia.Julia()
dot = j.include("dot.jl")
print(dot)
start_time = time.time()
dot(array1, array2)
print(f"--- {time.time() - start_time} seconds ---")
