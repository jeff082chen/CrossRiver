import time
import tkinter as tk
from PIL import Image, ImageTk
from CrossRiver.setup import setParameter

RIVER_IMG_PATH = 'GUI/img/river.png'
BOAT_IMG_PATH = 'GUI/img/boat.png'

div_size = 200
align_mode = 'nswe' # align center
pad = 3

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Canibals & Missionaries')
        self.resizable(width = False, height = False)

class ControlSystem:
    def __init__(self):
        self.ready = False
        self.lock = False

        self.path = None

        self.boatA_pos = 1
        self.boatB_pos = 1
        self.right_cannibals = 3
        self.right_missionaries = 3
        self.left_cannibals = 0
        self.left_missionaries = 0
        self.boatA_cannibals = 0
        self.boatA_missionaries = 0
        self.boatB_cannibals = 0
        self.boatB_missionaries = 0

    def isValid(self):
        if self.right_cannibals < 0 or self.right_missionaries < 0:
            return False
        if self.left_cannibals < 0 or self.left_missionaries < 0:
            return False
        if self.right_cannibals > self.right_missionaries and self.right_missionaries > 0:
            return False
        if self.left_cannibals > self.left_missionaries and self.left_missionaries > 0:
            return False
        if self.boatA_cannibals > self.boatA_missionaries and self.boatA_missionaries > 0:
            return False
        if self.boatB_cannibals > self.boatB_missionaries and self.boatB_missionaries > 0:
            return False
        return True

    def check_validity(self):
        assert self.isValid(), f"Invalid State Error: {self.right_cannibals} {self.right_missionaries} {self.left_cannibals} {self.left_missionaries} {self.boatA_cannibals} {self.boatA_missionaries} {self.boatB_cannibals} {self.boatB_missionaries}"

    def board_boatA(self, cannibals, missionaries):
        if self.boatA_pos:
            self.right_cannibals -= cannibals
            self.right_missionaries -= missionaries
        else:
            self.left_cannibals -= cannibals
            self.left_missionaries -= missionaries
        self.boatA_cannibals += cannibals
        self.boatA_missionaries += missionaries

    def board_boatB(self, cannibals, missionaries):
        if self.boatB_pos:
            self.right_cannibals -= cannibals
            self.right_missionaries -= missionaries
        else:
            self.left_cannibals -= cannibals
            self.left_missionaries -= missionaries
        self.boatB_cannibals += cannibals
        self.boatB_missionaries += missionaries
    
    def leave_boatA(self):
        if self.boatA_pos:
            self.right_cannibals += self.boatA_cannibals
            self.right_missionaries += self.boatA_missionaries
        else:
            self.left_cannibals += self.boatA_cannibals
            self.left_missionaries += self.boatA_missionaries
        self.boatA_cannibals = 0
        self.boatA_missionaries = 0

    def leave_boatB(self):
        if self.boatB_pos:
            self.right_cannibals += self.boatB_cannibals
            self.right_missionaries += self.boatB_missionaries
        else:
            self.left_cannibals += self.boatB_cannibals
            self.left_missionaries += self.boatB_missionaries
        self.boatB_cannibals = 0
        self.boatB_missionaries = 0

    def do_search(self, N, M, mode):
        Node = setParameter(N, M, mode = mode, alg = 'AS')
        start = Node()
        result = start.AStartSearch()
        self.path = [step.move for step in result['path'][1:]]
        self.ready = True
    
    def reset(self):
        self.right_cannibals = 3
        self.right_missionaries = 3
        self.left_cannibals = 0
        self.left_missionaries = 0
        self.boatA_cannibals = 0
        self.boatA_missionaries = 0
        self.boatB_cannibals = 0
        self.boatB_missionaries = 0



