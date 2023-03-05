import customtkinter
import os
import tkinter.messagebox
import customtkinter
from tkinter import *
import importlib.metadata
from PIL import Image
from tkinter.ttk import Progressbar

class Loading(tkinter.Toplevel):

    current_loadings = []
    width = 427
    height = 250   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial_loadings = ["","",""]
        self.progress_status_value = 0

        self.title("Loading")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.splash_text = tkinter.StringVar(value = f'''\n\n\n\n\n\n\n\t           V.{importlib.metadata.version("pvmodule")}\n\n\n
        
        \nLoading ...''')  

        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, textvariable=self.splash_text)

        self.bg_image_label.grid(row=0, column=0, )

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width_of_window = 427
        height_of_window = 250
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        self.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
        self.overrideredirect(True)  


        

        self.progress=Progressbar(self,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=500,mode='determinate')
        self.progress.place(x=-10,y=235)

        self.update()
        ## required to make window show before the program gets to the mainloop
    def bar(self):
        self.splash_text.set(f'''\n\n\n\n\n\n\n\t           V.{importlib.metadata.version("pvmodule")}\n\n\n
        
        \n{self.current_loadings[-1]}''' )
        self.progress['value'] = len(self.current_loadings)/len(self.initial_loadings)*100
        self.update_idletasks()

