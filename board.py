from tkinter import *
import numpy as np
from PIL import ImageTk
from PIL import Image

class Board:

    def  __init__(self):
        self.root = Tk()
        self.root.title("Game Board")
        self.root.resizable(height = False, width = False)
        widthpixels = 300
        heightpixels = 300
        self.root.geometry('{}x{}'.format(widthpixels, heightpixels))
        #Image sources
        self.images = ['cancel.png', 'zero.png']
        #make positions
        self.positions = []
        for i in range(4):
            row = []
            for j in range(4):
                if (3*i+j)%2 == 0:
                    color="gray53"
                else:
                    color = "white"
                a = Canvas(self.root,highlightthickness=0, height = 75, width = 75, bg=color)
                a.grid(row=i, column=j)
                row.append(a)
            self.positions.append(row)
        self.positions = np.array(self.positions)
        #Players' positions
        self.current_pos = [[0,0], [1,1]]
        
    def move(self, player, position):
        #'cancel.png' for player 0, zero.png for player 1
        #first remove image of previous position
        self.positions[self.current_pos[player][0]][self.current_pos[player][1]].delete("all")
        image_path = self.images[player]
        self.putimage(self.positions[position[0]][position[1]], image_path)
        self.current_pos[player] = position
        
    def putimage(self, canvas, image_path):
        photo = Image.open(image_path)
        photo = photo.resize((60,60))
        photo = ImageTk.PhotoImage(photo)
        canvas.create_image(35,35, image = photo)
        canvas.image = photo

