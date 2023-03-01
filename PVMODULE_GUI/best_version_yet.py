import tkinter as tk
import tkinter
from tkinter import ttk
from tkinter import messagebox
import tkintermapview



# root window
root = tk.Tk()
root.title('Notebook Demo')

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)


# create frames
tab1 = ttk.Frame(notebook)

tab2 = ttk.Frame(notebook)

tab1.pack()

tab2.pack()

# add frames to notebook

notebook.add(tab1, text='General Information')
notebook.add(tab2, text='Profile')




def map_window():
    top= tk.Toplevel(root)
    top.title("Map Window")
    map_frame = tkinter.Label(top, text="Location Selection Map")
    map_frame.grid(row = 99 , column = 0, padx = 0, pady = 10 )
    map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=0, padx=10, pady=10)
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
        top.destroy()
        map_frame.destroy()

    map_widget.add_left_click_map_command(left_click_event)
        

    

######Location Entry######
user_selection_frame = tkinter.Label(tab1, text="User Selection")
user_selection_frame.grid(row = 0 , column = 0, padx = 0, pady = 10 )

user_address_data = tkinter.LabelFrame(user_selection_frame, text="Location Data")
user_address_data.grid(row = 0 , column = 0, padx = 10, pady = 10, sticky="news")

######Latitude Entry######
Latitude_label= tkinter.Label(user_address_data, text="Latitude")
Latitude_label.grid(row = 0 , column = 0,)

Latitude_entry_var = tkinter.StringVar(value = "00.000000")
Latitude_Entry = tkinter.Label(user_address_data, textvariable=Latitude_entry_var)
Latitude_Entry.grid(row = 0 , column = 1)

######Longitude Entry######
Longitude_label= tkinter.Label(user_address_data, text="Longitude")
Longitude_label.grid(row = 1 , column = 0)
Longitude_entry_var = tkinter.StringVar(value = "00.000000")
Longitude_Entry = tkinter.Label(user_address_data, textvariable=Longitude_entry_var)
Longitude_Entry.grid(row = 1 , column = 1)    

######Button that opens the map######
button = tkinter.Button(user_address_data, text = "Select From Map", command = map_window )
button.grid(row=3, columnspan=3, sticky="news", padx=10, pady=10 )





######Setup Entry for Modules and Inverters######
setup = tkinter.LabelFrame(user_selection_frame, text="Setup Data")
setup.grid(row = 0 , column = 1, padx = 10, pady = 10, sticky="news")

######Creation of two grids side by side######
user_panel_data = tkinter.Frame(setup)
user_panel_data.grid(row = 0 , column = 0, padx = 10, pady = 10, sticky="news")

user_inverter_data = tkinter.Frame(setup)
user_inverter_data.grid(row = 0 , column = 1, padx = 10, pady = 10, sticky="news")


######Population both dropdowns menus depending on the first dropdown selection######
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
Module_List_Model_combobox = ttk.Combobox(user_panel_data, values= [])
Module_List_Model_Label.grid(row=1, column=0, sticky="news", padx=10, pady=10 )
Module_List_Model_combobox.grid(row=1, column=1, sticky="news", padx=10, pady=10 )







from pvmodule import Inverters
inverters = Inverters().list_inverters()

inverter_brand = inverters['Manufacturer']

inverter_brand = list(dict.fromkeys(inverter_brand.tolist()))
v = []
def combofill(event):
    v = inverters[ inverters['Manufacturer'] == Inverter_List_Brand_combobox.get()]['Model Number'].tolist()
    Inverter_List_Model_combobox.config(values=v)

Inverter_List_Brand_Label = tkinter.Label(user_inverter_data, text="Inverter Brand")
Inverter_List_Brand_combobox = ttk.Combobox(user_inverter_data, values= inverter_brand)
Inverter_List_Brand_combobox.bind('<<ComboboxSelected>>', combofill)
Inverter_List_Brand_Label.grid(row=0, column=0, sticky="news", padx=10, pady=10 )
Inverter_List_Brand_combobox.grid(row=0, column=1, sticky="news", padx=10, pady=10 )


inverter_model = inverters['Model Number']
Inverter_List_Model_Label = tkinter.Label(user_inverter_data, text="Inverter Model")
Inverter_List_Model_combobox = ttk.Combobox(user_inverter_data, values= [])
Inverter_List_Model_Label.grid(row=1, column=0, sticky="news", padx=10, pady=10 )
Inverter_List_Model_combobox.grid(row=1, column=1, sticky="news", padx=10, pady=10 )


user_panel_datasheet = tkinter.Frame(setup)
user_panel_datasheet.grid(row = 1 , column = 0, padx = 10, pady = 10, sticky="news")

user_inverter_datasheet = tkinter.Frame(setup)
user_inverter_datasheet.grid(row = 1 , column = 1, padx = 10, pady = 10, sticky="news")



######Aditional information regarding the selection above######
Module_Peak_Wattage_Label= tkinter.Label(user_panel_datasheet, text="Module Peak Wattage")
Module_Peak_Wattage_Label.grid(row = 0 , column = 0, sticky="news", padx=10, pady=10 )
Module_Peak_Wattage_entry_var = tkinter.StringVar(value = "0")
Module_Peak_Wattage_Entry = tkinter.Label(user_panel_datasheet, textvariable=Module_Peak_Wattage_entry_var)
Module_Peak_Wattage_Entry.grid(row = 0 , column = 1, sticky="news", padx=10, pady=10 ) 

Module_Technology_Label= tkinter.Label(user_panel_datasheet, text="Module Technology")
Module_Technology_Label.grid(row = 1 , column = 0, sticky="news", padx=10, pady=10 )
Module_Technology_entry_var = tkinter.StringVar(value = "0")
Module_Technology_Entry = tkinter.Label(user_panel_datasheet, textvariable=Module_Technology_entry_var)
Module_Technology_Entry.grid(row = 1 , column = 1, sticky="news", padx=10, pady=10 ) 

Module_Bifaciality_Label= tkinter.Label(user_panel_datasheet, text="Module Bifaciality")
Module_Bifaciality_Label.grid(row = 2 , column = 0, sticky="news", padx=10, pady=10 )
Module_Bifaciality_entry_var = tkinter.StringVar(value = "0")
Module_Bifaciality_Entry = tkinter.Label(user_panel_datasheet, textvariable=Module_Bifaciality_entry_var)
Module_Bifaciality_Entry.grid(row = 2 , column = 1, sticky="news", padx=10, pady=10 ) 









######Automatically adding padding to all children######
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

for widget in setup.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)






root.mainloop()