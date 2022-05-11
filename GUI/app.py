import time
import tkinter as tk
from PIL import Image, ImageTk

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
        self.display_mode = False
        self.boatA_pos = 1
        self.boatB_pos = 1

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

        # create items in root_div2
        self.canvas = tk.Canvas(self.root_div2, width = div_size * 5, height = div_size * 2.8) # 560 * 1000
        self.boat_img = ImageTk.PhotoImage(Image.open(BOAT_IMG_PATH).resize((div_size, div_size)))
        self.river_img = ImageTk.PhotoImage(Image.open(RIVER_IMG_PATH).resize((div_size * 5, div_size * 2.8)))

        # display items in root_div2
        self.canvas.grid(column = 0, row = 0)
        self.bg = self.canvas.create_image(0, 0, anchor = tk.NW, image = self.river_img)
        self.boatA = self.canvas.create_image(div_size * 3.5, div_size * 0.7, image = self.boat_img)
        self.boatB = self.canvas.create_image(div_size * 3.5, div_size * 2.1, image = self.boat_img)

        # bind events
        self.root.bind('<KeyPress-A>', self.move_boatA)
        self.root.bind('<KeyPress-B>', self.move_boatB)

    def move_boatA(self, event = None):
        step = div_size * 0.1 * (-1 if self.control.boatA_pos else 1)
        for i in range(20):
            self.canvas.move(self.boatA, step, 0)
            self.canvas.update()
            time.sleep(0.02)
        self.control.boatA_pos = not self.control.boatA_pos

    def move_boatB(self, event = None):
        step = div_size * 0.1 * (-1 if self.control.boatB_pos else 1)
        for i in range(20):
            self.canvas.move(self.boatB, step, 0)
            self.canvas.update()
            time.sleep(0.02)
        self.control.boatB_pos = not self.control.boatB_pos



if __name__ == '__main__':
    root = Root()
    app = App(root)
    root.mainloop()
