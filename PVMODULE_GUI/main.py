import tkinter
from tkinter import ttk
from tkinter import messagebox
import tkintermapview

TITLE = "PV Module"


window = tkinter.Tk()
window.title(TITLE)

frame = tkinter.Frame(window)
frame.pack()

######Saving user info
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row = 0 , column = 0, padx = 10, pady = 10)

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

map_widget = tkintermapview.TkinterMapView(frame, width=400, height=300, corner_radius=0, padx=10, pady=10)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
map_widget.grid(row=4, column=0)  



def left_click_event(coordinates_tuple):
    print("Left click event with coordinates:", coordinates_tuple)
    from pvmodule.location import Location
    Location = Location()
    print(coordinates_tuple[0])
    print(coordinates_tuple[1])
    location = Location.set_location(  latitude = coordinates_tuple[0],  longitude = coordinates_tuple[1]  )
    city_name_marker = map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1], text=location.name)
    

map_widget.add_left_click_map_command(left_click_event)


window.mainloop()