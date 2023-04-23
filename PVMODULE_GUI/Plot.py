import customtkinter
from Loading import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from numpy import trapz as calculate_area_under_curve


class Plot():
    def __init__(self):
        pass


    def plot(self, yearly_irradiance, yearly_kwh,yearly_kwh_wp,yearly_in_plane_irr,sys_eff,capacity_factor,perfom_ratio):

        try:
            for widgets in self.third_frame.winfo_children():
                widgets.destroy()
        except:
            pass

        self.tabview_stats = customtkinter.CTkTabview(self.third_frame, width=300)
        self.tabview_stats.grid(row=1, column=6,columnspan=2, rowspan=5, padx=(10, 5), pady=(10, 10), sticky="nsew")
        self.tabview_stats.add("Yearly Statistics")
        self.tabview_stats.tab("Yearly Statistics").grid_columnconfigure(0, weight=1)
        #self.yearly_kwh, self.yearly_kwh_wp, self.yearly_in_plane_irr, self.sys_eff, self.capacity_factor, self.perfom_ratio
        

        yearly_kwh = tkinter.StringVar(value = f"Yearly Energy: {round(yearly_kwh,2)} [kWh]") 
        Yearly_kwh = customtkinter.CTkButton(master=self.tabview_stats.tab("Yearly Statistics"), anchor='w', state="disabled",text_color_disabled="white",textvariable=f"{yearly_kwh}")
        Yearly_kwh.grid(row=0, column=0, padx=50, pady=(self.tabview_stats.winfo_height()/10, 5), sticky="news")

        yearly_kwh_wp = tkinter.StringVar(value = f"Yearly Energy per Peak: {round(yearly_kwh_wp,2)} [kWh/Wp]") 
        Yearly_kwh_wp = customtkinter.CTkButton(master=self.tabview_stats.tab("Yearly Statistics"), anchor='w', state="disabled",text_color_disabled="white",textvariable=f"{yearly_kwh_wp}")
        Yearly_kwh_wp.grid(row=1, column=0, padx=50, pady=(self.tabview_stats.winfo_height()/10, 5), sticky="news")

        yearly_in_plane_irr = tkinter.StringVar(value = f"Yearly in-plane Irradiation: {round(yearly_in_plane_irr,2)} [kWh/m2]") 
        Yearly_in_plane_irr = customtkinter.CTkButton(master=self.tabview_stats.tab("Yearly Statistics"), anchor='w', state="disabled",text_color_disabled="white",textvariable=f"{yearly_in_plane_irr}")
        Yearly_in_plane_irr.grid(row=2, column=0, padx=50, pady=(self.tabview_stats.winfo_height()/10, 5), sticky="news")

        sys_eff = tkinter.StringVar(value = f"System Efficiency: {round(sys_eff,2)} %") 
        Sys_eff = customtkinter.CTkButton(master=self.tabview_stats.tab("Yearly Statistics"), anchor='w', state="disabled",text_color_disabled="white",textvariable=f"{sys_eff}")
        Sys_eff.grid(row=3, column=0, padx=50, pady=(self.tabview_stats.winfo_height()/10, 5), sticky="news")

        capacity_factor = tkinter.StringVar(value = f"Capacity Factor: {round(capacity_factor,2)} %") 
        Capacity_factor = customtkinter.CTkButton(master=self.tabview_stats.tab("Yearly Statistics"), anchor='w', state="disabled",text_color_disabled="white",textvariable=f"{capacity_factor}")
        Capacity_factor.grid(row=4, column=0, padx=50, pady=(self.tabview_stats.winfo_height()/10, 5), sticky="news")
        
        perfom_ratio = tkinter.StringVar(value = f"Performance Ratio: {round(perfom_ratio,2)} %") 
        Perfom_ratio = customtkinter.CTkButton(master=self.tabview_stats.tab("Yearly Statistics"), anchor='w', state="disabled",text_color_disabled="white",textvariable=f"{perfom_ratio}")
        Perfom_ratio.grid(row=5, column=0, padx=50, pady=(self.tabview_stats.winfo_height()/10, 5), sticky="news")
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
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
        
        self.yearly_kwah = yearly_irradiance

        first_data = yearly_irradiance.loc[yearly_irradiance['Month'] == 1]


        self.line1, = self.ax.plot(first_data.index, first_data['Total Irradiance'], color='red', marker='v',linewidth='0.5',linestyle = 'dotted', markersize=2)
        self.line2, = self.ax.plot(first_data.index, first_data['Irradiance w/m2'], color='magenta', marker='s',linewidth='0.5',linestyle = 'dashdot', markersize=2)
        self.line1.axes.set_title("Irradiance")

        self.line1_dc, = self.bx.plot(first_data.index, first_data['Total DC Power'], color='red', marker='v',linewidth='0.5',linestyle = 'dotted', markersize=2)
        self.line2_dc, = self.bx.plot(first_data.index, first_data['Total AC Power'], color='magenta', marker='s',linewidth='0.5',linestyle = 'dashdot', markersize=2)
        self.line1_dc.axes.set_title("Power")

       
        if customtkinter.get_appearance_mode() == "Dark":
            self.ax.legend(['Global Irradiance','Irradiance W/m2'],frameon=False, labelcolor="white")
            self.bx.legend(['Total DC Power (kW)','Total AC Power (kW)'],frameon=False, labelcolor="white")

        else:
            self.ax.legend(['Global Irradiance','Irradiance W/m2'],frameon=False, labelcolor="black")
            self.bx.legend(['Total DC Power (kW)','Total AC Power (kW)'],frameon=False, labelcolor="black")

        self.canvas = FigureCanvasTkAgg(self.fig,master=self.second_frame)
        self.canvas.get_tk_widget().grid(row=2, columnspan=5, padx=5, pady=5)
        self.second_frame.grid(row=0, column=1, padx=5, pady=5)
        self.simulate_button.configure(state="normal")


    def change_plotting_month(self, event):
        data_irr = pd.DataFrame()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
        data_irr = self.yearly_kwah.loc[self.yearly_kwah['Month'] == int(months.index(event))+1]

        self.line1.set_xdata(data_irr.index)
        self.line1.set_ydata(data_irr['Total Irradiance'])

        self.line2.set_xdata(data_irr.index)
        self.line2.set_ydata(data_irr['Irradiance w/m2'])


        self.line1_dc.set_xdata(data_irr.index)
        self.line1_dc.set_ydata(data_irr['Total DC Power'])

        self.line2_dc.set_xdata(data_irr.index)
        self.line2_dc.set_ydata(data_irr['Total AC Power'])


        self.ax.set_xlim(data_irr.index.min(),data_irr.index.max())
        self.ax.set_ylim(data_irr['Total Irradiance'].min(),data_irr['Total Irradiance'].max() + data_irr['Total Irradiance'].max()*0.1)

        self.bx.set_xlim(data_irr.index.min(),data_irr.index.max())
        self.bx.set_ylim(data_irr['Total DC Power'].min(),data_irr['Total DC Power'].max()+ data_irr['Total DC Power'].max()*0.1)
        if customtkinter.get_appearance_mode() == "Dark":
            self.ax.legend(['Global Irradiance','Irradiance W/m2'],frameon=False, labelcolor="white")
            self.bx.legend(['Total DC Power (kW)','Total AC Power (kW)'],frameon=False, labelcolor="white")

        else:
            self.ax.legend(['Global Irradiance','Irradiance W/m2'],frameon=False, labelcolor="black")
            self.bx.legend(['Total DC Power (kW)','Total AC Power (kW)'],frameon=False, labelcolor="black")
            self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=45)
            self.bx.set_xticklabels(self.bx.get_xticklabels(), rotation=45)


        total_irradiance = calculate_area_under_curve(y=data_irr['Total AC Power'],dx=24/len(data_irr.index))
        print(f"Find print 1: Total Power AC: {total_irradiance}")
        self.canvas.draw()