import customtkinter
import os
import tkinter.messagebox
import customtkinter
import tkintermapview
from tkinter import *
from pvmodule import *
from tktooltip import ToolTip
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from numpy import trapz as calculate_area_under_curve
from Loading import *
from Splash import *
import pandas as pd

import threading

customtkinter.set_appearance_mode("Dark")
class App(customtkinter.CTk):
    
    def __init__(self):
        #pvmodule variables:
        self.pvmodule_module = None
        self.pvmodule_inverter = None
        self.pvmodule_location = None
        self.pvmodule_irradiance = None
        self.pvmodule_albedo = 0.2
        self.pvmodule_panel_tilt = 35
        self.pvmodule_azimuth = 0
        self.pvmodule_elevation = 2
        self.pvmodule_module_spacing = None
        self.image_list_to_destroy = []

        super().__init__()
        splash = Splash()

        splash.current_loadings.append("")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------

        self.title("PV Module GUI")
        self.geometry(f"{1200}x{600}")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)



        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        
        
        splash.current_loadings.append("Load Images")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Solar Estimator", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=(20,20), pady=20)



        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Setup",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")



        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Graphs",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")



        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")




        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        splash.current_loadings.append("Loading Frames")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------



        self.about_button = customtkinter.CTkButton(master=self.navigation_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="About", command=self.about_event)
        self.about_button.grid(row=10, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        
        splash.current_loadings.append("Loading Assets")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------


       
        # create tabview
        self.tabview_module = customtkinter.CTkTabview(self.home_frame, width=300)
        self.tabview_module.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew")
        self.tabview_module.add("Modules Selection")
        self.tabview_module.tab("Modules Selection").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
 


        self.tabview_inverter = customtkinter.CTkTabview(self.home_frame, width=300)
        self.tabview_inverter.grid(row=0, column=1, padx=(10, 5), pady=(10, 10), sticky="nsew")
        self.tabview_inverter.add("Inverters Selection")
        self.tabview_inverter.tab("Inverters Selection").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.tabview_PVGIS = customtkinter.CTkTabview(self.home_frame, width=300)
        self.tabview_PVGIS.grid(row=0, column=2, padx=(10, 5), pady=(10, 10), sticky="nsew")
        self.tabview_PVGIS.add("PVGIS Selection")
        self.tabview_PVGIS.tab("PVGIS Selection").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs


        
        self.tabview_information_module_info = customtkinter.CTkTabview(self.home_frame, width=250)
        self.tabview_information_module_info.add("Modules Info")
        self.tabview_information_module_info.grid_remove()

        self.tabview_information_inverter_info = customtkinter.CTkTabview(self.home_frame, width=250)
        self.tabview_information_inverter_info.add("Inverters Info")
        self.tabview_information_inverter_info.grid_remove()

        self.tabview_information_pvgis_info = customtkinter.CTkTabview(self.home_frame, width=250)
        self.tabview_information_pvgis_info.add("PVGIS Info")
        self.tabview_information_pvgis_info.grid_remove()

        self.tabview_information_module_info.tab("Modules Info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview_information_inverter_info.tab("Inverters Info").grid_columnconfigure(0, weight=1)
        self.tabview_information_pvgis_info.tab("PVGIS Info").grid_columnconfigure(0, weight=1)




        self.albedo_values  = Irradiance().list_albedo()
        self.albedo_values  = self.albedo_values['Surface'] 
        self.albedo_values  = list(dict.fromkeys(self.albedo_values .tolist())) 

        self.PVGIS_Panel_Tilt = customtkinter.CTkLabel(self.tabview_PVGIS.tab("PVGIS Selection"), text="Module Tilt:")
        self.PVGIS_Panel_Tilt.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.PVGIS_Panel_Tilt_input = customtkinter.CTkEntry(self.tabview_PVGIS.tab("PVGIS Selection"), placeholder_text="default: 35")
        self.PVGIS_Panel_Tilt_input.grid(row=0, column=1, padx=10, pady=(10, 10))


        self.PVGIS_Ground_Albedo = customtkinter.CTkLabel(self.tabview_PVGIS.tab("PVGIS Selection"), text="Albedo:")
        self.PVGIS_Ground_Albedo.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.PVGIS_Ground_Albedo_menu = customtkinter.CTkOptionMenu(self.tabview_PVGIS.tab("PVGIS Selection"), dynamic_resizing=False,values=self.albedo_values)
        self.PVGIS_Ground_Albedo_menu.grid(row=1, column=1, padx=10, pady=(10, 10))

        self.PVGIS_Module_azimuth = customtkinter.CTkLabel(self.tabview_PVGIS.tab("PVGIS Selection"), text="Azimuth:")
        self.PVGIS_Module_azimuth.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.Module_azimuth_array = customtkinter.CTkEntry(self.tabview_PVGIS.tab("PVGIS Selection"), placeholder_text="-180 to 180, default: 0")
        self.Module_azimuth_array.grid(row=2, column=1, padx=10, pady=(10, 10))

        self.PVGIS_Panel_Spacing = customtkinter.CTkLabel(self.tabview_PVGIS.tab("PVGIS Selection"), text="Module Spacing:")
        self.PVGIS_Panel_Spacing.grid(row=3, column=0, padx=10, pady=(10, 0))
        self.PVGIS_Panel_Spacing_Input_array = customtkinter.CTkEntry(self.tabview_PVGIS.tab("PVGIS Selection"), placeholder_text="default: Automatic")
        self.PVGIS_Panel_Spacing_Input_array.grid(row=3, column=1, padx=10, pady=(10, 10))


        self.sidebar_button_1 = customtkinter.CTkButton(self.tabview_PVGIS.tab("PVGIS Selection"), command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=4, columnspan=2, padx=10, pady=10)
        self.sidebar_button_1.configure(state="enabled", text="Select on Map", text_color="white")
        ToolTip(self.sidebar_button_1, msg="Opens a map widget where the user can click and it will automatically transfer the coordinates into the correct input.", delay=2.0)   # True by default




        splash.current_loadings.append("Importing Modules")        #<<<<<<<<--------------------
        splash.bar()                                               #<<<<<<<<--------------------
     

        self.modules = Modules().list_modules(print_data=False)  
        self.modules = self.modules.sort_values(by=['Manufacturer'])
        self.module_brand = self.modules['Manufacturer'] 
        self.module_brand = list(dict.fromkeys(self.module_brand.tolist())) 
        
        self.Module_List_Brand_Label = customtkinter.CTkLabel(self.tabview_module.tab("Modules Selection"), text="Module Brand:")
        self.Module_List_Brand_Label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.Module_List_Brand_menu = customtkinter.CTkOptionMenu(self.tabview_module.tab("Modules Selection"), dynamic_resizing=False,values=self.module_brand, command= self.combofill_modules)
        self.Module_List_Brand_menu.grid(row=0, column=1, padx=10, pady=(10, 10))
        
        self.Module_List_Model_Label = customtkinter.CTkLabel(self.tabview_module.tab("Modules Selection"), text="Module Model:")
        self.Module_List_Model_Label.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.Module_List_Model_menu = customtkinter.CTkOptionMenu(self.tabview_module.tab("Modules Selection"), fg_color="grey", state="disabled",dynamic_resizing=False, values=['Module Models'], command= self.fill_module_information)
        self.Module_List_Model_menu.grid(row=1, column=1, padx=10, pady=(10, 10))

        self.Module_Amount_Input_string = customtkinter.CTkButton(self.tabview_module.tab("Modules Selection"), state="disabled" ,fg_color="grey" ,text="Nº / String",command=self.open_input_dialog_amount_string)
        self.Module_Amount_Input_string.grid(row=2, column=0, padx=10, pady=(10, 10))
        self.modules_amount_string = tkinter.StringVar(value = "Modules: 1") 
        self.Module_Amount_Output_string = customtkinter.CTkLabel(self.tabview_module.tab("Modules Selection"), textvariable=self.modules_amount_string)
        self.Module_Amount_Output_string.grid(row=2, column=1, padx=10, pady=(10, 0))
        ToolTip(self.Module_Amount_Input_string, msg="The value represents the amount of modules are mounted in series (modules per string).", delay=2.0)   # True by default

        self.Module_Amount_Input_array = customtkinter.CTkButton(self.tabview_module.tab("Modules Selection"),fg_color="grey", state="disabled", text="Nº / Array",command=self.open_input_dialog_amount_array)
        self.Module_Amount_Input_array.grid(row=3, column=0, padx=10, pady=(10, 10))
        self.modules_amount_array = tkinter.StringVar(value = "Modules: 1") 
        self.Module_Amount_Output_array = customtkinter.CTkLabel(self.tabview_module.tab("Modules Selection"), textvariable=self.modules_amount_array)
        self.Module_Amount_Output_array.grid(row=3, column=1, padx=10, pady=(10, 0))
        ToolTip(self.Module_Amount_Input_array, msg="The value represents the amount of modules/string are mounted in paralel.", delay=2.0)   # True by default

        self.module_losses = tkinter.StringVar(value = "Losses: 0%") 
        self.Module_losses_Input_array = customtkinter.CTkLabel(self.tabview_module.tab("Modules Selection"), textvariable=self.module_losses)
        self.Module_losses_Input_array.grid(row=4, column=0, padx=10, pady=(10, 10))
        self.Module_losses_Input_array = customtkinter.CTkSlider(self.tabview_module.tab("Modules Selection"),state="disabled", fg_color="grey", from_=0, to=15, width=100 , command = self.slider_event)
        self.Module_losses_Input_array.grid(row=4, column=1, padx=10, pady=(10, 10))

        ToolTip(self.Module_losses_Input_array, msg="The percentage of losses the module has due to: \n-Dust\n-Damage\n-Partial Shading\n- ...", delay=2.0)   # True by default

                                                                                                         

        splash.current_loadings.append("Importing Inverters")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------

        self.inverters = Inverters().list_inverters()   
        inverter_brand = self.inverters['Manufacturer']                                                                  
        inverter_brand = list(dict.fromkeys(inverter_brand.tolist()))

        self.Inverter_List_Brand_Label = customtkinter.CTkLabel(self.tabview_inverter.tab("Inverters Selection"), text="Inverter Brand:")
        self.Inverter_List_Brand_Label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.Inverter_List_Brand_menu = customtkinter.CTkOptionMenu(self.tabview_inverter.tab("Inverters Selection"), dynamic_resizing=False,values=inverter_brand, command= self.combofill_inverter)
        self.Inverter_List_Brand_menu.grid(row=0, column=1, padx=10, pady=(10, 10))

        self.Inverter_List_Model_Label = customtkinter.CTkLabel(self.tabview_inverter.tab("Inverters Selection"), text="Inverter Model:")
        self.Inverter_List_Model_Label.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.Inverter_List_Model_menu = customtkinter.CTkOptionMenu(self.tabview_inverter.tab("Inverters Selection"), fg_color="grey", state="disabled", dynamic_resizing=False,values=["Inverter Model"], command= self.fill_inverter_information)
        self.Inverter_List_Model_menu.grid(row=1, column=1, padx=10, pady=(10, 10))

        self.Auto_Select_Inverter_Button = customtkinter.CTkButton(self.tabview_inverter.tab("Inverters Selection"), fg_color="grey", state="disabled", command= self.PVMODULE_auto_select_inverter)
        self.Auto_Select_Inverter_Button.grid(row=2, column=0, padx=10, pady=10)
        self.Auto_Select_Inverter_Button.configure(text="Auto-select", text_color="white")
        ToolTip(self.Auto_Select_Inverter_Button, msg="Auto-select chooses a suitable inverter (not necessarily the best option available).", delay=2.0)   # True by default


        
        self.module_wattage = tkinter.StringVar(value = "DC Wattage:") 
        Module_Wattage = customtkinter.CTkButton(master=self.tabview_information_module_info.tab("Modules Info"), state="disabled",text_color_disabled="white",textvariable=f"{self.module_wattage}")
        Module_Wattage.grid(row=0, column=0, padx=50, pady=(0, 5), sticky="news")

        self.module_size = tkinter.StringVar(value = "Size:") 
        Module_Size = customtkinter.CTkButton(master=self.tabview_information_module_info.tab("Modules Info"),state="disabled",text_color_disabled="white", textvariable=f"{self.module_size}")
        Module_Size.grid(row=1, column=0, padx=50, pady=(0, 5), sticky="news")
        
        self.module_bifaciality = tkinter.StringVar(value = "Bifaciality:") 
        Module_Bifaciality = customtkinter.CTkButton(master=self.tabview_information_module_info.tab("Modules Info"),state="disabled",text_color_disabled="white", textvariable=f"{self.module_bifaciality}")
        Module_Bifaciality.grid(row=2, column=0, padx=50, pady=(0, 5), sticky="news")
        
        self.module_technology = tkinter.StringVar(value = "Technology:") 
        Module_Technology = customtkinter.CTkButton(master=self.tabview_information_module_info.tab("Modules Info"), state="disabled",text_color_disabled="white",textvariable=f"{self.module_technology}")
        Module_Technology.grid(row=3, column=0, padx=50, pady=(0, 5), sticky="news")

        self.module_isc = tkinter.StringVar(value = "Short Circuit:") 
        Module_ISC = customtkinter.CTkButton(master=self.tabview_information_module_info.tab("Modules Info"),state="disabled",text_color_disabled="white", textvariable=f"{self.module_isc}")
        Module_ISC.grid(row=4, column=0, padx=50, pady=(0, 5), sticky="news")

        self.module_voc = tkinter.StringVar(value = "Open Circuit:") 
        Module_VOC = customtkinter.CTkButton(master=self.tabview_information_module_info.tab("Modules Info"),state="disabled",text_color_disabled="white", textvariable=f"{self.module_voc}")
        Module_VOC.grid(row=5, column=0, padx=50, pady=(0, 5), sticky="news")

        self.module_noct = tkinter.StringVar(value = "NOCT:")  
        Module_NOCT = customtkinter.CTkButton(master=self.tabview_information_module_info.tab("Modules Info"),state="disabled",text_color_disabled="white", textvariable=f"{self.module_noct}")
        Module_NOCT.grid(row=6, column=0, padx=50, pady=(0, 5), sticky="news")

     


        self.inverter_wattage = tkinter.StringVar(value = "AC Output: ") 
        Inverter_Wattage = customtkinter.CTkButton(master=self.tabview_information_inverter_info.tab("Inverters Info") ,state="disabled", text_color_disabled="white",textvariable=f"{self.inverter_wattage}")
        Inverter_Wattage.grid(row=0, column=0, padx=50, pady=(0, 5), sticky="news")

        self.inverter_paco = tkinter.StringVar(value = "Max Output Power:") 
        Inverter_max_dc_output= customtkinter.CTkButton(master=self.tabview_information_inverter_info.tab("Inverters Info") ,state="disabled",text_color_disabled="white", textvariable=f"{self.inverter_paco}")
        Inverter_max_dc_output.grid(row=1, column=0, padx=50, pady=(0, 5), sticky="news")

        self.inverter_max_mppt = tkinter.StringVar(value = "Max MPPT:") 
        Inverter_max_mppt= customtkinter.CTkButton(master=self.tabview_information_inverter_info.tab("Inverters Info") ,state="disabled",text_color_disabled="white", textvariable=f"{self.inverter_max_mppt}")
        Inverter_max_mppt.grid(row=2, column=0, padx=50, pady=(0, 5), sticky="news")

        self.inverter_min_mppt = tkinter.StringVar(value = "Min MPPT:") 
        Inverter_min_mppt= customtkinter.CTkButton(master=self.tabview_information_inverter_info.tab("Inverters Info") ,state="disabled",text_color_disabled="white", textvariable=f"{self.inverter_min_mppt}")
        Inverter_min_mppt.grid(row=3, column=0, padx=50, pady=(0, 5), sticky="news")
        
        self.inverter_efficiency = tkinter.StringVar(value = "Efficiency:") 
        Inverter_efficiency= customtkinter.CTkButton(master=self.tabview_information_inverter_info.tab("Inverters Info") ,state="disabled",text_color_disabled="white", textvariable=f"{self.inverter_efficiency}")
        Inverter_efficiency.grid(row=4, column=0, padx=50, pady=(0, 5), sticky="news")

        self.inverter_nominal_voc = tkinter.StringVar(value = "Nominal Voltage:") 
        Inverter_max_voc= customtkinter.CTkButton(master=self.tabview_information_inverter_info.tab("Inverters Info") ,state="disabled",text_color_disabled="white", textvariable=f"{self.inverter_nominal_voc}")
        Inverter_max_voc.grid(row=5, column=0, padx=50, pady=(0, 5), sticky="news")

        self.sidebar_button_2 = customtkinter.CTkButton(self.tabview_information_pvgis_info.tab("PVGIS Info"))
        self.sidebar_button_2.grid(row=2, column=0, padx=50, pady=(0, 5), sticky="news")
        self.Latitude_entry_var = tkinter.StringVar(value = "Latitude: 00.0000")   
        self.sidebar_button_2.configure(state="disabled", textvariable=self.Latitude_entry_var, text_color_disabled="white")
        ToolTip(self.sidebar_button_2, msg="Latitude coordinates", delay=2.0)   # True by default

        self.sidebar_button_3 = customtkinter.CTkButton(self.tabview_information_pvgis_info.tab("PVGIS Info"))
        self.sidebar_button_3.grid(row=3, column=0, padx=50, pady=(0, 5), sticky="news")
        self.Longitude_entry_var = tkinter.StringVar(value = "Longitude: 00.0000")                                                
        self.sidebar_button_3.configure(state="disabled", textvariable=self.Longitude_entry_var, text_color_disabled="white")
        ToolTip(self.sidebar_button_3, msg="Longitude coordinates", delay=2.0)   # True by default
        
        self.simulate_button = customtkinter.CTkButton(master=self.tabview_information_pvgis_info.tab("PVGIS Info"), border_width=1, fg_color='#66ff99', text_color="black",text_color_disabled='black', text="Simulate", command=self.check_if_can_simulate)
        self.simulate_button.grid(row=4, column=0, padx=(50, 50), pady=(50, 5), sticky="nsew")
        splash.current_loadings.append("Importing Assets")          #<<<<<<<<--------------------
        splash.bar()                                                #<<<<<<<<--------------------

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")



        # create third frame
        #self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")



        # select default frame
        splash.current_loadings.append("Initializing Assets")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------
        self.select_frame_by_name("Setup")
        self.Module_List_Brand_menu.set("Module Brand")
        self.Module_List_Model_menu.set("Module Model")
        self.Inverter_List_Brand_menu.set("Inverter Brand")
        self.Inverter_List_Model_menu.set("Inverter Model")
        self.map_window_frame = None
        self.about_me_Toplevel = None
        self.appearance_mode_menu.set("Dark")
        splash.destroy()
        self.protocol("WM_DELETE_WINDOW",  self.on_close)
        


    def about_event(self):
        if self.about_me_Toplevel is None or not self.about_me_Toplevel.winfo_exists():
            self.about_me_Toplevel= customtkinter.CTkToplevel(self) 
            self.about_me_Toplevel.geometry(f"{400}x{330}") 
            self.about_me_Toplevel.title("About")                                                                                  
            map_frame = customtkinter.CTkLabel(self.about_me_Toplevel, wraplength=350, text='''Copyright (c), 2023, Fábio Ramalho de Almeida
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.''')
            map_frame.grid(row = 0 , column = 0, padx = 20, pady = 10 ) 
            self.about_me_Toplevel.focus()
        else:
            self.about_me_Toplevel.focus()
        
    def combofill_modules(self,event):                                                                               
            v = self.modules[ self.modules['Manufacturer'] == self.Module_List_Brand_menu.get()]['Model Number'].tolist()     
            self.Module_List_Model_menu.configure(values=v) 
            self.Module_List_Model_menu.configure(fg_color="#3b8ed0")
            self.Module_List_Model_menu.configure(state="normal")

    def fill_module_information(self, event):

            selected_module = self.modules.loc[self.modules['Model Number'] == event].squeeze()

            threading.Thread(target=self.PVMODULE_define_module, args=(event, 
                                                                ''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()),
                                                                ''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()), 
                                                                ''.join(c for c in str(self.module_losses.get()) if c.isdigit()),)).start()
            self.Module_Amount_Input_string.configure(state="normal")
            self.Module_Amount_Input_string.configure(fg_color="#3b8ed0")
            self.Module_losses_Input_array.configure(fg_color="#3b8ed0")
            self.Module_Amount_Input_array.configure(fg_color="#3b8ed0")
            

            self.Module_Amount_Input_array.configure(state="normal")
            self.Module_losses_Input_array.configure(state="normal")

            self.module_wattage.set("DC Wattage: " + str(selected_module['Pmax']) + " W" )
            self.module_technology.set("Technology: " + str(selected_module['Technology']) )
            if str(selected_module['BIPV']) == 'N':
                self.module_bifaciality.set("Bifaciality: No")
            else:
                self.module_bifaciality.set("Bifaciality: Yes")
            self.module_isc.set("Short Circuit: "+ str(float(selected_module['Isc'])) + " A" )
            self.module_voc.set("Open Circuit: " + str(selected_module['Voc']) + " V" )
            self.module_noct.set("NOCT: " + str(selected_module['NOCT']) )
            self.module_size.set("Size: " + str(selected_module['Short Side']) + ' x ' + str(selected_module['Long Side']))
            self.tabview_information_module_info.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

    def PVMODULE_GET_DATA_THREAD_jan(self):
        _, data, _ = Irradiance().irradiance(_month=1,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_jan = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_January.stop()
        self.thread_progressbar_January.set(1)
        self.thread_progressbar_January.grid_forget()
        self.thread_progressbar_January_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_jan = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_feb(self):
        _, data, _ = Irradiance().irradiance(_month=2,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_feb = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_February.stop()
        self.thread_progressbar_February.set(1)
        self.thread_progressbar_February.grid_forget()
        self.thread_progressbar_February_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_feb = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_mar(self):
        _, data, _ = Irradiance().irradiance(_month=3,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_mar = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_March.stop()
        self.thread_progressbar_March.set(1)
        self.thread_progressbar_March.grid_forget()
        self.thread_progressbar_March_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_mar = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_apr(self):
        _, data, _ = Irradiance().irradiance(_month=4,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_apr = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_April.stop()
        self.thread_progressbar_April.set(1)
        self.thread_progressbar_April.grid_forget()
        self.thread_progressbar_April_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_apr = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_may(self):
        _, data, _ = Irradiance().irradiance(_month=5,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_may = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_May.stop()
        self.thread_progressbar_May.set(1)
        self.thread_progressbar_May.grid_forget()
        self.thread_progressbar_May_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_may = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_jun(self):
        _, data, _ = Irradiance().irradiance(_month=6,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_jun = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_June.stop()
        self.thread_progressbar_June.set(1)
        self.thread_progressbar_June.grid_forget()
        self.thread_progressbar_June_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_jun = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_jul(self):
        _, data, _ = Irradiance().irradiance(_month=7,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_jul = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_July.stop()
        self.thread_progressbar_July.set(1)
        self.thread_progressbar_July.grid_forget()
        self.thread_progressbar_July_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_jul = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_aug(self):
        _, data, _ = Irradiance().irradiance(_month=8,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_aug = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_August.stop()
        self.thread_progressbar_August.set(1)
        self.thread_progressbar_August.grid_forget()
        self.thread_progressbar_August_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_aug = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_sep(self):
        _, data, _ = Irradiance().irradiance(_month=9,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_sep = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_September.stop()
        self.thread_progressbar_September.set(1)
        self.thread_progressbar_September.grid_forget()
        self.thread_progressbar_September_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_sep = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_oct(self):
        _, data, _ = Irradiance().irradiance(_month=10,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_oct = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_October.stop()
        self.thread_progressbar_October.set(1)
        self.thread_progressbar_October.grid_forget()
        self.thread_progressbar_October_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_oct = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_nov(self):
        _, data, _ = Irradiance().irradiance(_month=11,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_nov = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_November.stop()
        self.thread_progressbar_November.set(1)
        self.thread_progressbar_November.grid_forget()
        self.thread_progressbar_November_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_nov = data
        self.thread_counter = self.thread_counter - 1

    def PVMODULE_GET_DATA_THREAD_dec(self):
        _, data, _ = Irradiance().irradiance(_month=12,module=self.pvmodule_module, location=self.pvmodule_location, panel_tilt=self.pvmodule_panel_tilt, azimuth=self.pvmodule_azimuth, albedo=self.pvmodule_albedo,panel_distance=self.pvmodule_module_spacing)
        self.pvmodule_dc_output_dec = System().dc_production(self.pvmodule_module, data)
        self.thread_progressbar_December.stop()
        self.thread_progressbar_December.set(1)
        self.thread_progressbar_December.grid_forget()
        self.thread_progressbar_December_Label.grid_forget()
        data.sort_index(inplace=True)
        self.pvmodule_irradiance_dec = data
        self.thread_counter = self.thread_counter - 1
    



    def CHECK_FOR_THREADS(self):
        while self.thread_counter > 0:
            print("")
            pass
        import seaborn as sns

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
        self.months_convert = dict(January=1, February=2, March=3, April=4, May=5, June=6, July=7, August=8, September=9, October=10, November=11,December=12)
        self.monthly_data = ""
        self.change_month_label = customtkinter.CTkLabel(self.second_frame, text="Month:")                                           
        self.change_month_label.grid(row = 0 , column=6, padx=10, pady=(10, 10))
        self.change_month = customtkinter.CTkOptionMenu(self.second_frame, dynamic_resizing=False,values=months, command= self.change_plotting_month)
        self.change_month.grid(row=0, column=7, padx=10, pady=(10, 10))
        self.change_month.set('January')
        self.fig = Figure(facecolor='#242424')  
        self.bx = self.fig.add_subplot(212)
        self.ax = self.fig.add_subplot(211)
        self.fig.tight_layout()
        
        self.ax.spines['bottom'].set_color('#144870')
        self.ax.spines['top'].set_color('#144870') 
        self.ax.spines['right'].set_color('#144870')
        self.ax.spines['left'].set_color('#144870')
        self.ax.title.set_color('#3b8ed0')
        self.ax.yaxis.label.set_color('#3b8ed0')
        self.ax.xaxis.label.set_color('#3b8ed0')
        self.ax.tick_params(axis='x', colors='#3b8ed0')
        self.ax.tick_params(axis='y', colors='#3b8ed0')
        self.ax.set_facecolor("#2b2b2b")
        
        self.bx.spines['bottom'].set_color('#144870')
        self.bx.spines['top'].set_color('#144870') 
        self.bx.spines['right'].set_color('#144870')
        self.bx.spines['left'].set_color('#144870')
        self.bx.title.set_color('#3b8ed0')
        self.bx.yaxis.label.set_color('#3b8ed0')
        self.bx.xaxis.label.set_color('#3b8ed0')
        self.bx.tick_params(axis='x', colors='#3b8ed0')
        self.bx.tick_params(axis='y', colors='#3b8ed0')
        self.bx.set_facecolor("#2b2b2b")
        if customtkinter.get_appearance_mode() == "Dark":
            self.ax.set_facecolor("#2b2b2b")
            self.bx.set_facecolor("#2b2b2b")
            self.fig.set_facecolor("#242424")
        else:
            self.ax.set_facecolor("#dbdbdb")
            self.bx.set_facecolor("#dbdbdb")
            self.fig.set_facecolor("#ebebeb")


        self.line1, = self.ax.plot(self.pvmodule_irradiance_jan['Time_H'], self.pvmodule_irradiance_jan['Total_G'], color='red', marker='v',linewidth='0.5',linestyle = 'dotted', markersize=2)
        self.line2, = self.ax.plot(self.pvmodule_irradiance_jan['Time_H'], self.pvmodule_irradiance_jan['G_Front'], color='magenta', marker='s',linewidth='0.5',linestyle = 'dashdot', markersize=2)
        self.line3, = self.ax.plot(self.pvmodule_irradiance_jan['Time_H'], self.pvmodule_irradiance_jan['G_Rear'], color='green', marker='d',linewidth='0.5',linestyle = 'dotted', markersize=2)
        self.line1.axes.set_title("Irradiance")

        self.line1_dc, = self.bx.plot(self.pvmodule_dc_output_jan['Time_H'], self.pvmodule_dc_output_jan['Total DC Power'], color='red', marker='v',linewidth='0.5',linestyle = 'dotted', markersize=2)
        self.line2_dc, = self.bx.plot(self.pvmodule_dc_output_jan['Time_H'], self.pvmodule_dc_output_jan['Front DC Power'], color='magenta', marker='s',linewidth='0.5',linestyle = 'dashdot', markersize=2)
        self.line3_dc, = self.bx.plot(self.pvmodule_dc_output_jan['Time_H'], self.pvmodule_dc_output_jan['Rear DC Power'], color='green', marker='d',linewidth='0.5',linestyle = 'dotted', markersize=2)
        self.line1_dc.axes.set_title("Power")

        


       
        if customtkinter.get_appearance_mode() == "Dark":
            self.ax.legend(['Global Irradiance W/m2','Front Irradiance W/m2','Rear Irradiance W/m2'],frameon=False, labelcolor="white")
            self.bx.legend(['Total DC Power (W)','Front DC Power (W)','Rear DC Power (W)'],frameon=False, labelcolor="white")

        else:
            self.ax.legend(['Global Irradiance W/m2','Front Irradiance W/m2','Rear Irradiance W/m2'],frameon=False, labelcolor="black")
            self.bx.legend(['Total DC Power (W)','Front DC Power (W)','Rear DC Power (W)'],frameon=False, labelcolor="black")

        self.canvas = FigureCanvasTkAgg(self.fig,master=self.second_frame)
        self.canvas.get_tk_widget().grid(row=2, columnspan=5, padx=5, pady=5)
        self.second_frame.grid(row=0, column=1, padx=5, pady=5)
        self.simulate_button.configure(state="normal")
        


    def check_if_can_simulate(self):
        self.second_frame.grid_forget()

        if self.PVGIS_Panel_Tilt_input.get() != '':
            self.pvmodule_panel_tilt = float(self.PVGIS_Panel_Tilt_input.get())

        if self.PVGIS_Ground_Albedo_menu.get() != '':
            list_of_albedos = Irradiance().list_albedo()
            albedo = list_of_albedos.loc[list_of_albedos['Surface'] == self.PVGIS_Ground_Albedo_menu.get()]
            self.pvmodule_albedo = float(albedo['Albedo Average'])

        if self.Module_azimuth_array.get() != '':
            self.pvmodule_azimuth = float(self.Module_azimuth_array.get())

        if self.PVGIS_Panel_Spacing_Input_array.get() != '':
            self.pvmodule_module_spacing = float(self.PVGIS_Panel_Spacing_Input_array.get())
        
        can_simulate = False
        try:

            if self.pvmodule_module != None:
                can_simulate = True
            else:
                can_simulate = False
                return tkinter.messagebox.showwarning(title="Error", message="No Module selected")
            if not self.pvmodule_inverter.empty and can_simulate:
                pass
            else:
                return tkinter.messagebox.showwarning(title="Error", message="No Inverter selected")
            if self.pvmodule_location != None and can_simulate:
            
                try:
                    self.select_frame_by_name("Graph")
                    self.simulate_button.configure(state="disabled")
                    self.thread_progressbar_January_Label = customtkinter.CTkLabel(self.second_frame, text="Importing January")                                           
                    self.thread_progressbar_January_Label.grid(row=1, column=2, padx=(10, 10), pady=(150, 10), sticky="nsew")
                    self.thread_progressbar_January = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_January.start()
                    self.thread_progressbar_January.grid(row=1, column=1, padx=(100, 10), pady=(150, 10), sticky="nsew")

                    self.thread_progressbar_February_Label = customtkinter.CTkLabel(self.second_frame, text="Importing February")                                           
                    self.thread_progressbar_February_Label.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_February= customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_February.start()
                    self.thread_progressbar_February.grid(row=2, column=1, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_March_Label = customtkinter.CTkLabel(self.second_frame, text="Importing March")                                           
                    self.thread_progressbar_March_Label.grid(row=3, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_March = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_March.start()
                    self.thread_progressbar_March.grid(row=3, column=1, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_April_Label = customtkinter.CTkLabel(self.second_frame, text="Importing April")                                           
                    self.thread_progressbar_April_Label.grid(row=4, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_April = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_April.start()
                    self.thread_progressbar_April.grid(row=4, column=1, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_May_Label = customtkinter.CTkLabel(self.second_frame, text="Importing May")                                           
                    self.thread_progressbar_May_Label.grid(row=5, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_May = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_May.start()
                    self.thread_progressbar_May.grid(row=5, column=1, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_June_Label = customtkinter.CTkLabel(self.second_frame, text="Importing June")                                           
                    self.thread_progressbar_June_Label.grid(row=6, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_June = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_June.start()
                    self.thread_progressbar_June.grid(row=6, column=1, padx=(100, 10), pady=(10, 10), sticky="nsew")
                    
                    self.thread_progressbar_July_Label = customtkinter.CTkLabel(self.second_frame, text="Importing July")                                           
                    self.thread_progressbar_July_Label.grid(row=1, column=4, padx=(10, 10), pady=(150, 10), sticky="nsew")
                    self.thread_progressbar_July = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_July.start()
                    self.thread_progressbar_July.grid(row=1, column=3, padx=(100, 10), pady=(150, 10), sticky="nsew")

                    self.thread_progressbar_August_Label = customtkinter.CTkLabel(self.second_frame, text="Importing August")                                           
                    self.thread_progressbar_August_Label.grid(row=2, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_August = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_August.start()
                    self.thread_progressbar_August.grid(row=2, column=3, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_September_Label = customtkinter.CTkLabel(self.second_frame, text="Importing September")                                           
                    self.thread_progressbar_September_Label.grid(row=3, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_September = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_September.start()
                    self.thread_progressbar_September.grid(row=3, column=3, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_October_Label = customtkinter.CTkLabel(self.second_frame, text="Importing October")                                           
                    self.thread_progressbar_October_Label.grid(row=4, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_October = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_October.start()
                    self.thread_progressbar_October.grid(row=4, column=3, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_November_Label = customtkinter.CTkLabel(self.second_frame, text="Importing November")                                           
                    self.thread_progressbar_November_Label.grid(row=5, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_November = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_November.start()
                    self.thread_progressbar_November.grid(row=5, column=3, padx=(100, 10), pady=(10, 10), sticky="nsew")

                    self.thread_progressbar_December_Label = customtkinter.CTkLabel(self.second_frame, text="Importing December")                                           
                    self.thread_progressbar_December_Label.grid(row=6, column=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
                    self.thread_progressbar_December = customtkinter.CTkProgressBar(master=self.second_frame)
                    self.thread_progressbar_December.start()
                    self.thread_progressbar_December.grid(row=6, column=3, padx=(100, 10), pady=(10, 10), sticky="nsew")
                    
                    
                    timer = threading.Timer(1.0, self.start_threads)
                    timer.start()  # after 60 seconds, 'callback' will be called

                    

                except KeyError:
                    return tkinter.messagebox.showwarning(title="Error", message="Bad Location\n Location over sea or not covered.\n Please, select another location")
            else:
                return tkinter.messagebox.showwarning(title="Error", message="No Location selected")
        except KeyError:
            return tkinter.messagebox.showwarning(title="Error", message="No Module, Inverter or Location selected")

    def start_threads(self):
        thread1 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_jan)
        thread1.start()
        thread2 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_feb)
        thread2.start()
        thread3 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_mar)
        thread3.start()
        thread4 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_apr)
        thread4.start()
        thread5 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_may)
        thread5.start()
        thread6 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_jun)
        thread6.start()
        thread7 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_jul)
        thread7.start()
        thread8 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_aug)
        thread8.start()
        thread9 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_sep)
        thread9.start()
        thread10 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_oct)
        thread10.start()
        thread11 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_nov)
        thread11.start()
        thread12 = threading.Thread(target=self.PVMODULE_GET_DATA_THREAD_dec)
        thread12.start()
        self.thread_counter = 12
        check_for_threads = threading.Thread(target=self.CHECK_FOR_THREADS)
        check_for_threads.start()
        

    def change_plotting_month(self, event):
        data_irr = pd.DataFrame()
        data_pwr = pd.DataFrame()
        if event == "January":
            data_irr = self.pvmodule_irradiance_jan
            data_pwr = self.pvmodule_dc_output_jan
        if event == "February":
            data_irr = self.pvmodule_irradiance_feb
            data_pwr = self.pvmodule_dc_output_feb
        if event == "March":
            data_irr = self.pvmodule_irradiance_mar
            data_pwr = self.pvmodule_dc_output_mar
        if event == "April":
            data_irr = self.pvmodule_irradiance_apr
            data_pwr = self.pvmodule_dc_output_apr
        if event == "May":
            data_irr = self.pvmodule_irradiance_may
            data_pwr = self.pvmodule_dc_output_may
        if event == "June":
            data_irr = self.pvmodule_irradiance_jun
            data_pwr = self.pvmodule_dc_output_jun
        if event == "July":
            data_irr = self.pvmodule_irradiance_jul
            data_pwr = self.pvmodule_dc_output_jul
        if event == "August":
            data_irr = self.pvmodule_irradiance_aug
            data_pwr = self.pvmodule_dc_output_aug
        if event == "September":
            data_irr = self.pvmodule_irradiance_sep
            data_pwr = self.pvmodule_dc_output_sep
        if event == "October":
            data_irr = self.pvmodule_irradiance_oct
            data_pwr = self.pvmodule_dc_output_oct
        if event == "November":
            data_irr = self.pvmodule_irradiance_nov
            data_pwr = self.pvmodule_dc_output_nov
        if event == "December":
            data_irr = self.pvmodule_irradiance_dec
            data_pwr = self.pvmodule_dc_output_dec

        self.line1.set_xdata(data_irr['Time_H'])
        self.line1.set_ydata(data_irr['Total_G'])

        self.line2.set_xdata(data_irr['Time_H'])
        self.line2.set_ydata(data_irr['G_Front'])

        self.line3.set_xdata(data_irr['Time_H'])
        self.line3.set_ydata(data_irr['G_Rear'])

        self.line1_dc.set_xdata(data_pwr['Time_H'])
        self.line1_dc.set_ydata(data_pwr['Total DC Power'])

        self.line2_dc.set_xdata(data_pwr['Time_H'])
        self.line2_dc.set_ydata(data_pwr['Front DC Power'])

        self.line3_dc.set_xdata(data_pwr['Time_H'])
        self.line3_dc.set_ydata(data_pwr['Rear DC Power'])

        self.ax.set_xlim(data_irr['Time_H'].min(),data_irr['Time_H'].max())
        self.ax.set_ylim(data_irr['Total_G'].min(),data_irr['Total_G'].max() + 50)

        self.bx.set_xlim(data_pwr['Time_H'].min(),data_pwr['Time_H'].max())
        self.bx.set_ylim(data_pwr['Total DC Power'].min(),data_pwr['Total DC Power'].max() + 50)
        if customtkinter.get_appearance_mode() == "Dark":
            self.ax.legend(['Global Irradiance W/m2','Front Irradiance W/m2','Rear Irradiance W/m2'],frameon=False, labelcolor="white")
            self.bx.legend(['Total DC Power (W)','Front DC Power (W)','Rear DC Power (W)'],frameon=False, labelcolor="white")

        else:
            self.ax.legend(['Global Irradiance W/m2','Front Irradiance W/m2','Rear Irradiance W/m2'],frameon=False, labelcolor="black")
            self.bx.legend(['Total DC Power (W)','Front DC Power (W)','Rear DC Power (W)'],frameon=False, labelcolor="black")


        total_irradiance = calculate_area_under_curve(y=data_pwr['Total DC Power'],dx=24/len(data_pwr.index))
        print(f"Find print 1: Total Power DC: {total_irradiance}")
        self.canvas.draw()





        


    def combofill_inverter(self, event):                                                                               
            v = self.inverters[ self.inverters['Manufacturer'] == self.Inverter_List_Brand_menu.get()]['Model Number'].tolist()
            self.Inverter_List_Model_menu.configure(values=v)
            self.Inverter_List_Model_menu.configure(fg_color="#3b8ed0")
            self.Inverter_List_Model_menu.configure(state="normal")


    def fill_inverter_information(self,event):
            self.tabview_information_inverter_info.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
            selected_inverter = self.inverters.loc[self.inverters['Model Number'] == event].squeeze()
            self.inverter_wattage.set("AC Output: " + str(selected_inverter['Nominal Voltage (Vac)']) + " V" )
            self.inverter_paco.set("Max Output Power: " + str(selected_inverter['Maximum Continuous Output Power (kW)']) + " kW")
            self.inverter_max_mppt.set("Max MPPT: "+ str(selected_inverter['Voltage Maximum (Vdc)']) + " V" )
            self.inverter_min_mppt.set("Min MPPT: "+ str(selected_inverter['Voltage Minimum (Vdc)']) + " V" )
            self.inverter_nominal_voc.set("Nominal Voltage : " + str(selected_inverter['Voltage Nominal (Vdc)']) + " V" )
            self.inverter_efficiency.set("Efficiency: " + str(selected_inverter['Weighted Efficiency (%)']) + " %" )
            self.pvmodule_inverter = Inverters().inverter(name=selected_inverter['Model Number'])

    def PVMODULE_auto_select_inverter(self):
        if self.pvmodule_module == None:
            return tkinter.messagebox.showwarning(title="Error", message="No module selected found.")
        else:
            self.pvmodule_inverter = Inverters().auto_select_inverter(module = self.pvmodule_module)
            inverter = self.pvmodule_inverter.squeeze()

            if inverter.empty:
                tkinter.messagebox.showwarning(title="Error", message="No suitable inverter found.")
            else:
                self.Inverter_List_Brand_menu.set(inverter['Manufacturer'])
                self.Inverter_List_Model_menu.set(inverter['Model Number'])
                self.fill_inverter_information(inverter['Model Number'])

        
        self.Inverter_List_Model_menu.configure(fg_color="#3b8ed0")
        self.Inverter_List_Model_menu.configure(state="normal")
        self.combofill_inverter(self.Inverter_List_Brand_menu.get())
        return self.pvmodule_inverter 

    def PVMODULE_define_module(self,Model_name, nr_per_string, nr_per_array, losses):
        self.pvmodule_module =  Modules().module(model = Model_name , modules_per_string = float(nr_per_string) ,number_of_strings = float(nr_per_array) , losses = float(losses))
        self.Auto_Select_Inverter_Button.configure(state="normal")
        self.Auto_Select_Inverter_Button.configure(fg_color="#3b8ed0")
        return self.pvmodule_module
        

    def slider_event(self, value):
        self.module_losses.set(f"Losses: {round(int(value),0)}%")
        self.pvmodule_module['losses'] = float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))
        selected_module = self.modules.loc[self.modules['Model Number'] == self.Module_List_Model_menu.get()].squeeze()
        num = float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))
        count = 0
        while num != 0:
            num //= 10
            count += 1
        if count > 4:
            self.module_isc.set("Short Circuit: "+ str(round(float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))/1000,2)) + " kA" )
        else:
            self.module_isc.set("Short Circuit: "+ str(round(float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit())),2)) + " A" )
        
        num = selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))
        count = 0
        while num != 0:
            num //= 10
            count += 1
        if count > 4:
            self.module_voc.set("Open Circuit: " + str(round(selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))/1000,2)) + " kV" )
        else:
            self.module_voc.set("Open Circuit: " + str(round(selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit())),2)) + " V" )
        
        num = selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)
        count = 0
        while num != 0:
            num //= 10
            count += 1

        if count > 7 :
            self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)/1000000,2)) + " MW" )
        elif count > 4:
            self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)/1000,2)) + " kW" )
        else:
            self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100),2)) + " W" )
    
        self.pvmodule_module['modules_per_string'] = float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))
 

    def open_input_dialog_amount_string(self):
        dialog = customtkinter.CTkInputDialog(text="mount of Modules per String", title="Amount of Modules per String")
        self.modules_amount_string.set(value = "Modules: " + str(dialog.get_input())) 
        selected_module = self.modules.loc[self.modules['Model Number'] == self.Module_List_Model_menu.get()].squeeze()

        if not ''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()).isdigit():
            self.pvmodule_module['number_of_strings'] = 1 
            self.modules_amount_string.set(value = "Modules: 1") 
        else:

            num = float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))
            count = 0
            while num != 0:
                num //= 10
                count += 1
            if count > 4:
                self.module_isc.set("Short Circuit: "+ str(round(float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))/1000,2)) + " kA" )
            else:
                self.module_isc.set("Short Circuit: "+ str(round(float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit())),2)) + " A" )
        
            num = selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))
            count = 0
            while num != 0:
                num //= 10
                count += 1
            if count > 4:
                self.module_voc.set("Open Circuit: " + str(round(selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))/1000,2)) + " kV" )
            else:
                self.module_voc.set("Open Circuit: " + str(round(selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit())),2)) + " V" )
             
            num = selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)
            count = 0
            while num != 0:
                num //= 10
                count += 1
            if count > 7 :
                self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)/1000000,2)) + " MW" )
            elif count > 4:
                self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)/1000,2)) + " kW" )
            else:
                self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100),2)) + " W" )
    
            self.pvmodule_module['modules_per_string'] = float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))




    def open_input_dialog_amount_array(self):
        dialog = customtkinter.CTkInputDialog(text="Amount of Modules per Array (amount of string)", title="Amount of Modules per Array")
        self.modules_amount_array.set(value = "Modules: " + str(dialog.get_input())) 

        if not ''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()).isdigit():
            self.pvmodule_module['number_of_strings'] = 1 
            self.modules_amount_array.set(value = "Modules: 1") 
        else:
            self.pvmodule_module['number_of_strings'] = float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))
            selected_module = self.modules.loc[self.modules['Model Number'] == self.Module_List_Model_menu.get()].squeeze()
            num = float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))
            count = 0
            while num != 0:
                num //= 10
                count += 1
            if count > 4:
                self.module_isc.set("Short Circuit: "+ str(round(float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))/1000,2)) + " kA" )
            else:
                self.module_isc.set("Short Circuit: "+ str(round(float(selected_module['Isc'])*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit())),2)) + " A" )
            
            num = selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))
            count = 0
            while num != 0:
                num //= 10
                count += 1
            if count > 4:
                self.module_voc.set("Open Circuit: " + str(round(selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))/1000,2)) + " kV" )
            else:
                self.module_voc.set("Open Circuit: " + str(round(selected_module['Voc']*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit())),2)) + " V" )
            
            num = selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)
            count = 0
            while num != 0:
                num //= 10
                count += 1
            if count > 7 :
                self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)/1000000,2)) + " MW" )
            elif count > 4:
                self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100)/1000,2)) + " kW" )
            else:
                self.module_wattage.set("DC Wattage: " + str(round(selected_module['Pmax']*float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))*float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))*(1-float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))/100),2)) + " W" )
    
            self.pvmodule_module['modules_per_string'] = float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def sidebar_button_event(self):
        if self.map_window_frame is None or not self.map_window_frame.winfo_exists():

            self.map_window_frame= customtkinter.CTkToplevel(self)                                                                                  
            self.map_window_frame.title("Map Window")                                                                                 
            map_frame = customtkinter.CTkLabel(self.map_window_frame, text="")                                           
            map_frame.grid(row = 0 , column = 0, padx = 0, pady = 0 )                                             
            map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=0, padx=0, pady=0)
            map_widget.set_position(38.7557, -9.2803)  # Oeiras, Portugal
            map_widget.set_zoom(12)
            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
            map_widget.grid(row=4, column=0)
            self.map_window_frame.focus() 
            self.map_window_frame.overrideredirect(True)                                                                       

            def left_click_event(coordinates_tuple):

                loading = Loading() 
                loading.current_loadings.append("Reading map coordinates")
                loading.bar()

                map_widget.delete_all_marker()                                                                      
                latitude = round(coordinates_tuple[0],4)                                                            
                longitude = round(coordinates_tuple[1],4)                                                           

                self.pvmodule_location = Location().set_location(latitude=latitude, longitude=longitude)
                self.tabview_information_pvgis_info.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
                                                                                                 
                self.Latitude_entry_var.set("Latitude: " + str(latitude))                                                                  
                self.Longitude_entry_var.set("Longitude: "+ str(longitude))                                                                  
                self.map_window_frame.destroy()                                                                                       
                loading.destroy()                                                                      

            map_widget.add_left_click_map_command(left_click_event) 
        else:
            self.map_window_frame.focus()                                                


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Setup" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "Graph" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        # show selected frame
        if name == "Setup":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Graph":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        #if name == "frame_3":
        #    self.third_frame.grid(row=0, column=1, sticky="nsew")
        #else:
        #    self.third_frame.grid_forget()



    def home_button_event(self):
        self.select_frame_by_name("Setup")

    def frame_2_button_event(self):
        self.select_frame_by_name("Graph")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        try:
            if new_appearance_mode == "Dark":
                        self.ax.set_facecolor("#2b2b2b")
                        self.bx.set_facecolor("#2b2b2b")
                        self.fig.set_facecolor("#242424")
                        self.ax.legend(['Global Irradiance W/m2','Front Irradiance W/m2','Rear Irradiance W/m2'],frameon=False, labelcolor="white")

            else:
                        self.ax.set_facecolor("#dbdbdb")
                        self.bx.set_facecolor("#dbdbdb")
                        self.fig.set_facecolor("#ebebeb")
                        self.ax.legend(['Global Irradiance W/m2','Front Irradiance W/m2','Rear Irradiance W/m2'],frameon=False, labelcolor="black")

        except:
            pass
        customtkinter.set_appearance_mode(new_appearance_mode)


    def on_close(self):
        #custom close options, here's one example:
        close = tkinter.messagebox.askokcancel("Close", "Would you like to close the program?")
        if close:
            import os
            os._exit(1)





if __name__ == '__main__':


    app = App()
    app.mainloop()


