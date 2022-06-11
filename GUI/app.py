from itertools import accumulate
import sys
import time
import traceback
import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
from CrossRiver.setup import setParameter

RIVER_IMG_PATH = 'GUI/img/river.png'
BOAT_IMG_PATH = 'GUI/img/boat.png'

div_size = 200
align_mode = 'nswe' # align center
pad = 3

class SolutionNotFoundError(Exception):
    pass

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Canibals & Missionaries')
        self.resizable(width = False, height = False)

class ControlSystem:
    def __init__(self):
        self.ready_to_search = True
        self.ready_to_move = False
        self.ready_to_reset = False
        self.lock = False

        self.path = None
        self.current_step = 0
        self.total_time = None
        self.total_price = None
        self.time_list = []
        self.price_list = []

        self.boatA_pos = 1
        self.boatB_pos = 1
        self.right_cannibals = 0
        self.right_missionaries = 0
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

    def do_search(self, N, M, mode, limit):
        Node = setParameter(N, M, mode = mode, alg = 'AS', limit = limit)
        start = Node()
        result = start.AStartSearch()

        if result is None:
            raise SolutionNotFoundError

        self.path = [step.move for step in result['path'][1:]]
        self.time_list = [step.total_time for step in result['path'][1:]]
        self.price_list = [step.total_price for step in result['path'][1:]]
        self.total_time = self.total_price = 0
    
    def reset(self):
        self.right_cannibals = 0
        self.right_missionaries = 0
        self.left_cannibals = 0
        self.left_missionaries = 0
        self.boatA_cannibals = 0
        self.boatA_missionaries = 0
        self.boatB_cannibals = 0
        self.boatB_missionaries = 0

        self.total_price = None
        self.total_time = None
        self.current_step = 0

    def update(self, N, M):
        self.right_cannibals = N
        self.right_missionaries = N + M



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
        self.state_label = tk.Label(self.root_div1, text = 'ready to search', font = ('Arial', 20), bg = 'white')
        self.search_button = tk.Button(self.root_div1, text = 'search', bg = 'white')
        self.search_button.bind('<Button-1>', self.search)
        self.reset_button = tk.Button(self.root_div1, text = 'reset', bg = 'white')
        self.reset_button.bind('<Button-1>', self.reset)
        self.quit_button = tk.Button(self.root_div1, text = 'quit', bg = 'white')
        self.quit_button.bind('<Button-1>', self.quit)

        self.nextmove_button = tk.Button(self.root_div1, text = 'next', bg = 'white')
        self.nextmove_button.bind('<Button-1>', self.nextmove)
        self.prevmove_button = tk.Button(self.root_div1, text = 'prev', bg = 'white')
        self.prevmove_button.bind('<Button-1>', self.prevmove)
        self.automove_button = tk.Button(self.root_div1, text = 'auto', bg = 'white')
        self.automove_button.bind('<Button-1>', self.automove)

        self.N_label = tk.Label(self.root_div1, text = 'N:', font = ('Arial', 20), bg = 'white')
        self.N_input = tk.Text(self.root_div1, width = 3, height = 1, font = ('Arial', 12), bg = 'white', highlightbackground = "black", highlightthickness = 2)
        self.M_label = tk.Label(self.root_div1, text = 'M:', font = ('Arial', 20), bg = 'white')
        self.M_input = tk.Text(self.root_div1, width = 3, height = 1, font = ('Arial', 12), bg = 'white', highlightbackground = "black", highlightthickness = 2)
        self.limit_lable = tk.Label(self.root_div1, text = 'limit:', font = ('Arial', 20), bg = 'white')
        self.limit_input = tk.Text(self.root_div1, width = 3, height = 1, font = ('Arial', 12), bg = 'white', highlightbackground = "black", highlightthickness = 2)

        self.mode_lable = tk.Label(self.root_div1, text = 'mode:', font = ('Arial', 20), bg = 'white')
        self.mode_list = ['price', 'time']
        self.mode_str = tk.StringVar()
        self.mode_str.set(self.mode_list[0])
        self.mode_select = tk.OptionMenu(self.root_div1, self.mode_str, *self.mode_list)

        self.price_label = tk.Label(self.root_div1, text = 'price:', font = ('Arial', 20), bg = 'white')
        self.time_label = tk.Label(self.root_div1, text = 'time:', font = ('Arial', 20), bg = 'white')

        # display items in root_div1
        self.search_button.place(x = 50, y = 20, width = 80, height = 20)
        self.reset_button.place(x = 50, y = 50, width = 80, height = 20)
        self.quit_button.place(x = 50, y = 80, width = 80, height = 20)
        self.state_label.place(x = 120, y = 110, width = 200, height = 20)

        self.nextmove_button.place(x = 360, y = 110, width = 80, height = 20)
        self.prevmove_button.place(x = 460, y = 110, width = 80, height = 20)
        self.automove_button.place(x = 560, y = 110, width = 80, height = 20)

        self.N_label.place(x = 210, y = 20, width = 20, height = 20)
        self.N_input.place(x = 250, y = 20, width = 50, height = 20)
        self.M_label.place(x = 210, y = 60, width = 20, height = 20)
        self.M_input.place(x = 250, y = 60, width = 50, height = 20)
        self.mode_lable.place(x = 360, y = 20, width = 80, height = 20)
        self.mode_select.place(x = 440, y = 20, width = 100, height = 20)
        self.limit_lable.place(x = 360, y = 60, width = 80, height = 20)
        self.limit_input.place(x = 450, y = 60, width = 80, height = 20)

        self.price_label.place(x = 600, y = 20, width = 120, height = 20)
        self.time_label.place(x = 600, y = 60, width = 120, height = 20)

        # create items in root_div2
        self.canvas = tk.Canvas(self.root_div2, width = div_size * 5, height = div_size * 2.8) # 560 * 1000
        self.boat_img = ImageTk.PhotoImage(Image.open(BOAT_IMG_PATH).resize((div_size, div_size)))
        self.river_img = ImageTk.PhotoImage(Image.open(RIVER_IMG_PATH).resize((div_size * 5, div_size * 2.8)))

        # display items in root_div2
        self.canvas.grid(column = 0, row = 0)
        self.bg = self.canvas.create_image(0, 0, anchor = tk.NW, image = self.river_img)
        self.boatA = self.canvas.create_image(div_size * 3.5, div_size * 0.7, image = self.boat_img)
        self.boatB = self.canvas.create_image(div_size * 3.5, div_size * 2.1, image = self.boat_img)
        self.right_cannibals = self.canvas.create_text(div_size * 4.5, div_size * 0.7, text = str(self.control.right_cannibals), font = ('Arial', 100), fill = 'Crimson')
        self.right_missionaries = self.canvas.create_text(div_size * 4.5, div_size * 2.1, text = str(self.control.right_missionaries), font = ('Arial', 100), fill = 'black')
        self.left_cannibals = self.canvas.create_text(div_size * 0.5, div_size * 0.7, text = str(self.control.left_cannibals), font = ('Arial', 100), fill = 'Crimson')
        self.left_missionaries = self.canvas.create_text(div_size * 0.5, div_size * 2.1, text = str(self.control.left_missionaries), font = ('Arial', 100), fill = 'black')
        self.boatA_cannibals = self.canvas.create_text(div_size * 3.3, div_size * 0.4, text = str(self.control.boatA_cannibals), font = ('Arial', 50), fill = 'Crimson')
        self.boatA_missionaries = self.canvas.create_text(div_size * 3.6, div_size * 0.4, text = str(self.control.boatA_missionaries), font = ('Arial', 50), fill = 'black')
        self.boatB_cannibals = self.canvas.create_text(div_size * 3.3, div_size * 1.8, text = str(self.control.boatB_cannibals), font = ('Arial', 50), fill = 'Crimson')
        self.boatB_missionaries = self.canvas.create_text(div_size * 3.6, div_size * 1.8, text = str(self.control.boatB_missionaries), font = ('Arial', 50), fill = 'black')

    def update(self):
        self.canvas.itemconfig(self.right_cannibals, text = str(self.control.right_cannibals))
        self.canvas.itemconfig(self.right_missionaries, text = str(self.control.right_missionaries))
        self.canvas.itemconfig(self.left_cannibals, text = str(self.control.left_cannibals))
        self.canvas.itemconfig(self.left_missionaries, text = str(self.control.left_missionaries))
        self.canvas.itemconfig(self.boatA_cannibals, text = str(self.control.boatA_cannibals))
        self.canvas.itemconfig(self.boatA_missionaries, text = str(self.control.boatA_missionaries))
        self.canvas.itemconfig(self.boatB_cannibals, text = str(self.control.boatB_cannibals))
        self.canvas.itemconfig(self.boatB_missionaries, text = str(self.control.boatB_missionaries))

        self.time_label.config(text = 'time: ' + (str(self.control.total_time) if self.control.total_time is not None else ''))
        self.price_label.config(text = 'price: ' + (str(self.control.total_price) if self.control.total_price is not None else ''))

    def moving(self, boatA_step, boatB_step):
        for _ in range(20):
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

    def get_parameters(self):
        N = self.N_input.get("1.0", "end").strip()
        M = self.M_input.get("1.0", "end").strip()
        mode = self.mode_str.get()
        limit = self.limit_input.get("1.0", "end").strip()
        return N, M, mode, limit

    def search(self, event = None):
        if self.control.lock or not self.control.ready_to_search:
            return
        self.control.lock = True
        N, M, mode, limit = self.get_parameters()

        if mode == 'price':
            mode = 'p'
        elif mode == 'time':
            mode = 't'

        if limit == '':
            limit = None

        try:
            N = int(N)
            M = int(M)
            limit = int(limit) if limit else None
            self.control.update(N, M)
            self.control.do_search(N, M, mode, limit)
        except SolutionNotFoundError:
            messagebox.showinfo('Error', 'No solution found')
        except Exception as e:
            print(N, M, mode, limit)
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print("\nExecution halted:\n" + errMsg)
            self.state_label.config(text = "Error, try again")
        else:
            self.update()
            self.state_label.config(text = 'ready to move')
            self.control.ready_to_search = False
            self.control.ready_to_move = True
        finally:
            self.control.lock = False

    def move(self, event = None):
        if self.control.lock or not self.control.ready_to_move:
            return
        self.control.lock = True
        for i, step in enumerate(self.control.path):
            self.control.total_price = self.control.price_list[i]
            self.control.total_time = self.control.time_list[i]
            self.update()
            self.move_boats(int(step[0], 16), int(step[1], 16), int(step[2], 16), int(step[3], 16))
        self.state_label.config(text = 'ready to reset')
        self.control.ready_to_move = False
        self.control.ready_to_reset = True
        self.control.lock = False

    def nextmove(self, event = None):
        if self.control.lock or not self.control.ready_to_move:
            return
        self.control.lock = True
        self.control.total_price = self.control.price_list[self.control.current_step]
        self.control.total_time = self.control.time_list[self.control.current_step]
        self.update()
        step = self.control.path[self.control.current_step]
        self.move_boats(int(step[0], 16), int(step[1], 16), int(step[2], 16), int(step[3], 16))
        self.control.current_step += 1
        if self.control.current_step == len(self.control.path):
            self.state_label.config(text = 'ready to reset')
            self.control.ready_to_move = False
            self.control.ready_to_reset = True
        self.control.lock = False

    def prevmove(self, event = None):
        if self.control.lock or not self.control.ready_to_move:
            return
        if self.control.current_step == 0:
            return
        self.control.lock = True
        self.control.current_step -= 1
        self.control.total_price = self.control.price_list[self.control.current_step]
        self.control.total_time = self.control.time_list[self.control.current_step]
        self.update()
        step = self.control.path[self.control.current_step]
        self.move_boats(int(step[0], 16), int(step[1], 16), int(step[2], 16), int(step[3], 16))
        self.control.lock = False

    def automove(self, event = None):
        if self.control.lock or not self.control.ready_to_move:
            return
        self.control.lock = True
        for i in range(self.control.current_step, len(self.control.path)):
            self.control.total_price = self.control.price_list[i]
            self.control.total_time = self.control.time_list[i]
            self.update()
            step = self.control.path[i]
            self.move_boats(int(step[0], 16), int(step[1], 16), int(step[2], 16), int(step[3], 16))
            self.control.current_step = i
        self.state_label.config(text = 'ready to reset')
        self.control.ready_to_move = False
        self.control.ready_to_reset = True
        self.control.lock = False

    def reset(self, event = None):
        if self.control.lock or not self.control.ready_to_reset:
            return
        self.control.lock = True
        self.control.reset()
        self.update()
        boatA_step = div_size * 0.1 * (0 if self.control.boatA_pos else 1)
        boatB_step = div_size * 0.1 * (0 if self.control.boatB_pos else 1)
        self.moving(boatA_step, boatB_step)
        self.control.boatA_pos = 1
        self.control.boatB_pos = 1
        self.state_label.config(text = 'ready to search')
        self.control.ready_to_reset = False
        self.control.ready_to_search = True
        self.control.lock = False

    def quit(self, event = None):
        self.root.destroy()
