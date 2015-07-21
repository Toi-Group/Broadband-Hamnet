#header files

import tkinter as tk #tkinter is a GUI support package
#as tk renames tkinter as tk for ease

class Application(tk.Frame): #application class must inherit from Tkinter's frame class
   
     def __init__(self, master=None):
        tk.Frame.__init__(self, master) #calls the constructor
        
        self.grid() #necessary for app to appear on the screen
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',
              command= self.quit) #creates the quit button
       
         self.quitButton.grid() #puts the button on the app

app = Application() #the main program starts here
app.master.title('Quit Button Application') #creates the title of the window
app.mainloop() #waiting for keyboard/mouse
