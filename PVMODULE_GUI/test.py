from tkinter import *
import webbrowser

def callback(url):
   webbrowser.open_new_tab(url)
   
def TEstWin():
    toplevel = Toplevel(ws)

    toplevel.title("Test window")
    toplevel.geometry("230x80")


    l1=Label(toplevel, image="::tk::icons::information")
    l1.grid(row=0, column=0)
    l2=Label(toplevel,text="Test")
    l2.grid(row=0, column=1)


    left_label = Label(toplevel, text='Weblink', cursor="hand2", relief='raised', foreground='blue')#text= "Left-bottom")
    left_label.grid(row=2, column=2)
    left_label.bind("<Button-1>", lambda e:callback("https://robot.jbnu.ac.kr/robot/21492/subview.do"))

ws = Tk()
ws.geometry("300x200")
ws.title('Python Guides')
ws.config(bg='#345')
Button(ws,text="Test the window",command=TEstWin).pack(pady=80)

ws.mainloop()