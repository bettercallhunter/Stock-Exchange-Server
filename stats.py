import pstats

# Load the profiling information for one of the worker processes
stats = pstats.Stats('profile_worker_32537.prof')

# Print a sorted list of the functions and the time spent in each
stats.sort_stats('time').print_stats()

# You can also output the results to a file
with open('profile_results.txt', 'w') as f:
    stats = pstats.Stats('profile_worker_32537.prof', stream=f)
    stats.sort_stats('time').print_stats()
