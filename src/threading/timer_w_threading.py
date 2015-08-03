# /python3
#
# This is a example of timer in python
#
# First import threading and time
#
from threading import Thread
import time


def timer(name, delay, repeat):
	# Show user timer has started
	#
	print("Timer: {} Started" .format(name))
	
	# Run timer for specified period of time. 
	#
	while repeat > 0:
		time.sleep(delay)
		print("{}: {}" .format(name, str(time.ctime(time.time()))))
		repeat -= 1
	print("Timer: {} Completed" .format(name))
	
def Main():
	# Create timer threads:
	# First parameter is function, second are the arguments
	#
	t1 = Thread(target=timer, args=("Timer1", 1, 5))
	t2 = Thread(target=timer, args=("Timer2", 2, 5))
	
	# Tell threads to start
	#
	t1.start()
	t2.start()
	
	# Show user that main thread has completed
	#
	print("Main Complete")

if __name__ == '__main__':
	Main()
	