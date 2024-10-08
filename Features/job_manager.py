# The function reads one line of arguments from a file and launches code execution.
# It uses FileLock to correctly handle the co-existence of several job_managers in parallel.


from filelock import FileLock, Timeout		# for file locks
import os	# for shell execution of the code
import sys
import socket	# for netowrk hostname
import numpy
from main_df import main

# actual calculations
# from signal import signal, SIGPIPE, SIG_DFL		# To handle broken pipe messages

from constants import args_lock, args_file, lock_timeout
# calculation_script = "main.py"

# # Set Python to ignore absent write pipe for `print` operator
# signal(SIGPIPE,SIG_DFL)


while True:
	# Try to obtain lock
	lock = FileLock(args_lock, timeout = lock_timeout)
	#numpy.savetxt('blabl.txt',[1,2,3,4])
	try:

		# If get lock
		with lock:

			# Read and store all lines in the arguments file
			with open(args_file, 'r') as file_object:
				all_lines = file_object.read().splitlines(True)



			# If arguments file is empty, end program
			if len(all_lines) == 0:
				print("Arguments file empty. Finishing.")
				sys.exit(0)

			# Write all lines back except for the first one
			with open(args_file, 'w') as file_object:
				file_object.writelines(all_lines[1:])

			# Get current arguments and clen
			cur_args = all_lines[0].strip()
			del all_lines

	# If unable to get lock
	except Exception as e:
		print("Ecountered unknown exception while getting the file lock: '"+ e + "'")
		sys.exit(-1)
	# Launch calculation with current arguments
	print("Launching calculations with parameters '" + cur_args + "'")
	main(cur_args)
