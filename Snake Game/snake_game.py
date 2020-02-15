from tkinter import *
import random
import threading
import time

WIDTH = 500
HEIGHT = 500


class Snake(Tk):
    """background set as canvas and grid"""
    def __init__(self):
        Tk.__init__(self)
        self.title("Snake")
        self.configure(width=WIDTH, height=HEIGHT)
        self.grid()
        fond = Canvas(self)
        fond.grid()
        self.canvas = Canvas(fond, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.grid(columnspan=3)
        self.canvas.focus_set()
        self.start = Button(fond, text="Start", width=3, height=1, command=self.greet)
        self.start.place(x=225, y=225)

        """snake's body"""
        self.serpwidth = 10
        """apple definition"""
        self.red_apple = None
        """game over status"""
        self.gameover = False
        """direction storage"""
        self.direction = None
        """score"""
        self.score = 0

    def greet(self):
        """green snake set to 3 squares"""
        #print("Greetings!") #debug
        self.canvas.delete(ALL)
        self.start.place_forget()
        serp1 = self.canvas.create_rectangle(WIDTH/2-self.serpwidth, HEIGHT/2-self.serpwidth, WIDTH/2+self.serpwidth
                                             , HEIGHT/2+self.serpwidth, outline="green3", fill="green3"
                                             , tag="serp1")
        serp2 = self.canvas.create_rectangle(WIDTH/2-self.serpwidth, HEIGHT/2-self.serpwidth, WIDTH/2+self.serpwidth
                                             , HEIGHT/2+self.serpwidth, outline="green3", fill="green3"
                                             , tag="serp2")
        serp3 = self.canvas.create_rectangle(WIDTH/2-self.serpwidth, HEIGHT/2-self.serpwidth, WIDTH/2+self.serpwidth
                                             , HEIGHT/2+self.serpwidth, outline="green3", fill="green3"
                                             , tag="serp3")

        """snake's body parts made into a list"""
        self.rectangles = [serp1, serp2, serp3]
        """resets"""
        self.gameover = False
        self.direction = None
        self.red_apple = None
        self.score = 0

        """commands"""
        self.canvas.bind("<Key>", self.movement)
        self.move_start()

    def movement(self, event):
        """keybinds"""
        leftcode = 113
        rightcode = 114
        upcode = 111
        downcode = 116
        """changes self.direction according to keyboard"""
        if self.gameover is False:
            if event.keycode == upcode:
                self.direction = 'up'
            elif event.keycode == rightcode:
                self.direction = 'right'
            elif event.keycode == downcode:
                self.direction = 'down'
            elif event.keycode == leftcode:
                self.direction = 'left'

    def move_start(self):
        threading.Thread(target=self.auto_move).start()

    def auto_move(self):
        """snake movement, moves last rectangle infront of the head, becoming the new head"""
        w = self.serpwidth *2
        if self.gameover is False:
            lock = threading.Lock()
            lock.acquire()
            """coordinates of the front and back of the snake"""
            front_coords = self.canvas.coords(self.rectangles[0])
            end_coords = self.canvas.coords(self.rectangles[-1])
            """removes the last rectangle"""
            moving_rectangle = self.rectangles.pop()
            """direction"""
            if self.direction == 'up':
                self.canvas.move(self.canvas.gettags(moving_rectangle), int(front_coords[0]-end_coords[0]),
                                 int(front_coords[1]-end_coords[1])-w)
            elif self.direction == 'down':
                self.canvas.move(self.canvas.gettags(moving_rectangle), int(front_coords[0]-end_coords[0]),
                                 int(front_coords[1]-end_coords[1])+w)
            elif self.direction == 'left':
                self.canvas.move(self.canvas.gettags(moving_rectangle), int(front_coords[0]-end_coords[0])-w,
                                 int(front_coords[1]-end_coords[1]))
            elif self.direction == 'right':
                self.canvas.move(self.canvas.gettags(moving_rectangle), int(front_coords[0]-end_coords[0])+w,
                                 int(front_coords[1]-end_coords[1]))
            self.canvas.after(50)
            self.rectangles.insert(0, moving_rectangle)
            self.canvas.after(50, self.move_start)
            lock.release()
            self.grow()
            self.end_game()
        elif self.gameover is True:
            self.canvas.delete(ALL)
            self.start = Button(self.canvas, text="GAME OVER! Score: %d \nClick to restart" % self.score
                                , width=20, height=2, command=self.greet)
            self.start.place(x=160, y=225)

    def grow(self):
        """when apples are eaten, snake grows"""
        if self.red_apple is None:
            self.apple()
        w = self.serpwidth * 2
        front_coords = self.canvas.coords(self.rectangles[0])
        self.a_coords = self.canvas.find_overlapping(front_coords[0], front_coords[1], front_coords[2], front_coords[3])
        for item in self.a_coords:
            if item == self.red_apple:
                lock = threading.Lock()
                lock.acquire()
                """body part's tag number"""
                num = "serp" + str(len(self.rectangles) + 1)
                """coordinates"""
                end_coords = self.canvas.coords(self.rectangles[-1])
                x1 = end_coords[0]
                y1 = end_coords[1]
                x2 = end_coords[2]
                y2 = end_coords[3]
                if self.direction == "up":
                    new = self.canvas.create_rectangle(x1, y1-w, x2, y2-w, outline="green3", fill="green3", tag=num)
                    self.rectangles.append(new)
                elif self.direction == "down":
                    new = self.canvas.create_rectangle(x1, y1+w, x2, y2+w, outline="green3", fill="green3", tag=num)
                    self.rectangles.append(new)
                elif self.direction == "left":
                    new = self.canvas.create_rectangle(x1-w, y1, x2-w, y2, outline="green3", fill="green3", tag=num)
                    self.rectangles.append(new)
                elif self.direction == "right":
                    new = self.canvas.create_rectangle(x1+w, y1, x2+w, y2, outline="green3", fill="green3", tag=num)
                    self.rectangles.append(new)
                self.score += 1
                self.canvas.delete(self.red_apple)
                self.red_apple = None
                lock.release()

    def apple(self):
        """apple appearances"""
        w = self.serpwidth * 2
        x_apple = int(random.randrange(481))
        y_apple = int(random.randrange(481))
        self.red_apple = self.canvas.create_rectangle(x_apple, y_apple, x_apple+w, y_apple+w
                                                      , outline="red3", fill="red2", tag="red_apple")

    def end_game(self):
        """ends game"""
        front_coords = self.canvas.coords(self.rectangles[0])
        x1 = front_coords[0]
        y1 = front_coords[1]
        x2 = front_coords[2]
        y2 = front_coords[3]
        if x1 < -1 or y1 < -1 or x2 > 501 or y2 > 501:
            self.gameover = True
        for item in self.rectangles[3:]:
            item = self.canvas.coords(item)
            if item == front_coords:
                self.gameover = True


Snake().mainloop()

"""
        for item in self.a_coords:
            if item in self.rectangles[3:]:
                self.game_over = True
"""
