import tkinter
import tkinter.messagebox
import customtkinter
import tkintermapview
from tkinter.ttk import Progressbar
from tkinter import *
import importlib.metadata
import random
from pvmodule import Inverters 
from pvmodule import Modules 
from pvmodule import Irradiance
from tktooltip import ToolTip



customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Splash(tkinter.Toplevel):
    
    current_loadings = []
    def __init__(self, parent):

        self.initial_loadings = ["Start","Title","Sidebar","Appearence","Scaling","Entry","Main Button","TextBox","Tabview","Modules","Inverters","RadioButtons","ProgressBar","CheckBox","Delete Splash"]
        self.progress_status_value = 0
        tkinter.Toplevel.__init__(self, parent)
        self.title("Splash")
        width_of_window = 427
        height_of_window = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        self.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
        self.overrideredirect(1)

        s = tkinter.ttk.Style() 
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
        self.progress=Progressbar(self,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=500,mode='determinate')
        
        self.progress.place(x=-10,y=235)
        color = random.choice(['#2596be','#3ba1c5','#51abcb','#66b6d2'])
        Frame(self,width=427,height=241,bg=color).place(x=0,y=0)  

        

        ######## Label

        l1=Label(self,text='PV',fg='white',bg=color)
        lst1=('Calibri (Body)',18,'bold')
        l1.config(font=lst1)
        l1.place(x=50,y=80)

        l2=Label(self,text='Module',fg='white',bg=color)
        lst2=('Calibri (Body)',18)
        l2.config(font=lst2)
        l2.place(x=90,y=82)

        l3=Label(self,text=f'Version {importlib.metadata.version("pvmodule")}',fg='white',bg=color)
        lst3=('Calibri (Body)',13)
        l3.config(font=lst3)
        l3.place(x=50,y=110)

        l5=Label(self,text="Fábio Almeida",fg='white',bg=color)
        lst5=('Calibri (Body)',8)
        l5.config(font=lst5)
        l5.place(x=52,y=130)

        self.Loading_text = tkinter.StringVar(value = "Loading assets...")   
        l4=Label(self,textvariable=self.Loading_text,fg='white',bg=color)
        lst4=('Calibri (Body)',10)
        l4.config(font=lst4)
        l4.place(x=18,y=210)  
 


        self.update()

    def bar(self):
        self.Loading_text.set(self.current_loadings[-1] + "...")
        self.progress['value'] = len(self.current_loadings)/len(self.initial_loadings)*100
        self.update_idletasks()

        ## required to make window show before the program gets to the mainloop
        
        
class Loading(tkinter.Toplevel):
    

    def __init__(self, parent):

        tkinter.Toplevel.__init__(self, parent)
        self.title("Loading")
        width_of_window = 427
        height_of_window = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        self.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
        self.overrideredirect(1)

        s = tkinter.ttk.Style() 
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
        self.progress=Progressbar(self,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=500,mode='determinate')
    
        self.progress.place(x=-10,y=235)
        color = random.choice(['#2596be','#3ba1c5','#51abcb','#66b6d2'])
        Frame(self,width=427,height=241,bg=color).place(x=0,y=0)  

    

        ######## Label

        l1=Label(self,text='PV',fg='white',bg=color)
        lst1=('Calibri (Body)',18,'bold')
        l1.config(font=lst1)
        l1.place(x=50,y=80)

        l2=Label(self,text='Module',fg='white',bg=color)
        lst2=('Calibri (Body)',18)
        l2.config(font=lst2)
        l2.place(x=90,y=82)

        l3=Label(self,text=f'Version {importlib.metadata.version("pvmodule")}',fg='white',bg=color)
        lst3=('Calibri (Body)',13)
        l3.config(font=lst3)
        l3.place(x=50,y=110)

        l5=Label(self,text="Fábio Almeida",fg='white',bg=color)
        lst5=('Calibri (Body)',8)
        l5.config(font=lst5)
        l5.place(x=52,y=130)

        self.Loading_text = tkinter.StringVar(value = "Loading assets...")   
        l4=Label(self,textvariable=self.Loading_text,fg='white',bg=color)
        lst4=('Calibri (Body)',18)
        l4.config(font=lst4)
        l4.place(x=18,y=210)  
 
        self.update()

        ## required to make window show before the program gets to the mainloop


