import os

from tkinter import Tk, Label, Button, Entry, Radiobutton, IntVar, Checkbutton, Menu

import webbrowser

from labyrinth_explorer import game

class GUI:
    def __init__(self, master):
        self.master = master
        self.menuBar = Menu(self.master)
        self.menuBar.add_command(label="Results", command=self.showResults)
        self.menuBar.add_command(label="Help", command=self.showHelp)
        self.menuBar.add_command(label="Quit", command=root.quit)
        master.title("Maze Searcher")
        self.method = IntVar()
        self.method.set(0)
        self.filterAct = IntVar()
        self.filterAct.set(0)

        self.mazeWidthLabel = Label(master, text="Maze Width")
        self.mazeWidthEntry = Entry(master)
        
        self.mazeHeightLabel = Label(master, text="Maze Height")
        self.mazeHeightEntry = Entry(master)

        self.searchMethodLabel = Label(master, text="Search Method")

        self.bfts = Radiobutton(master, text = "Breadth First Tree Search",variable=self.method, value=0)
        self.bfgs = Radiobutton(master, text = "Breadth First Graph Search",variable=self.method, value=1)
        self.dfts = Radiobutton(master, text = "Depth First Tree Search",variable=self.method, value=2)
        self.dfgs = Radiobutton(master, text = "Depth First Graph Search",variable=self.method, value=3)
        self.ucs = Radiobutton(master, text = "Uniform-Cost Search",variable=self.method, value=4)
        self.ids = Radiobutton(master, text = "Iterative Deepening Search",variable=self.method, value=5)
        self.gts = Radiobutton(master, text = "Greedy Tree Search",variable=self.method, value=6)
        self.ggs = Radiobutton(master, text = "Greedy Graph Search",variable=self.method, value=7)
        self.asts = Radiobutton(master, text = "A* Tree Search",variable=self.method, value=8)
        self.asgs = Radiobutton(master, text = "A* Graph Search",variable=self.method, value=9)

        self.filterActions = Checkbutton(master, text="Filter actions?", variable=self.filterAct)


        self.button = Button(master, text="Start", command=self.start)

        self.errorLabel = Label(master, text="Enter Values")

        self.mazeWidthLabel.grid(row=0, column=0, columnspan=1)
        self.mazeWidthEntry.grid(row=0, column=1, columnspan=1)
        self.mazeHeightLabel.grid(row=1, column=0, columnspan=1)
        self.mazeHeightEntry.grid(row=1, column=1, columnspan=1)
        self.searchMethodLabel.grid(row=2, column=0, columnspan=2)
        self.bfts.grid(row=3, column=0, columnspan=1)
        self.bfgs.grid(row=3, column=1, columnspan=1)
        self.dfts.grid(row=4, column=0, columnspan=1)
        self.dfgs.grid(row=4, column=1, columnspan=1)
        self.ucs.grid(row=5, column=0, columnspan=1)
        self.ids.grid(row=5, column=1, columnspan=1)
        self.gts.grid(row=6, column=0, columnspan=1)
        self.ggs.grid(row=6, column=1, columnspan=1)
        self.asts.grid(row=7, column=0, columnspan=1)
        self.asgs.grid(row=7, column=1, columnspan=1)
        self.filterActions.grid(row=8, column=0, columnspan=2)
        self.button.grid(row=9, column=0, columnspan=2)
        self.errorLabel.grid(row=10, column=0, columnspan=2)

        master.config(menu=self.menuBar)


    def start(self):
        try:
            method = self.method.get()
            width = int(self.mazeWidthEntry.get())
            height = int(self.mazeHeightEntry.get())
            filterActionsValue = self.filterAct.get()
            if(height<1 and width<1):
                raise ArithmeticError
            game(method,filterActionsValue,width,height)
            self.errorLabel['text']="Enter new values or test different algorithms"
        except(ValueError):
            self.errorLabel['text']="Enter numerical values in width and height"
        except(ArithmeticError):
            self.errorLabel['text']="Enter positive width and height values"

    def showHelp(self):
        path  = os.path.join(os.path.dirname(__file__),'help.txt')
        webbrowser.open_new(path)

    def showResults(self):
        path  = os.path.join(os.path.dirname(__file__),'results.txt')
        webbrowser.open_new(path)

root = Tk()
gui = GUI(root)
root.mainloop()