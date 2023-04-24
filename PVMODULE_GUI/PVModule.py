import customtkinter
import os
import tkinter.messagebox
from tkinter import *
from tktooltip import ToolTip
import PIL.Image
from Splash import *
from Map import *
from PPFD_Plot import *
from Get_Data_Threads import *
import threading
import multiprocessing
from multiprocessing import Process, Queue
from Plot import *
import webbrowser
import httpimport
import schedule, time
with httpimport.github_repo('fabio-r-almeida', 'pvmodule', ref='main'):
    import irradiance as IRRADIANCE
    import module as MODULE
    import inverter as INVERTER
    import pvmodule_version as VERSION_API
with open('VERSION.txt') as f:
    SOFTWARE_VERSION = f.readlines()[0].replace("__version__","").replace("'", "").replace("=", "").replace(" ", "")

import configparser


class App(customtkinter.CTk):
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config_dot_ini_theme = config['THEME']['value']
        customtkinter.set_appearance_mode(config_dot_ini_theme)


        #pvmodule variables:
        self.THREADS = Get_Data_Threads()

        self.threads= []
        self.stop_blinking_event = False

        self.pvmodule_module = None
        self.pvmodule_inverter = None
        self.pvmodule_location = None
        self.pvmodule_irradiance = None
        self.yearly_kwah = None
        self.pvmodule_albedo = 0.2
        self.pvmodule_panel_tilt = 35
        self.pvmodule_azimuth = 0
        self.pvmodule_elevation = 2
        self.pvmodule_module_spacing = None
        self.image_list_to_destroy = []
        super().__init__()
        splash = Splash()
        #if getattr(sys, 'frozen', False):
        #    import pyi_splash

        #splash.current_loadings.append("")        #<<<<<<<<--------------------
        #splash.bar()                              #<<<<<<<<--------------------
        
        self.geometry(f"{1200}x{600}")
    
        splash.current_loadings.append("Looking for updates")        #<<<<<<<<--------------------
        splash.bar()        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
            



        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(PIL.Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(PIL.Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(PIL.Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=PIL.Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=PIL.Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=PIL.Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=PIL.Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=PIL.Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=PIL.Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.yearly_analysis_image = customtkinter.CTkImage(light_image=PIL.Image.open(os.path.join(image_path, "Yearly_analysis_light.png")),
                                                     dark_image=PIL.Image.open(os.path.join(image_path, "Yearly_analysis_dark.png")), size=(20, 20))
        self.ppdf_dli = customtkinter.CTkImage(light_image=PIL.Image.open(os.path.join(image_path, "ppfd_light.png")),
                                                     dark_image=PIL.Image.open(os.path.join(image_path, "ppfd_dark.png")), size=(20, 20))
        
        self.iconbitmap(os.path.join(image_path, "icon.ico"))

        link = "https://raw.githubusercontent.com/fabio-r-almeida/Dissertation/main/PVMODULE_GUI/version.py?raw=true"
        changelog = "https://raw.githubusercontent.com/fabio-r-almeida/Dissertation/main/PVMODULE_GUI/changelog.py?raw=true"
        import requests
        f = requests.get(link)
        online_version = f.text.replace("__version__","").replace("'", "").replace("=", "").replace(" ", "")
        with open('VERSION.txt') as f:
            local_version = f.readlines()[0].replace("__version__","").replace("'", "").replace("=", "").replace(" ", "")
        if local_version == online_version:
            pass
        else:
            splash.destroy()
            f = requests.get(changelog)
            changes = f.text
            if tkinter.messagebox.askyesno(title="Update Available", message=f'Would you like to update?\n\n\nCurrent Version: {local_version}\nLatest Version: {online_version}\nChange Log:\n{changes}') == True:
                webbrowser.open_new_tab("https://github.com/fabio-r-almeida/Dissertation/blob/main/PVMODULE_GUI/Output/Pvmodule%20Installer.exe?raw=true")
                os._exit(1)
            splash = Splash()
        
        splash.current_loadings.append("Load Images")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------
        self.title(f"PV Module GUI {local_version}")

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Agro-Solar Estimator", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=(20,20), pady=20)



        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Setup",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")



        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Graphs",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        #self.frame_2_button.grid(row=2, column=0, sticky="ew")



        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Yearly Analysis",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.yearly_analysis_image, anchor="w", command=self.frame_3_button_event)
        
        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="PPFD & DLI",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.ppdf_dli, anchor="w", command=self.frame_4_button_event)
        #self.frame_3_button.grid(row=3, column=0, sticky="ew")




        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        splash.current_loadings.append("Loading Frames")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------


        self.versions1 = customtkinter.CTkLabel(self.navigation_frame,anchor="w", text="",fg_color="transparent",bg_color="transparent")
        self.versions1.grid(row=20, column=0, padx=(20, 20), pady=(0, 5), sticky="n")
        self.about_button = customtkinter.CTkButton(master=self.navigation_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="About", command=self.about_event)
        self.about_button.grid(row=20, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.versions = customtkinter.CTkLabel(self.navigation_frame,anchor="w", text=f"API:\t{VERSION_API.__version__}\nBuild:\t{SOFTWARE_VERSION}")
        self.versions.grid(row=21, column=0, padx=(20, 20), pady=(5, 0), sticky="s")


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




        self.albedo_values  = IRRADIANCE.Irradiance().list_albedo()
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
        ToolTip(self.sidebar_button_1, msg="Opens a map widget where the user can click and it will automatically transfer the coordinates into the correct input.", delay=1)   # True by default




        splash.current_loadings.append("Importing Modules")        #<<<<<<<<--------------------
        splash.bar()                                               #<<<<<<<<--------------------
     

        self.modules = MODULE.Modules().list_modules(print_data=False)  
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
        ToolTip(self.Module_Amount_Input_string, msg="The value represents the amount of modules are mounted in series (modules per string).", delay=1.0)   # True by default

        self.Module_Amount_Input_array = customtkinter.CTkButton(self.tabview_module.tab("Modules Selection"),fg_color="grey", state="disabled", text="Nº / Array",command=self.open_input_dialog_amount_array)
        self.Module_Amount_Input_array.grid(row=3, column=0, padx=10, pady=(10, 10))
        self.modules_amount_array = tkinter.StringVar(value = "Modules: 1") 
        self.Module_Amount_Output_array = customtkinter.CTkLabel(self.tabview_module.tab("Modules Selection"), textvariable=self.modules_amount_array)
        self.Module_Amount_Output_array.grid(row=3, column=1, padx=10, pady=(10, 0))
        ToolTip(self.Module_Amount_Input_array, msg="The value represents the amount of modules/string are mounted in paralel.", delay=1.0)   # True by default

        self.module_losses = tkinter.StringVar(value = "Losses: 0%") 
        self.Module_losses_Input_array = customtkinter.CTkLabel(self.tabview_module.tab("Modules Selection"), textvariable=self.module_losses)
        self.Module_losses_Input_array.grid(row=4, column=0, padx=10, pady=(10, 10))
        self.Module_losses_Input_array = customtkinter.CTkSlider(self.tabview_module.tab("Modules Selection"),state="disabled", fg_color="grey", from_=0, to=15, width=100 , command = self.slider_event)
        self.Module_losses_Input_array.grid(row=4, column=1, padx=10, pady=(10, 10))

        ToolTip(self.Module_losses_Input_array, msg="The percentage of losses the module has due to: \n-Dust\n-Damage\n-Partial Shading\n- ...", delay=1.0)   # True by default

                                                                                                         

        splash.current_loadings.append("Importing Inverters")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------

        self.inverters = INVERTER.Inverters().list_inverters()   
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
        ToolTip(self.Auto_Select_Inverter_Button, msg="Auto-select chooses a suitable inverter (not necessarily the best option available).", delay=1.0)   # True by default


        
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
        ToolTip(self.sidebar_button_2, msg="Latitude coordinates", delay=1.0)   # True by default

        self.sidebar_button_3 = customtkinter.CTkButton(self.tabview_information_pvgis_info.tab("PVGIS Info"))
        self.sidebar_button_3.grid(row=3, column=0, padx=50, pady=(0, 5), sticky="news")
        self.Longitude_entry_var = tkinter.StringVar(value = "Longitude: 00.0000")                                                
        self.sidebar_button_3.configure(state="disabled", textvariable=self.Longitude_entry_var, text_color_disabled="white")
        ToolTip(self.sidebar_button_3, msg="Longitude coordinates", delay=1.0)   # True by default
        
        self.simulate_button = customtkinter.CTkButton(master=self.tabview_information_pvgis_info.tab("PVGIS Info"), border_width=1, fg_color='#66ff99', text_color="black",text_color_disabled='black', text="Simulate", command=self.check_if_can_simulate)
        self.simulate_button.grid(row=4, column=0, padx=(50, 50), pady=(50, 5), sticky="nsew")
        
        self.checkbox_power_estimate = customtkinter.CTkCheckBox(master=self.tabview_information_pvgis_info.tab("PVGIS Info"), text="Power Estimation", onvalue=1, offvalue=0)
        self.checkbox_power_estimate.grid(row=5, column=0, padx=(25, 50), pady=(10, 5), sticky="nsew")
        self.checkbox_ppfd_dli = customtkinter.CTkCheckBox(master=self.tabview_information_pvgis_info.tab("PVGIS Info"), text="PPFD & DLI", onvalue=1, offvalue=0)
        self.checkbox_ppfd_dli.grid(row=6, column=0, padx=(25, 50), pady=(5, 5), sticky="nsew")
        
        splash.current_loadings.append("Importing Assets")          #<<<<<<<<--------------------
        splash.bar()                                                #<<<<<<<<--------------------

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")



        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")


        #if getattr(sys, 'frozen', False):
        #    pyi_splash.close()
        # select default frame
        #if getattr(sys, 'frozen', False):
        #    pyi_splash.close()

        splash.current_loadings.append("Initializing Assets")        #<<<<<<<<--------------------
        splash.bar()                              #<<<<<<<<--------------------
        self.select_frame_by_name("Setup")
        self.Module_List_Brand_menu.set("Module Brand")
        self.Module_List_Model_menu.set("Module Model")
        self.Inverter_List_Brand_menu.set("Inverter Brand")
        self.Inverter_List_Model_menu.set("Inverter Model")
        self.map_window_frame = None
        self.about_me_Toplevel = None
        self.appearance_mode_menu.set(config_dot_ini_theme)
        splash.destroy()
        self.protocol("WM_DELETE_WINDOW",  self.on_close)

        


    def about_event(self):
        if self.about_me_Toplevel is None or not self.about_me_Toplevel.winfo_exists():
            self.about_me_Toplevel= customtkinter.CTkToplevel(self) 
            self.about_me_Toplevel.geometry(f"{440}x{330}") 
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

            fill_info = threading.Thread(target=self.PVMODULE_define_module, args=(event, 
                                                                ''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()),
                                                                ''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()), 
                                                                ''.join(c for c in str(self.module_losses.get()) if c.isdigit()),)).start()
            self.Module_Amount_Input_string.configure(state="normal")
            self.Module_Amount_Input_string.configure(fg_color="#3b8ed0")
            self.Module_losses_Input_array.configure(fg_color="#3b8ed0")
            self.Module_Amount_Input_array.configure(fg_color="#3b8ed0")
            self.threads.append(fill_info)
            

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

   

    def check_if_can_simulate(self):
        self.second_frame.grid_forget()

        if self.PVGIS_Panel_Tilt_input.get() != '':
            self.pvmodule_panel_tilt = float(self.PVGIS_Panel_Tilt_input.get())

        if self.PVGIS_Ground_Albedo_menu.get() != '':
            list_of_albedos = IRRADIANCE.Irradiance().list_albedo()
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
                    self.simulate_button.configure(state="disabled")
                    try:
                        for widgets in self.second_frame.winfo_children():
                            widgets.destroy()
                        for widgets in self.third_frame.winfo_children():
                            widgets.destroy()
                        for widgets in self.fourth_frame.winfo_children():
                            widgets.destroy()
                    except:
                        pass
                 
                    #In order to not block the progress bars           
                    timer = threading.Timer(1.0, self.start_threads)
                    self.threads.append(timer)
                    timer.start()  # after 60 seconds, 'callback' will be called
                    

                except KeyError:
                    return tkinter.messagebox.showwarning(title="Error", message="Bad Location\n Location over sea or not covered.\n Please, select another location")
            else:
                return tkinter.messagebox.showwarning(title="Error", message="No Location selected")
        except KeyError:
            return tkinter.messagebox.showwarning(title="Error", message="No Module, Inverter or Location selected")

    def create_loading_progressbar(self, frame):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
        label_ = []
        progress_bar = []
        for i in range(1, 13): 
            if i <= 6:
                row = i
                column = 2
            else:
                row = i-6
                column = 4
            label = customtkinter.CTkLabel(frame, text=f"Importing {months[i-1]}")
            if row == 1:
                label.grid(row=row, column=column, padx=(10, 10), pady=(150, 10), sticky="nsew")
            else:
                label.grid(row=row, column=column, padx=(10, 10), pady=(10, 10), sticky="nsew")
            progress_bar_GRAPH = customtkinter.CTkProgressBar(master=frame)
            progress_bar_GRAPH.start()
            if row == 1:
                progress_bar_GRAPH.grid(row=row, column=column-1, padx=(100, 10), pady=(150, 10), sticky="nsew")                        
            else:
                progress_bar_GRAPH.grid(row=row, column=column-1, padx=(100, 10), pady=(10, 10), sticky="nsew")
            
            label_.append(label)
            progress_bar.append(progress_bar_GRAPH)
        return progress_bar, label_

    def start_threads(self): 
        if self.checkbox_power_estimate.get() == 1:
            self.select_frame_by_name("Graph")
            self.frame_2_button.grid(row=2, column=0, sticky="ew") 
            progress_bar, label = self.create_loading_progressbar(self.second_frame)
            queue = Queue()
            if self.pvmodule_module['BIPV'] == 'Y' and self.pvmodule_panel_tilt == 90:
                p1 = Process(target=self.THREADS.bi_PVMODULE_GET_DATA_THREAD_PER_MONTH, args=(queue, self.pvmodule_location, self.pvmodule_module, self.pvmodule_inverter, self.pvmodule_azimuth))
            else:
                p1 = Process(target=self.THREADS.PVMODULE_GET_DATA_THREAD_PER_MONTH, args=(queue, self.pvmodule_location, self.pvmodule_module, self.pvmodule_inverter, self.pvmodule_azimuth, self.pvmodule_panel_tilt))
        
            p1.start() 
            
        
            self.SYSdata, self.SYSyearly_kwh, self.SYSyearly_kwh_wp, self.SYSyearly_in_plane_irr, self.SYSsys_eff, self.SYScapacity_factor, self.SYSperfom_ratio =  queue.get()
            for i in range(0, len(progress_bar)): 
                            progress_bar[i].stop()
                            progress_bar[i].set(1)
                            progress_bar[i].grid_forget()
                            label[i].grid_forget()

            plot = threading.Thread(target=Plot.plot, args=(self, self.SYSdata, self.SYSyearly_kwh, self.SYSyearly_kwh_wp, self.SYSyearly_in_plane_irr, self.SYSsys_eff, self.SYScapacity_factor, self.SYSperfom_ratio,))
            self.threads.append(plot)
            plot.start()
            #Make 'Yearly Analysis', 'PPFD & DLI' buttons available
            self.frame_3_button.grid(row=3, column=0, sticky="ew")
            self.home_frame.grid_forget()
            self.fourth_frame.grid_forget()
            self.third_frame.grid_forget()

        if self.checkbox_ppfd_dli.get() == 1:
            self.frame_4_button.grid(row=4, column=0, sticky="ew") 
            queue_agro = Queue()
            p2 = Process(target=self.THREADS.PVMODULE_GET_PPDF_DLI, args=(queue_agro, self.pvmodule_location, ))
            progress_bar, label = self.create_loading_progressbar(self.fourth_frame)
            p2.start()  
            self.SYSAgro_data, self.SYSppfd_dli = queue_agro.get()
            if self.checkbox_power_estimate.get() == 1:
                self.stop_blinking_event = False
                self.blinking_button = threading.Thread(target=self.run_threaded, args=(self.frame_4_button,))
                self.blinking_button.start()
                
            for i in range(0, len(progress_bar)): 
                            progress_bar[i].stop()
                            progress_bar[i].set(1)
                            progress_bar[i].grid_forget()
                            label[i].grid_forget()

            
            ppfd_dli_plot = threading.Thread(target=PPFD_Plot.plot_ppfd, args=(self, self.SYSAgro_data, self.SYSppfd_dli ,))
            self.threads.append(ppfd_dli_plot)
            ppfd_dli_plot.start()
            self.home_frame.grid_forget()
            self.third_frame.grid_forget()
            self.fourth_frame.grid_forget()




        
    def change_plotting_month(self, event):
        Plot.change_plotting_month(self, event)

    
    def start_blink_button_frame(self, button):
        print("Start blink button frame")
        button.configure(fg_color=("gray70", "gray30"))
        time.sleep(1)
        button.configure(fg_color='transparent')
        time.sleep(1)
        if not self.stop_blinking_event:
            self.blinking_button = threading.Thread(target=self.run_threaded, args=(self.frame_4_button,))
            self.blinking_button.start()

        #self.blinking_button = schedule.every(4).seconds.do(self.run_threaded, button=self.frame_4_button)
        #self.blinking_button.run()


    def run_threaded(self, button):
        self.blinking_button = threading.Thread(target=self.start_blink_button_frame, args=(button,))
        self.blinking_button.start()
        self.blinking_button.join()

    





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
            self.pvmodule_inverter = INVERTER.Inverters().inverter(name=selected_inverter['Model Number'])

    def PVMODULE_auto_select_inverter(self):
        if self.pvmodule_module == None:
            return tkinter.messagebox.showwarning(title="Error", message="No module selected found.")
        else:
            self.pvmodule_inverter, self.pvmodule_module = INVERTER.Inverters().auto_select_inverter(module = self.pvmodule_module)
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
        self.pvmodule_module =  MODULE.Modules().module(model = Model_name , modules_per_string = float(nr_per_string) ,number_of_strings = float(nr_per_array) , losses = float(losses))
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
        Map.pick_on_map(self)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Setup" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "Graph" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "Yearly Analysis" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "PPFD & DLI" else "transparent")
        # show selected frame
        if name == "Setup":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Graph":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "Yearly Analysis":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "PPFD & DLI":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()



    def home_button_event(self):
        self.select_frame_by_name("Setup")

    def frame_2_button_event(self):
        self.select_frame_by_name("Graph")

    def frame_3_button_event(self):
        self.select_frame_by_name("Yearly Analysis")

    def frame_4_button_event(self):
        try:
            self.stop_blinking_event = True
        except:
            pass
        self.select_frame_by_name("PPFD & DLI")

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

        parser = configparser.ConfigParser()
        parser.read('config.ini')
        parser.set('THEME', 'value', str(new_appearance_mode))
        with open("config.ini", "w+") as configfile:
            parser.write(configfile)



    def on_close(self):
        close = tkinter.messagebox.askokcancel("Close", "Would you like to close the program?")
        if close:
            for thread in self.threads:
                try:
                    thread.raise_exception()
                    thread.kill()
                except:
                    pass
            os._exit(1)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = App()
    app.mainloop()


