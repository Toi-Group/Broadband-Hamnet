# /python3
# 
# Source: https://www.youtube.com/watch?v=EvbA3qVMGaw
# This program saves a file in the background while the main continues running
# We create our own custom thread class that will be created to take a string and save
# it in the background.

# Async.py 

# Import entire thread module
#
import threading
# Timer for sleep
#
import time


class AsyncWrite(threading.Thread):
	# Text to save and Output to save to
	#
	def __init__(self, text, out):
		threading.Thread.__init__(self)
		self.text = text
		self.out = out
	
	# Run save file
	#
	def run(self):
		# Open the file
		#
		f = open(self.out, "a")
		
		# Write to the file
		#
		f.write(self.text + "\n")
		f.close()
		
		time.sleep(2)
		print("Finished Background file write to {}" .format(self.out))
	
	
def Main():
	message = input("Enter a string to store:")
	background = AsyncWrite(message, 'out.txt')
	background.start()
	
	print("The program can continue to run while it writes in another thread")
	print(100+400)
	
	# Write to thread until thread thread is finished
	#
	background.join()
	print("Waited until thread was complete")
	
if __name__ == '__main__':
	Main()
	