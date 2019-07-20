from tkinter import *
from tkinter import messagebox
import random
import time
import pygame


root = Tk()


root.title('Pong')
root.wm_attributes('-topmost',1)
root.resizable(0,0)


def controls():
    messagebox.showinfo(title = 'Controls', message = "Use 'A' and 'D' to move the left paddle and 'Left' and 'Right' key to move the right paddle. " )

def help():
    messagebox.showinfo(title = 'Help', message = "Every time the ball misses the peddle the opposite teammate gains a point. When any of the teammate reaches 10 points , he/she "
                                                  "is declared to be the winner!!")

mainMenu = Menu(root)
root.config(menu = mainMenu)
subMenu = Menu(mainMenu, tearoff = 0)


mainMenu.add_command(label= 'Controls', command = controls)
mainMenu.add_command(label = 'Help', command = help)

canvas = Canvas(root,height = 500, width = 700, bd = 0, highlightthickness = 0)
canvas.configure(bg = 'black')
canvas.pack()
root.update()

canvas.create_line(350,0,350,500, fill = '#ffffff')




class Ball:
    def __init__(self,canvas,paddle_1,paddle_2,color):
        self.canvas = canvas
        self.paddle_1 = paddle_1
        self.paddle_2 = paddle_2
        self.id = canvas.create_oval(10,10,25,25, fill = color)
        self.canvas.move(self.id,335,240)
        start_x = [-3,3]
        start_y = [-3,3]

        self.l_s = None
        self.r_s = None

        self.s_1 = None
        self.s_2 = None

        random.shuffle(start_x)
        random.shuffle(start_y)

        self.x = start_x[0]
        self.y = start_y[0]

        self.counter_1 = 0
        self.counter_2 = 0

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()





    def hit_paddle_1(self,pos):
        paddle_1_pos = self.canvas.coords(self.paddle_1.id)
        if pos[3] <= paddle_1_pos[3] and pos[3] >= paddle_1_pos[1]:
            if pos[0] <= paddle_1_pos[2] and pos[2] >= paddle_1_pos[0]:
                return True
            return False

    def hit_paddle_2(self,pos):
        paddle_2_pos = self.canvas.coords(self.paddle_2.id)
        if pos[3] >= paddle_2_pos[1] and pos[3] <= paddle_2_pos[3]:
            if pos[2] >= paddle_2_pos[0] and pos[0] <= paddle_2_pos[2]:
                return True
            return False

    def update_left_score(self,val):
        self.canvas.delete(self.l_s)
        self.l_s = self.canvas.create_text(125,40,text = str(val),font = ('Ariel',50), fill = '#ffffff')



    def update_right_score(self,val):
        self.canvas.delete(self.r_s)
        self.r_s = self.canvas.create_text(475,40,text = str(val),font = ('Ariel',50), fill = '#ffffff')



    def draw(self):

        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3

        if pos[3] >= self.canvas_height:
            self.y = -3
        if pos[0] <= 0:
            self.counter_2 += 1

            pygame.init()
            pygame.mixer.music.load('beep.wav')
            pygame.mixer.music.play()

            self.canvas.move(self.id,327,220)
            self.x = 3

            self.update_right_score(self.counter_2)

        if pos[2] >= self.canvas_width:
            self.counter_1 += 1

            pygame.init()
            pygame.mixer.music.load('beep.wav')
            pygame.mixer.music.play()

            self.canvas.move(self.id,-327,-220)
            self.x = -3

            self.update_left_score(self.counter_1)

        if self.hit_paddle_1(pos) == True:
            self.x = 3


            pygame.init()
            pygame.mixer.music.load('Pong.wav')
            pygame.mixer.music.play()





        if self.hit_paddle_2(pos) == True:
            self.x = -3


            pygame.init()
            pygame.mixer.music.load('Pong.wav')
            pygame.mixer.music.play()





    def checkwin(self):
        winner = None
        if self.counter_1 == 10:
            winner = 'Left player'
        elif self.counter_2 == 10:
            winner = 'Right player'

        return winner





class Paddle_1:
    def __init__(self,canvas,color):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0,0,15,110, fill = color)
        self.canvas.move(self.id,5,250)

        self.y = 0

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()





    def draw(self):
        self.canvas.move(self.id, 0,self.y)
        self.canvas.bind_all('a', self.go_up)
        self.canvas.bind_all('d',self.go_down)
        paddle_1_pos = self.canvas.coords(self.id)

        if paddle_1_pos[1] <= 0:
            self.y = 0
        if paddle_1_pos[3] >= self.canvas_height:
            self.y = 0


    def go_up(self,evt):
        self.y = -3
    def go_down(self,evt):
        self.y = 3



class Paddle_2:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, 15, 110, fill=color)
        self.canvas.move(self.id, 685, 250)

        self.y = 0

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, 0, self.y)
        self.canvas.bind_all('<Left>', self.go_up)
        self.canvas.bind_all('<Right>', self.go_down)
        paddle_2_pos = self.canvas.coords(self.id)

        if paddle_2_pos[1] <= 0:
            self.y = 0
        if paddle_2_pos[3] >= self.canvas_height:
            self.y = 0

    def go_up(self,evt):
        self.y = -3
    def go_down(self,evt):
        self.y = 3




paddle_1 = Paddle_1(canvas,'blue')
paddle_2 = Paddle_2(canvas,'red')
ball = Ball(canvas,paddle_1,paddle_2,'orange')





while 1:

    ball.draw()
    paddle_1.draw()
    paddle_2.draw()
    if ball.checkwin():
        messagebox.showinfo('Game End', ball.checkwin()+' wins !!')
        break
    root.update_idletasks()
    root.update()
    time.sleep(0.008)



quit()
root.mainloop()