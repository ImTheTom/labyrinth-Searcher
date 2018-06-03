from tkinter import Tk, Label, Button, Entry, Radiobutton, IntVar

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Maze Searcher")
        self.v = IntVar()
        self.v.set(0)

        self.mazeWidthLabel = Label(master, text="Maze Width")
        self.mazeWidthEntry = Entry(master)
        
        self.mazeHeightLabel = Label(master, text="Maze Height")
        self.mazeHeightEntry = Entry(master)

        self.searchMethodLabel = Label(master, text="Search Method")

        self.bfts = Radiobutton(master, text = "Breadth First Tree Search",variable=self.v, value=0)
        self.bfgs = Radiobutton(master, text = "Breadth First Graph Search",variable=self.v, value=1)
        self.dfts = Radiobutton(master, text = "Depth First Tree Search",variable=self.v, value=2)
        self.dfgs = Radiobutton(master, text = "Depth First Graph Search",variable=self.v, value=3)
        self.gts = Radiobutton(master, text = "Greedy Tree Search",variable=self.v, value=4)
        self.ggs = Radiobutton(master, text = "Greedy Graph Search",variable=self.v, value=5)
        self.asts = Radiobutton(master, text = "A* Tree Search",variable=self.v, value=6)
        self.asgs = Radiobutton(master, text = "A* Graph Search",variable=self.v, value=7)
        self.ucs = Radiobutton(master, text = "Uniform-Cost Search",variable=self.v, value=8)
        self.ids = Radiobutton(master, text = "Iterative Deepening Search",variable=self.v, value=9)

        self.button = Button(master, text="Start", command=self.start)

        self.mazeWidthLabel.grid(row=0, column=0, columnspan=1)
        self.mazeWidthEntry.grid(row=0, column=1, columnspan=1)
        self.mazeHeightLabel.grid(row=1, column=0, columnspan=1)
        self.mazeHeightEntry.grid(row=1, column=1, columnspan=1)
        self.searchMethodLabel.grid(row=2, column=0, columnspan=2)
        self.bfts.grid(row=3, column=0, columnspan=1)
        self.bfgs.grid(row=3, column=1, columnspan=1)
        self.dfts.grid(row=4, column=0, columnspan=1)
        self.dfgs.grid(row=4, column=1, columnspan=1)
        self.gts.grid(row=5, column=0, columnspan=1)
        self.ggs.grid(row=5, column=1, columnspan=1)
        self.asts.grid(row=6, column=0, columnspan=1)
        self.asgs.grid(row=6, column=1, columnspan=1)
        self.button.grid(row=7, column=0, columnspan=2)

    def start(self):
        print(self.v.get())
        print(self.mazeWidthEntry.get())
        print(self.mazeHeightEntry.get())
        print("Started")


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()