class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.control = ControlSystem()

        # create frames
        self.root_div1 = tk.Frame(root, width = div_size * 5, height = div_size * 0.8, bg = 'white', highlightbackground = "black", highlightthickness = 5) # 160 * 1000
        self.root_div2 = tk.Frame(root, width = div_size * 5, height = div_size * 2.8) # 560 * 1000

        # display frames
        self.root_div1.grid(column = 0, row = 0, padx = pad, pady = pad, sticky = align_mode)
        self.root_div2.grid(column = 0, row = 1, sticky = align_mode)

        # create items in root_div1
        self.search_button = tk.Button(root, text = 'search', bg = 'green')
        self.search_button.bind('<Button-1>', self.search)
        self.move_button = tk.Button(root, text = 'move', bg = 'white')
        self.move_button.bind('<Button-1>', self.move)
        self.reset_button = tk.Button(root, text = 'reset', bg = 'white')
        self.reset_button.bind('<Button-1>', self.reset)

        # display items in root_div1
        self.search_button.place(x = 50, y = 50, width = 80, height = 20)
        self.move_button.place(x = 50, y = 80, width = 80, height = 20)
        self.reset_button.place(x = 50, y = 110, width = 80, height = 20)

        # create items in root_div2
        self.canvas = tk.Canvas(self.root_div2, width = div_size * 5, height = div_size * 2.8) # 560 * 1000
        self.boat_img = ImageTk.PhotoImage(Image.open(BOAT_IMG_PATH).resize((div_size, div_size)))
        self.river_img = ImageTk.PhotoImage(Image.open(RIVER_IMG_PATH).resize((div_size * 5, div_size * 2.8)))

        # display items in root_div2
        self.canvas.grid(column = 0, row = 0)
        self.bg = self.canvas.create_image(0, 0, anchor = tk.NW, image = self.river_img)
        self.boatA = self.canvas.create_image(div_size * 3.5, div_size * 0.7, image = self.boat_img)
        self.boatB = self.canvas.create_image(div_size * 3.5, div_size * 2.1, image = self.boat_img)
        self.right_cannibals = self.canvas.create_text(div_size * 4.5, div_size * 0.7, text = str(self.control.right_cannibals), font = ('Arial', 100), fill = 'black')
        self.right_missionaries = self.canvas.create_text(div_size * 4.5, div_size * 2.1, text = str(self.control.right_missionaries), font = ('Arial', 100), fill = 'Crimson')
        self.left_cannibals = self.canvas.create_text(div_size * 0.5, div_size * 0.7, text = str(self.control.left_cannibals), font = ('Arial', 100), fill = 'black')
        self.left_missionaries = self.canvas.create_text(div_size * 0.5, div_size * 2.1, text = str(self.control.left_missionaries), font = ('Arial', 100), fill = 'Crimson')
        self.boatA_cannibals = self.canvas.create_text(div_size * 3.3, div_size * 0.4, text = str(self.control.boatA_cannibals), font = ('Arial', 50), fill = 'black')
        self.boatA_missionaries = self.canvas.create_text(div_size * 3.6, div_size * 0.4, text = str(self.control.boatA_missionaries), font = ('Arial', 50), fill = 'Crimson')
        self.boatB_cannibals = self.canvas.create_text(div_size * 3.3, div_size * 1.8, text = str(self.control.boatB_cannibals), font = ('Arial', 50), fill = 'black')
        self.boatB_missionaries = self.canvas.create_text(div_size * 3.6, div_size * 1.8, text = str(self.control.boatB_missionaries), font = ('Arial', 50), fill = 'Crimson')

    def update(self):
        self.canvas.itemconfig(self.right_cannibals, text = str(self.control.right_cannibals))
        self.canvas.itemconfig(self.right_missionaries, text = str(self.control.right_missionaries))
        self.canvas.itemconfig(self.left_cannibals, text = str(self.control.left_cannibals))
        self.canvas.itemconfig(self.left_missionaries, text = str(self.control.left_missionaries))
        self.canvas.itemconfig(self.boatA_cannibals, text = str(self.control.boatA_cannibals))
        self.canvas.itemconfig(self.boatA_missionaries, text = str(self.control.boatA_missionaries))
        self.canvas.itemconfig(self.boatB_cannibals, text = str(self.control.boatB_cannibals))
        self.canvas.itemconfig(self.boatB_missionaries, text = str(self.control.boatB_missionaries))

    def moving(self, boatA_step, boatB_step):
        for i in range(20):
            self.canvas.move(self.boatA, boatA_step, 0)
            self.canvas.move(self.boatA_cannibals, boatA_step, 0)
            self.canvas.move(self.boatA_missionaries, boatA_step, 0)
            self.canvas.move(self.boatB, boatB_step, 0)
            self.canvas.move(self.boatB_cannibals, boatB_step, 0)
            self.canvas.move(self.boatB_missionaries, boatB_step, 0)
            self.canvas.update()
            time.sleep(0.02)

    def move_boats(self, boatA_cannibals, boatA_missionaries, boatB_cannibals, boatB_missionaries):
        boatA_step, boatB_step = 0, 0
        if boatA_cannibals + boatA_missionaries > 0:
            boatA_step = div_size * 0.1 * (-1 if self.control.boatA_pos else 1)
        if boatB_cannibals + boatB_missionaries > 0:
            boatB_step = div_size * 0.1 * (-1 if self.control.boatB_pos else 1)
        self.control.board_boatA(boatA_cannibals, boatA_missionaries)
        self.control.board_boatB(boatB_cannibals, boatB_missionaries)
        self.control.check_validity()
        self.update()
        self.moving(boatA_step, boatB_step)
        if boatA_cannibals + boatA_missionaries > 0:
            self.control.boatA_pos = not self.control.boatA_pos
        if boatB_cannibals + boatB_missionaries > 0:
            self.control.boatB_pos = not self.control.boatB_pos
        self.control.leave_boatA()
        self.control.leave_boatB()
        self.control.check_validity()
        self.update()

    def search(self, event = None):
        if self.control.lock or self.control.ready:
            return
        self.control.lock = True
        self.search_button['bg'] = 'red'
        self.control.do_search(3, 0, 'p')
        self.search_button['bg'] = 'green'
        self.control.lock = False

    def move(self, event = None):
        if self.control.lock or not self.control.ready:
            return
        self.control.lock = True
        for step in self.control.path:
            self.move_boats(int(step[0], 16), int(step[1], 16), int(step[2], 16), int(step[3], 16))
        self.path = None
        self.control.ready = False
        self.control.lock = False

    def reset(self, event = None):
        if self.control.lock or self.control.ready:
            return
        self.control.lock = True
        self.control.reset()
        self.update()
        boatA_step = div_size * 0.1 * (0 if self.control.boatA_pos else 1)
        boatB_step = div_size * 0.1 * (0 if self.control.boatB_pos else 1)
        self.moving(boatA_step, boatB_step)
        self.control.boatA_pos = 1
        self.control.boatB_pos = 1
        self.control.lock = False



if __name__ == '__main__':
    root = Root()
    app = App(root)
    root.mainloop()
