import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from numpy import trapz as calculate_area_under_curve
import tkinter
from tabulate import tabulate
import tkinter.messagebox

class Plot():
    def __init__(self):
        pass


    def plot(self, yearly_irradiance, yearly_kwh,yearly_kwh_wp,yearly_in_plane_irr,sys_eff,capacity_factor,perfom_ratio):

        try:
            for widgets in self.third_frame.winfo_children():
                widgets.destroy()
        except:
            pass
        months = ['Units','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']

        data = pd.DataFrame(columns=['Month','Total DC','Irradiance','T cell','Efficiency','Total AC'], index = months)
        for i in range(len(months)-1):
            Total_DC_Power = yearly_irradiance.loc[yearly_irradiance['Month'] == int(i+1)]
            Total_DC_Power = Total_DC_Power['Total DC Power'].sum()
            Irradiance = yearly_irradiance.loc[yearly_irradiance['Month'] == int(i+1)]
            Irradiance = Irradiance['Irradiance w/m2'].sum()
            T_cell = yearly_irradiance.loc[yearly_irradiance['Month'] == int(i+1)]
            T_cell = float(T_cell['T cell'].sum())/float(24)
            Efficiency = yearly_irradiance.loc[yearly_irradiance['Month'] == int(i+1)]
            Efficiency = float(Efficiency['Efficiency'].sum())/float(24)
            Total_AC_Power = yearly_irradiance.loc[yearly_irradiance['Month'] == int(i+1)]
            Total_AC_Power = Total_AC_Power['Total AC Power'].sum()

            data.loc[months[i+1]] = pd.Series({   'Month':months[i+1],
                                                'Total DC':round(Total_DC_Power,2),
                                                'Irradiance':round(Irradiance,2),
                                                'T cell':round(T_cell,2),
                                                'Efficiency':round(Efficiency,2),
                                                'Total AC':round(Total_AC_Power,2),
                                                })
            
        data.loc['Units'] = pd.Series({   'Month':'',
                                            'Total DC':'[kW]',
                                            'Irradiance':'[W/m2]',
                                            'T cell':'[°C]',
                                            'Efficiency':'[%]',
                                            'Total AC':'[kW]',
                                            })
        
        if self.selling_price_input.get() != '':
            try:
                price = self.selling_price_input.get().replace(',','.')
                price = yearly_kwh*float(price)
            except:
                tkinter.messagebox.showerror(title="Error", message=f"{self.selling_price_input.get()} is not a valid price")
                price = 0  

        else:
            price = 0
        if yearly_kwh > 1000:
            yearly_info = [yearly_kwh/1000,yearly_in_plane_irr,sys_eff,capacity_factor,perfom_ratio,price]
            units = ['[MWh]','[W/m2]','[%]','[%]','[%]','[€]'] 
            if yearly_kwh > 1000:
                yearly_info = [yearly_kwh/1000,yearly_in_plane_irr,sys_eff,capacity_factor,perfom_ratio,price]
                units = ['[GWh]','[W/m2]','[%]','[%]','[%]','[€]'] 
                if yearly_kwh > 1000:
                    yearly_info = [yearly_kwh/1000,yearly_in_plane_irr,sys_eff,capacity_factor,perfom_ratio,price]
                    units = ['[TWh]','[W/m2]','[%]','[%]','[%]','[€]'] 
        else:
            yearly_info = [yearly_kwh,yearly_in_plane_irr,sys_eff,capacity_factor,perfom_ratio,price]
            units = ['[kWh]','[W/m2]','[%]','[%]','[%]','[€]']
        header = ['Total AC Energy','Irradiance','System Efficiency','Capacity Factor','Performance Factor','Revenue']
        yearly_data = pd.DataFrame(columns=['Values','Units'], index = header)
        for i in range(len(yearly_info)):
            yearly_data.loc[header[i]] = pd.Series({ 'Values': round(yearly_info[i],2),
                                                     'Units': units[i]
                                                    })
                    
        monthly_data = tabulate(data, headers=['Total DC','Irradiance','Temperature','Efficiency','Total AC'], tablefmt="fancy_outline", showindex=False)

        monthly_statistics_title = customtkinter.CTkLabel(self.third_frame, text="Monthly Statistics",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        monthly_statistics_title.grid(row=0, column=0, padx=50, pady=(5, 5))


        table_monthly_data = tkinter.StringVar(value = monthly_data) 
        Table_monthly_data = customtkinter.CTkLabel(self.third_frame,  textvariable=table_monthly_data
                                                   ,font=customtkinter.CTkFont(family='Consolas',size=14))
        Table_monthly_data.grid(row=1, column=0, padx=50, pady=(5, 5))

        yearly_statistics_title = customtkinter.CTkLabel(self.third_frame, text="Yearly Statistics",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        yearly_statistics_title.grid(row=2, column=0, padx=75, pady=(10, 5))



        table_yearly_data = tabulate(yearly_data, headers=['Values','Units'], tablefmt="fancy_outline", showindex=True)
        table_yearly_data = tkinter.StringVar(value = table_yearly_data) 
        Table_yearly_data = customtkinter.CTkLabel(self.third_frame,  textvariable=table_yearly_data
                                                   ,font=customtkinter.CTkFont(family='Consolas',size=14))
        Table_yearly_data.grid(row=3, column=0, padx=50, pady=(5, 5))
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']

        
        #yearly_kwh_wp = tkinter.StringVar(value = f"Yearly Energy per Peak: {round(yearly_kwh_wp,2)} [kWh/Wp]") 
        #Yearly_kwh_wp = customtkinter.CTkLabel(self.third_frame,  textvariable=yearly_kwh_wp
        #                                     ,font=customtkinter.CTkFont(size=14))
        #Yearly_kwh_wp.grid(row=2, column=0, padx=50, pady=(self.third_frame.winfo_height()/10, 5), sticky="w")
##
        #yearly_in_plane_irr = tkinter.StringVar(value = f"Yearly in-plane Irradiation: {round(yearly_in_plane_irr,2)} [kWh/m2]") 
        #Yearly_in_plane_irr = customtkinter.CTkLabel(self.third_frame, textvariable=yearly_in_plane_irr
        #                                     ,font=customtkinter.CTkFont(size=14))
        #Yearly_in_plane_irr.grid(row=3, column=0, padx=50, pady=(self.third_frame.winfo_height()/10, 5), sticky="w")
##
        #sys_eff = tkinter.StringVar(value = f"System Efficiency: {round(sys_eff,2)} %") 
        #Sys_eff = customtkinter.CTkLabel(self.third_frame,  textvariable=sys_eff
        #                                     ,font=customtkinter.CTkFont(size=14))
        #Sys_eff.grid(row=4, column=0, padx=50, pady=(self.third_frame.winfo_height()/10, 5), sticky="w")
##
        #capacity_factor = tkinter.StringVar(value = f"Capacity Factor: {round(capacity_factor,2)} %") 
        #Capacity_factor = customtkinter.CTkLabel(self.third_frame, textvariable=capacity_factor
        #                                     ,font=customtkinter.CTkFont(size=14))
        #Capacity_factor.grid(row=5, column=0, padx=50, pady=(self.third_frame.winfo_height()/10, 5), sticky="w")
        #
        #perfom_ratio = tkinter.StringVar(value = f"Performance Ratio: {round(perfom_ratio,2)} %") 
        #Perfom_ratio = customtkinter.CTkLabel(self.third_frame, textvariable=perfom_ratio
        #                                     ,font=customtkinter.CTkFont(size=14))
        #Perfom_ratio.grid(row=6, column=0, padx=50, pady=(self.third_frame.winfo_height()/10, 5), sticky="w")
        
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
        self.fig.autofmt_xdate()

       
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