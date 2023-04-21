import customtkinter
import tkintermapview
from Loading import *
#from pvmodule import Location
import httpimport
with httpimport.github_repo('fabio-r-almeida', 'pvmodule', ref='main'):
    import location as LOCATION


class Map(customtkinter.CTk):
    def __init__(self):
        self.map_window_frame = None

    def pick_on_map(self):
        if self.map_window_frame is None or not self.map_window_frame.winfo_exists():

            self.map_window_frame = customtkinter.CTkToplevel(self)                                                                                  
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

                self.pvmodule_location = LOCATION.Location().set_location(latitude=latitude, longitude=longitude)
                self.tabview_information_pvgis_info.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew") 
                                                                                                 
                self.Latitude_entry_var.set("Latitude: " + str(latitude))                                                                  
                self.Longitude_entry_var.set("Longitude: "+ str(longitude))                                                                  
                self.map_window_frame.destroy()                                                                                    
                loading.destroy()                                                                

            map_widget.add_left_click_map_command(left_click_event) 
        else:
            self.map_window_frame.focus()
