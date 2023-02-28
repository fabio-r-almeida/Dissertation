import tkinter
from tkinter import ttk
from tkinter import messagebox
import tkintermapview

TITLE = "PV Module"
window = tkinter.Tk()
window.title(TITLE)

frame = tkinter.Frame(window)
frame.pack()

def map_window():

    map_frame = tkinter.Label(frame, text="Location Selection Map")
    map_frame.grid(row = 99 , column = 0, padx = 0, pady = 10 )
    map_widget = tkintermapview.TkinterMapView(map_frame, width=400, height=300, corner_radius=0, padx=10, pady=10)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    map_widget.grid(row=4, column=0)  

    def left_click_event(coordinates_tuple):   
        map_widget.delete_all_marker()
        
        latitude = round(coordinates_tuple[0],6)
        longitude = round(coordinates_tuple[1],6)
        adr = tkintermapview.convert_coordinates_to_address(latitude, longitude)
        try:
            address_display = adr.street + ", " + adr.city
        except:
            address_display = "Street Address not found"
        city_name_marker = map_widget.set_marker(latitude, longitude, text=address_display)
        
        Latitude_entry_var.set(latitude)
        Longitude_entry_var.set(longitude)
        map_frame.destroy()
    map_widget.add_left_click_map_command(left_click_event)
        

    








######Saving user info
user_selection_frame = tkinter.Label(frame, text="User Selection")
user_selection_frame.grid(row = 0 , column = 0, padx = 0, pady = 10 )



user_address_data = tkinter.LabelFrame(user_selection_frame, text="Location Data")
user_address_data.grid(row = 0 , column = 0, padx = 10, pady = 10, sticky="news")

Latitude_label= tkinter.Label(user_address_data, text="Latitude")
Latitude_label.grid(row = 0 , column = 0,)


Latitude_entry_var = tkinter.StringVar(value = "00.000000")
Latitude_Entry = tkinter.Label(user_address_data, textvariable=Latitude_entry_var)
Latitude_Entry.grid(row = 0 , column = 1)

Longitude_label= tkinter.Label(user_address_data, text="Longitude")
Longitude_label.grid(row = 1 , column = 0)
Longitude_entry_var = tkinter.StringVar(value = "00.000000")
Longitude_Entry = tkinter.Label(user_address_data, textvariable=Longitude_entry_var)
Longitude_Entry.grid(row = 1 , column = 1)    

button = tkinter.Button(user_address_data, text = "Select From Map", command = map_window )
button.grid(row=3, columnspan=3, sticky="news", padx=10, pady=10 )






setup = tkinter.LabelFrame(user_selection_frame, text="Setup Data")
setup.grid(row = 0 , column = 1, padx = 10, pady = 10, sticky="news")


user_panel_data = tkinter.Frame(setup)
user_panel_data.grid(row = 0 , column = 0, padx = 10, pady = 10, sticky="news")

user_inverter_data = tkinter.Frame(setup)
user_inverter_data.grid(row = 0 , column = 1, padx = 10, pady = 10)


from pvmodule import Modules
modules = Modules().list_modules(print_data=False)
module_brand = modules['Manufacturer']

module_brand = list(dict.fromkeys(module_brand.tolist()))
v = []
def combofill(event):
    v = modules[ modules['Manufacturer'] == Module_List_Brand_combobox.get()]['Model Number'].tolist()
    Module_List_Model_combobox.config(values=v)

Module_List_Brand_Label = tkinter.Label(user_panel_data, text="Module Brand")
Module_List_Brand_combobox = ttk.Combobox(user_panel_data, values= module_brand)
Module_List_Brand_combobox.bind('<<ComboboxSelected>>', combofill)
Module_List_Brand_Label.grid(row=0, column=0, sticky="news", padx=10, pady=10 )
Module_List_Brand_combobox.grid(row=0, column=1, sticky="news", padx=10, pady=10 )



module_model = modules['Model Number']
Module_List_Model_Label = tkinter.Label(user_panel_data, text="Module Model")
Module_List_Model_combobox = ttk.Combobox(user_panel_data, values= module_model.tolist())
Module_List_Model_Label.grid(row=1, column=0, sticky="news", padx=10, pady=10 )
Module_List_Model_combobox.grid(row=1, column=1, sticky="news", padx=10, pady=10 )




Inverter_Brand_Label= tkinter.Label(user_inverter_data, text="Inverter Brand")
Inverter_Brand_Label.grid(row = 0 , column = 0)
Inverter_Brand_entry_var = tkinter.StringVar(value = "                                     ")
Inverter_Brand_Entry = tkinter.Label(user_inverter_data, textvariable=Inverter_Brand_entry_var)
Inverter_Brand_Entry.grid(row = 0 , column = 1)

Inverter_Model_Label= tkinter.Label(user_inverter_data, text="Inverter Model")
Inverter_Model_Label.grid(row = 1 , column = 0)
Inverter_Model_entry_var = tkinter.StringVar(value = "                                     ")
Inverter_Brand_Entry = tkinter.Label(user_inverter_data, textvariable=Inverter_Model_entry_var)
Inverter_Brand_Entry.grid(row = 1 , column = 1)


from pvmodule import Inverters
inverter_list = Inverters().list_inverters()

Inverter_List_Label = tkinter.Label(user_inverter_data, text="Inverter List")
Inverter_List_combobox = ttk.Combobox(user_inverter_data, values= inverter_list.Name.tolist())
Inverter_List_Label.grid(row=3, column=0, sticky="news", padx=10, pady=10 )
Inverter_List_combobox.grid(row=3, column=1, sticky="news", padx=10, pady=10 )




for widget in user_address_data.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in user_selection_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in setup.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in user_panel_data.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in user_inverter_data.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)





window.mainloop()