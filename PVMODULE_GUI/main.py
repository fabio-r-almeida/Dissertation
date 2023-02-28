import tkinter
from tkinter import ttk

TITLE = "PV Module"
window = tkinter.Tk()
window.title(TITLE)




######Widget
frame = tkinter.Frame(window)
frame.pack()

######Saving user info
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row = 0 , column = 0, padx = 20, pady = 20)

######Widget inside LabelFrame
#titles
first_name_label= tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row = 0 , column = 0)
#titles
last_name_label= tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row = 0 , column = 1)

######Entries
#Text Entry
first_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row = 1 , column = 0)

last_name_entry = tkinter.Entry(user_info_frame)
last_name_entry.grid(row = 1 , column = 1)

#List Entry
title_label = tkinter.Label(user_info_frame, text="Title")
title_combobox = ttk.Combobox(user_info_frame, values= ["", "Mr.", "Ms.", "Dr."])
title_label.grid(row = 0, column = 2)
title_combobox.grid(row = 1, column = 2)

age_label = tkinter.Label(user_info_frame, text="Age")
age_spinbox = tkinter.Spinbox(user_info_frame, from_= 18, to = 110)
age_label.grid(row = 2, column = 0)
age_spinbox.grid(row = 3, column = 0)

nationality_label = tkinter.Label(user_info_frame, text="Nationality")
nationality_combobox = ttk.Combobox(user_info_frame, values= ["EN", "PT", "DE", "BR"])
nationality_label.grid(row = 2, column = 1)
nationality_combobox.grid(row = 3, column = 1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)



######Saving course info
courses_frame = tkinter.LabelFrame(frame, text="Registration")
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=20)

registered_label = tkinter.Label(courses_frame, text = "Registration Status")
registered_label.grid(row = 0, column = 0)

registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered")
registered_check.grid(row = 1, column = 0)



















window.mainloop()