import customtkinter
from Loading import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from numpy import trapz as calculate_area_under_curve


class PPFD_Plot():
    def __init__(self):
        pass


    def plot_ppfd(self, yearly_irradiance):

        #months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
        #self.change_month_label = customtkinter.CTkLabel(self.fourth_frame, text="Month:")                                           
        #self.change_month_label.grid(row = 0 , column=6, padx=10, pady=(10, 10))
        #self.change_month = customtkinter.CTkOptionMenu(self.fourth_frame, dynamic_resizing=False,values=months, command= self.ppfd_change_plotting_month)
        #self.change_month.grid(row=0, column=7, padx=10, pady=(10, 10))
        #self.change_month.set('January')
        self.fig_ppfd = Figure(facecolor='#242424')  
        self.ax_ppfd = self.fig_ppfd.add_subplot(111)
        self.fig_ppfd.tight_layout()
        
        self.ax_ppfd.spines['bottom'].set_color('#144870')
        self.ax_ppfd.spines['top'].set_color('#144870') 
        self.ax_ppfd.spines['right'].set_color('#144870')
        self.ax_ppfd.spines['left'].set_color('#144870')
        self.ax_ppfd.title.set_color('#3b8ed0')
        self.ax_ppfd.yaxis.label.set_color('#3b8ed0')
        self.ax_ppfd.xaxis.label.set_color('#3b8ed0')
        self.ax_ppfd.tick_params(axis='x', colors='#3b8ed0')
        self.ax_ppfd.tick_params(axis='y', colors='#3b8ed0')
        self.ax_ppfd.set_facecolor("#2b2b2b")

        if customtkinter.get_appearance_mode() == "Dark":
            self.ax_ppfd.set_facecolor("#2b2b2b")
            self.fig_ppfd.set_facecolor("#242424")
        else:
            self.ax_ppfd.set_facecolor("#dbdbdb")
            self.fig_ppfd.set_facecolor("#ebebeb")
        
        for i in range(1, 13):
            data = yearly_irradiance.loc[yearly_irradiance['month'] == i]
            self.line1_ppfd, = self.ax_ppfd.plot(data.index, data['Total Irradiance'], color='red', marker='v',linewidth='0.5',linestyle = 'dotted', markersize=2)
        self.line1_ppfd.axes.set_title("Photosynthetic Photon Flux Density")

       
        if customtkinter.get_appearance_mode() == "Dark":
            self.ax_ppfd.legend(['Monthly Average PPFD'],frameon=False, labelcolor="white")

        else:
            self.ax_ppfd.legend(['Monthly Average PPFD'],frameon=False, labelcolor="black")

        self.canvas_ppfd = FigureCanvasTkAgg(self.fig_ppfd,master=self.fourth_frame)
        self.canvas_ppfd.get_tk_widget().grid(row=2, columnspan=5, padx=5, pady=5)
        self.fourth_frame.grid(row=0, column=1, padx=5, pady=5)


    #def change_plotting_month(self, event):
    #    data_irr = pd.DataFrame()
    #    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
    #    data_irr = self.yearly_kwah.loc[self.yearly_kwah['Month'] == int(months.index(event))+1]
#
    #    self.line1.set_xdata(data_irr.index)
    #    self.line1.set_ydata(data_irr['Total Irradiance'])
#
    #    self.line2.set_xdata(data_irr.index)
    #    self.line2.set_ydata(data_irr['Irradiance w/m2'])
#
#
    #    self.line1_dc.set_xdata(data_irr.index)
    #    self.line1_dc.set_ydata(data_irr['Total DC Power'])
#
    #    self.line2_dc.set_xdata(data_irr.index)
    #    self.line2_dc.set_ydata(data_irr['Total AC Power'])
#
#
    #    self.ax.set_xlim(data_irr.index.min(),data_irr.index.max())
    #    self.ax.set_ylim(data_irr['Total Irradiance'].min(),data_irr['Total Irradiance'].max() + data_irr['Total Irradiance'].max()*0.1)
#
    #    self.bx.set_xlim(data_irr.index.min(),data_irr.index.max())
    #    self.bx.set_ylim(data_irr['Total DC Power'].min(),data_irr['Total DC Power'].max()+ data_irr['Total DC Power'].max()*0.1)
    #    if customtkinter.get_appearance_mode() == "Dark":
    #        self.ax.legend(['Global Irradiance','Irradiance W/m2'],frameon=False, labelcolor="white")
    #        self.bx.legend(['Total DC Power (kW)','Total AC Power (kW)'],frameon=False, labelcolor="white")
#
    #    else:
    #        self.ax.legend(['Global Irradiance','Irradiance W/m2'],frameon=False, labelcolor="black")
    #        self.bx.legend(['Total DC Power (kW)','Total AC Power (kW)'],frameon=False, labelcolor="black")
    #        self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=45)
    #        self.bx.set_xticklabels(self.bx.get_xticklabels(), rotation=45)
#
#
    #    total_irradiance = calculate_area_under_curve(y=data_irr['Total AC Power'],dx=24/len(data_irr.index))
    #    print(f"Find print 1: Total Power AC: {total_irradiance}")
    #    self.canvas.draw()