class App(customtkinter.CTk):
    def __init__(self):
        
        #pvmodule variables:
        self.pvmodule_module = None
        self.pvmodule_inverter = None

        super().__init__()
        splash = Splash(self)
        Splash(self).current_loadings.append("")        #<<<<<<<<--------------------
        Splash(self).bar()                              #<<<<<<<<--------------------


        # configure window
        self.title("PV Module GUI")
        #self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.geometry(f"{1100}x{600}")
        Splash(self).current_loadings.append("Loading fonts")   #<<<<<<<<--------------------
        Splash(self).bar()                                      #<<<<<<<<--------------------

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Solar Estimator", font=customtkinter.CTkFont(size=20, weight="bold"))
        
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=10)
        self.sidebar_button_1.configure(state="enabled", text="Select on Map", text_color="white")
        ToolTip(self.sidebar_button_1, msg="Opens a map widget where the user can click and it will automatically transfer the coordinates into the correct input.", delay=2.0)   # True by default


        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=10)
        self.Latitude_entry_var = tkinter.StringVar(value = "Latitude: 00.0000")   
        self.sidebar_button_2.configure(state="disabled", textvariable=self.Latitude_entry_var, text_color_disabled="black", fg_color="white")
        ToolTip(self.sidebar_button_2, msg="Latitude coordinates", delay=2.0)   # True by default


        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=10, pady=10)
        self.Longitude_entry_var = tkinter.StringVar(value = "Longitude: 00.0000")                                                
        self.sidebar_button_3.configure(state="disabled", textvariable=self.Longitude_entry_var, text_color_disabled="black", fg_color="white")
        ToolTip(self.sidebar_button_3, msg="Longitude coordinates", delay=2.0)   # True by default

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_4.grid(row=4, column=0, padx=10, pady=10)
        self.city_entry_var = tkinter.StringVar(value = "")                                                
        self.sidebar_button_4.configure(state="disabled", textvariable=self.city_entry_var, text_color_disabled="black", fg_color="white")
        ToolTip(self.sidebar_button_4, msg="City name of the location, if not known, 'None' will be displayed. This does not affect the results.", delay=2.0) 

        Splash(self).current_loadings.append("Loading sidebars")    #<<<<<<<<--------------------
        Splash(self).bar()                                  #<<<<<<<<--------------------








        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=5, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=5, pady=(10, 10))
        Splash(self).current_loadings.append("Loading appearances")     #<<<<<<<<--------------------
        Splash(self).bar()                                      #<<<<<<<<--------------------


        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=5, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=5, pady=(10, 20))
        Splash(self).current_loadings.append("Scaling assets")    #<<<<<<<<--------------------
        Splash(self).bar()                                        #<<<<<<<<--------------------

        self.about_button = customtkinter.CTkButton(master=self.sidebar_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="About", command=self.about_event)
        self.about_button.grid(row=10, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        Splash(self).current_loadings.append("Loading buttons")      #<<<<<<<<--------------------
        Splash(self).bar()                                          #<<<<<<<<--------------------

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        Splash(self).current_loadings.append("Loading buttons")    #<<<<<<<<--------------------
        Splash(self).bar()                                       #<<<<<<<<--------------------

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        Splash(self).current_loadings.append("Loading textboxes")  #<<<<<<<<--------------------
        Splash(self).bar()                                        #<<<<<<<<--------------------

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(10, 5), pady=(10, 10), sticky="nsew")
        self.tabview.add("Modules Selection")
        self.tabview.add("Inverters Selection")

        self.tabview.tab("Modules Selection").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Inverters Selection").grid_columnconfigure(0, weight=1)
        Splash(self).current_loadings.append("Loading tabviews")     #<<<<<<<<--------------------
        Splash(self).bar()                                           #<<<<<<<<--------------------
        
        self.tabview_information = customtkinter.CTkTabview(self, width=250)
        self.tabview_information.grid(row=0, column=3, padx=(5, 10), pady=(10, 10), sticky="nsew")
        self.tabview_information.add("Modules Info")
        self.tabview_information.add("Inverters Info")

        self.tabview_information.tab("Modules Info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview_information.tab("Inverters Info").grid_columnconfigure(0, weight=1)
        Splash(self).current_loadings.append("Loading tabviews")     #<<<<<<<<--------------------
        Splash(self).bar()                                           #<<<<<<<<--------------------



        def combofill_modules(event):                                                                               
            v = modules[ modules['Manufacturer'] == self.Module_List_Brand_menu.get()]['Model Number'].tolist()     
            self.Module_List_Model_menu.configure(values=v) 

        def fill_module_information(event):

            selected_module = modules.loc[modules['Model Number'] == event].squeeze()

            self.pvmodule_module = self.PVMODULE_define_module(event, 
                                                                ''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()),
                                                                ''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()), 
                                                                ''.join(c for c in str(self.module_losses.get()) if c.isdigit())
                                                                )
            self.Module_Amount_Input_string.configure(state="normal")
            self.Module_Amount_Input_array.configure(state="normal")
            self.Module_losses_Input_array.configure(state="normal")
            self.Auto_Select_Inverter_Button.configure(state="normal")


            self.module_wattage.set("DC Wattage: " + str(selected_module['Pmax']) + " W" )
            self.module_technology.set("Technology: " + str(selected_module['Technology']) )
            if selected_module['BIPV'] == 'N':
                self.module_bifaciality.set("Bifaciality: No")
            else:
                self.module_bifaciality.set("Bifaciality: Yes")
            self.module_isc.set("Short Circuit: "+ str(selected_module['Isc']) + " A" )
            self.module_voc.set("Open Circuit: " + str(selected_module['Voc']) + " V" )
            self.module_noct.set("NOCT: " + str(selected_module['NOCT']) )
            self.module_size.set("Size: " + str(selected_module['Short Side']) + ' x ' + str(selected_module['Long Side']))
            #self.module_n_cells.set("Nº Cells: " + str(selected_module['N_s']) )




            

            
        modules = Modules().list_modules(print_data=False)  
        module_brand = modules['Manufacturer'] 
        module_brand = list(dict.fromkeys(module_brand.tolist())) 
        
        self.Module_List_Brand_Label = customtkinter.CTkLabel(self.tabview.tab("Modules Selection"), text="Module Brand:")
        self.Module_List_Brand_Label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.Module_List_Brand_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Modules Selection"), dynamic_resizing=False,values=module_brand, command= combofill_modules)
        self.Module_List_Brand_menu.grid(row=0, column=1, padx=10, pady=(10, 10))
        
        self.Module_List_Model_Label = customtkinter.CTkLabel(self.tabview.tab("Modules Selection"), text="Module Model:")
        self.Module_List_Model_Label.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.Module_List_Model_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Modules Selection"), dynamic_resizing=False,values=[], command= fill_module_information)
        self.Module_List_Model_menu.grid(row=1, column=1, padx=10, pady=(10, 10))

        self.Module_Amount_Input_string = customtkinter.CTkButton(self.tabview.tab("Modules Selection"), state="disabled" ,text="Nº / String",command=self.open_input_dialog_amount_string)
        self.Module_Amount_Input_string.grid(row=2, column=0, padx=10, pady=(10, 10))
        self.modules_amount_string = tkinter.StringVar(value = "Modules: 1") 
        self.Module_Amount_Output_string = customtkinter.CTkLabel(self.tabview.tab("Modules Selection"), textvariable=self.modules_amount_string)
        self.Module_Amount_Output_string.grid(row=2, column=1, padx=10, pady=(10, 0))
        ToolTip(self.Module_Amount_Input_string, msg="The value represents the amount of modules are mounted in series (modules per string).", delay=2.0)   # True by default

        self.Module_Amount_Input_array = customtkinter.CTkButton(self.tabview.tab("Modules Selection"), state="disabled", text="Nº / Array",command=self.open_input_dialog_amount_array)
        self.Module_Amount_Input_array.grid(row=3, column=0, padx=10, pady=(10, 10))
        self.modules_amount_array = tkinter.StringVar(value = "Modules: 1") 
        self.Module_Amount_Output_array = customtkinter.CTkLabel(self.tabview.tab("Modules Selection"), textvariable=self.modules_amount_array)
        self.Module_Amount_Output_array.grid(row=3, column=1, padx=10, pady=(10, 0))
        ToolTip(self.Module_Amount_Input_array, msg="The value represents the amount of modules/string are mounted in paralel.", delay=2.0)   # True by default

        self.module_losses = tkinter.StringVar(value = "Losses: 0%") 
        self.Module_losses_Input_array = customtkinter.CTkLabel(self.tabview.tab("Modules Selection"), textvariable=self.module_losses)
        self.Module_losses_Input_array.grid(row=4, column=0, padx=10, pady=(10, 10))
        self.Module_losses_Input_array = customtkinter.CTkSlider(self.tabview.tab("Modules Selection"),state="disabled", from_=0, to=15, width=100 , command = self.slider_event)
        self.Module_losses_Input_array.grid(row=4, column=1, padx=10, pady=(10, 10))
        ToolTip(self.Module_losses_Input_array, msg="The percentage of losses the module has due to: \n-Dust\n-Damage\n-Partial Shading\n- ...", delay=2.0)   # True by default
        Splash(self).current_loadings.append("Importing Modules")  #<<<<<<<<--------------------
        Splash(self).bar()                               #<<<<<<<<--------------------



                                                                                                         
        def combofill_inverter(event):                                                                               
            v = self.inverters[ self.inverters['Manufacturer'] == self.Inverter_List_Brand_menu.get()]['Model Number'].tolist()
            self.Inverter_List_Model_menu.configure(values=v)


        self.inverters = Inverters().list_inverters()   
        inverter_brand = self.inverters['Manufacturer']                                                                  
        inverter_brand = list(dict.fromkeys(inverter_brand.tolist()))

        self.Inverter_List_Brand_Label = customtkinter.CTkLabel(self.tabview.tab("Inverters Selection"), text="Inverter Brand:")
        self.Inverter_List_Brand_Label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.Inverter_List_Brand_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Inverters Selection"), dynamic_resizing=False,values=inverter_brand, command= combofill_inverter)
        self.Inverter_List_Brand_menu.grid(row=0, column=1, padx=10, pady=(10, 10))

        self.Inverter_List_Model_Label = customtkinter.CTkLabel(self.tabview.tab("Inverters Selection"), text="Inverter Model:")
        self.Inverter_List_Model_Label.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.Inverter_List_Model_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Inverters Selection"), dynamic_resizing=False,values=[], command= self.fill_inverter_information)
        self.Inverter_List_Model_menu.grid(row=1, column=1, padx=10, pady=(10, 10))

        self.Auto_Select_Inverter_Button = customtkinter.CTkButton(self.tabview.tab("Inverters Selection"), state="disabled", command= self.PVMODULE_auto_select_inverter)
        self.Auto_Select_Inverter_Button.grid(row=2, column=0, padx=10, pady=10)
        self.Auto_Select_Inverter_Button.configure(text="Auto-select", text_color="white")
        ToolTip(self.Auto_Select_Inverter_Button, msg="Auto-select chooses a suitable inverter (not necessarily the best option available).", delay=2.0)   # True by default
        Splash(self).current_loadings.append("Importing Inverters")  #<<<<<<<<--------------------
        Splash(self).bar()                                 #<<<<<<<<--------------------


        self.scrollable_frame_modules = self.tabview_information.tab("Modules Info") #customtkinter.CTkScrollableFrame(self.tabview_information.tab("Modules"))
        #self.scrollable_frame_modules.grid(row=0, column=3,)
        #self.scrollable_frame_modules.grid_columnconfigure(1, weight=1)
        
        self.module_wattage = tkinter.StringVar(value = "DC Wattage:") 
        Module_Wattage = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_wattage}")
        Module_Wattage.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")

        self.module_size = tkinter.StringVar(value = "Size:") 
        Module_Size = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_size}")
        Module_Size.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")
        
        self.module_bifaciality = tkinter.StringVar(value = "Bifaciality:") 
        Module_Bifaciality = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_bifaciality}")
        Module_Bifaciality.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")
        
        self.module_technology = tkinter.StringVar(value = "Technology:") 
        Module_Technology = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_technology}")
        Module_Technology.grid(row=5, column=0, padx=10, pady=(0, 5), sticky="w")

        self.module_isc = tkinter.StringVar(value = "Short Circuit:") 
        Module_ISC = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_isc}")
        Module_ISC.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="w")

        self.module_voc = tkinter.StringVar(value = "Open Circuit:") 
        Module_VOC = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_voc}")
        Module_VOC.grid(row=7, column=0, padx=10, pady=(0, 5), sticky="w")

        self.module_noct = tkinter.StringVar(value = "NOCT:")  
        Module_NOCT = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_noct}")
        Module_NOCT.grid(row=8, column=0, padx=10, pady=(0, 5), sticky="w")

        #self.module_n_cells = tkinter.StringVar(value = "Nº Cells:") 
        #Module_N_Cells = customtkinter.CTkLabel(master=self.scrollable_frame_modules, textvariable=f"{self.module_n_cells}")
        #Module_N_Cells.grid(row=9, column=0, padx=10, pady=(0, 5), sticky="w")
        Splash(self).current_loadings.append("Adding Module Information")  #<<<<<<<<--------------------
        Splash(self).bar()                                 #<<<<<<<<--------------------



        self.scrollable_frame_inverter = self.tabview_information.tab("Inverters Info") # customtkinter.CTkScrollableFrame(self.tabview_information.tab("Inverters"))
        #self.scrollable_frame_inverter.grid(row=1, column=3, sticky="nsew")
        #self.scrollable_frame_inverter.grid_columnconfigure(0, weight=1)
        
        self.inverter_wattage = tkinter.StringVar(value = "AC Output: ") 
        Inverter_Wattage = customtkinter.CTkLabel(master=self.scrollable_frame_inverter, textvariable=f"{self.inverter_wattage}")
        Inverter_Wattage.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="w")

        self.inverter_paco = tkinter.StringVar(value = "Max Output Power:") 
        Inverter_max_dc_output= customtkinter.CTkLabel(master=self.scrollable_frame_inverter, textvariable=f"{self.inverter_paco}")
        Inverter_max_dc_output.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")

        self.inverter_max_mppt = tkinter.StringVar(value = "Max MPPT:") 
        Inverter_max_mppt= customtkinter.CTkLabel(master=self.scrollable_frame_inverter, textvariable=f"{self.inverter_max_mppt}")
        Inverter_max_mppt.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")

        self.inverter_min_mppt = tkinter.StringVar(value = "Min MPPT:") 
        Inverter_min_mppt= customtkinter.CTkLabel(master=self.scrollable_frame_inverter, textvariable=f"{self.inverter_min_mppt}")
        Inverter_min_mppt.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")

        self.inverter_nominal_voc = tkinter.StringVar(value = "Nominal Voltage:") 
        Inverter_max_voc= customtkinter.CTkLabel(master=self.scrollable_frame_inverter, textvariable=f"{self.inverter_nominal_voc}")
        Inverter_max_voc.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="w")

        self.inverter_efficiency = tkinter.StringVar(value = "Efficiency:") 
        Inverter_efficiency= customtkinter.CTkLabel(master=self.scrollable_frame_inverter, textvariable=f"{self.inverter_efficiency}")
        Inverter_efficiency.grid(row=5, column=0, padx=10, pady=(0, 5), sticky="w")
        Splash(self).current_loadings.append("Adding Module Information")  #<<<<<<<<--------------------
        Splash(self).bar()                                 #<<<<<<<<--------------------

        
        
        








        #self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Modules"),values=["Value 1", "Value 2", "Value Long....."])
        #self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        #self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Modules"), text="Open CTkInputDialog",command=self.open_input_dialog_event)
        #self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        #self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Inverters"), text="CTkLabel on Tab 2")
        #self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        #self.radiobutton_frame = customtkinter.CTkFrame(self)
        #self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        #self.radio_var = tkinter.IntVar(value=0)
        #self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        #self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        #self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        #self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        #self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        #self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        #self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        #self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
        #Splash(self).current_loadings.append("Loading radio buttons")  #<<<<<<<<--------------------
        #Splash(self).bar()                                    #<<<<<<<<--------------------

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")
        Splash(self).current_loadings.append("Loading progress bars")  #<<<<<<<<--------------------
        Splash(self).bar()                                   #<<<<<<<<--------------------

        # create scrollable frame
        #self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        #self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #self.scrollable_frame.grid_columnconfigure(0, weight=1)
        #self.scrollable_frame_switches = []
        #for i in range(100):
        #    switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
        #    switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        #    self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        #self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        #self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        #self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        #self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        #self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")
        #Splash(self).current_loadings.append("Loading checkboxes")  #<<<<<<<<--------------------
        #Splash(self).bar()                                #<<<<<<<<--------------------

        # set default values
        #self.checkbox_3.configure(state="disabled")
        #self.checkbox_1.select()
        #self.scrollable_frame_switches[0].select()
        #self.scrollable_frame_switches[4].select()
        #self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

        self.Module_List_Brand_menu.set("Module Brand")
        self.Module_List_Model_menu.set("Module Model")
        self.Inverter_List_Brand_menu.set("Inverter Brand")
        self.Inverter_List_Model_menu.set("Inverter Model")

        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.textbox.insert("0.0","")
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")


        Splash(self).current_loadings.append("")  #<<<<<<<<--------------------
        Splash(self).bar()                                     #<<<<<<<<--------------------
        splash.destroy()

    def fill_inverter_information(self,event):
            selected_inverter = self.inverters.loc[self.inverters['Model Number'] == event].squeeze()
            self.inverter_wattage.set("AC Output: " + str(selected_inverter['Nominal Voltage (Vac)']) + " V" )
            self.inverter_paco.set("Max Output Power: " + str(selected_inverter['Maximum Continuous Output Power (kW)']) + " kW")
            self.inverter_max_mppt.set("Max MPPT: "+ str(selected_inverter['Voltage Minimum (Vdc)']) + " V" )
            self.inverter_min_mppt.set("Min MPPT: "+ str(selected_inverter['Voltage Maximum (Vdc)']) + " V" )
            self.inverter_nominal_voc.set("Nominal Voltage : " + str(selected_inverter['Voltage Nominal (Vdc)']) + " V" )
            self.inverter_efficiency.set("Efficiency: " + str(selected_inverter['Weighted Efficiency (%)']) + " %" )

    def PVMODULE_auto_select_inverter(self):
        loading = Loading(self)

        if self.pvmodule_module == None:
            return tkinter.messagebox.showwarning(title="Error", message="No suitable inverter found.")

        else:
            self.pvmodule_inverter = Inverters().auto_select_inverter(module = self.pvmodule_module)
            inverter = self.pvmodule_inverter.squeeze()



            if inverter.empty:
                tkinter.messagebox.showwarning(title="Error", message="No suitable inverter found.")
            else:
                self.Inverter_List_Brand_menu.set(inverter['Manufacturer'])
                self.Inverter_List_Model_menu.set(inverter['Model Number'])
                self.fill_inverter_information(inverter['Model Number'])

        loading.destroy()

        return self.pvmodule_inverter 

    def PVMODULE_define_module(self,Model_name, nr_per_string, nr_per_array, losses):
        loading = Loading(self)

        return_module =  Modules().module(model = Model_name , 
                                          modules_per_string = float(nr_per_string) ,
                                          number_of_strings = float(nr_per_array) , 
                                          losses = float(losses))
        loading.destroy()
        return return_module
        

    def slider_event(self, value):
        self.module_losses.set(f"Losses: {round(int(value),0)}%")

        self.pvmodule_module['losses'] = float(''.join(c for c in str(self.module_losses.get()) if c.isdigit()))
 

    def open_input_dialog_amount_string(self):
        dialog = customtkinter.CTkInputDialog(text="mount of Modules per String", title="Amount of Modules per String")
        self.modules_amount_string.set(value = "Modules: " + str(dialog.get_input())) 

        if not ''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()).isdigit():
            self.pvmodule_module['number_of_strings'] = 1 
            self.modules_amount_string.set(value = "Modules: 1") 
        else:
            self.pvmodule_module['modules_per_string'] = float(''.join(c for c in str(self.modules_amount_string.get()) if c.isdigit()))


    def open_input_dialog_amount_array(self):
        dialog = customtkinter.CTkInputDialog(text="Amount of Modules per Array (amount of string)", title="Amount of Modules per Array")
        self.modules_amount_array.set(value = "Modules: " + str(dialog.get_input())) 

        if not ''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()).isdigit():
            self.pvmodule_module['number_of_strings'] = 1 
            self.modules_amount_array.set(value = "Modules: 1") 
        else:
            self.pvmodule_module['number_of_strings'] = float(''.join(c for c in str(self.modules_amount_array.get()) if c.isdigit()))

  
  


    def about_event(self):
        top= tkinter.Toplevel(self) 
        top.geometry(f"{400}x{350}") 
        top.title("About")                                                                                  
        map_frame = tkinter.Label(top, wraplength=350, text='''Copyright (c), 2023, Fabio Ramalho de Almeida
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.''')
        map_frame.grid(row = 0 , column = 0, padx = 20, pady = 10 ) 

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        top= tkinter.Toplevel(self)                                                                                  
        top.title("Map Window")                                                                                 
        map_frame = tkinter.Label(top, text="Location Selection Map")                                           
        map_frame.grid(row = 99 , column = 0, padx = 0, pady = 10 )                                             
        map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=0, padx=10, pady=10)
        map_widget.set_position(38.7557, -9.2803)  # Paris, France
        map_widget.set_zoom(12)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        map_widget.grid(row=4, column=0)                                                                        
                                                                                                                
        def left_click_event(coordinates_tuple):                                                                
            map_widget.delete_all_marker()                                                                      
            latitude = round(coordinates_tuple[0],4)                                                            
            longitude = round(coordinates_tuple[1],4)                                                           
            adr = tkintermapview.convert_coordinates_to_address(latitude, longitude)                            
            try:                                                                                                
                address_display = adr.street + ", " + adr.city                                                  
            except:                                                                                             
                address_display = "Street Address not found"                                                    
            city_name_marker = map_widget.set_marker(latitude, longitude, text=address_display)                 

            self.city_entry_var.set(str(adr.city))                                                                                                    
            self.Latitude_entry_var.set("Latitude: " + str(latitude))                                                                  
            self.Longitude_entry_var.set("Longitude: "+ str(longitude))                                                                  
            top.destroy()                                                                                       
            map_frame.destroy()                                                                                 
                                                                                                                
        map_widget.add_left_click_map_command(left_click_event)                                                 




if __name__ == "__main__":
    app = App()
    app.mainloop()
