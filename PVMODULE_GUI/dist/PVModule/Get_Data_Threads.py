#from pvmodule import PVGIS
#from pvmodule import System
from multiprocessing import Process, Queue
import httpimport
with httpimport.github_repo('fabio-r-almeida', 'pvmodule', ref='main'):
    import pvgis
    import system
    import agro_indicators

class Get_Data_Threads():
    
    def __init__(self):  
        self.ac_data = None
        self.dc_data = None
        self.irradiation_data = None
        self.location = None
        self.inverter = None
        self.module = None
        self.yearly_kwh = None
        self.yearly_kwh_wp = None
        self.yearly_in_plane_irr = None
        self.sys_eff = None
        self.capacity_factor = None
        self.perfom_ratio = None

    def get_ac_data(self):
        return self.ac_data
    
    def get_dc_data(self):
        return self.dc_data
    
    def get_irradiation_data(self):
        return self.irradiation_data
    
    def get_location(self):
        return self.location
    
    def get_module(self):
        return self.module
    
    def get_inverter(self):
        return self.inverter
    
    def get_yearly_kwh(self):
        return self.yearly_kwh
    
    def get_yearly_kwh_wp(self):
        return self.yearly_kwh_wp
    
    def get_yearly_in_plane_irr(self):
        return self.yearly_in_plane_irr
    
    def get_sys_eff(self):
        return self.sys_eff
    
    def get_capacity_factor(self):
        return self.capacity_factor
    
    def get_perfom_ratio(self):
        return self.perfom_ratio
    


    def bi_worker(self, queue, location, module, inverter, azimuth):
        _, data , _ = pvgis.PVGIS().retrieve_all_year_bifacial(location, azimuth = azimuth)
        dc = system.System().dc_production(module, data, "Global irradiance on a fixed plane", "2m Air Temperature", "10m Wind speed")
        ac = system.System().ac_production(dc, inverter, module)
        self.ac_data = ac
        self.dc_data = dc
        self.irradiation_data = data
        self.location = location
        self.inverter = inverter
        self.module = module
        self.yearly_kwh, self.yearly_kwh_wp, self.yearly_in_plane_irr, self.sys_eff, self.capacity_factor, self.perfom_ratio = system.System().Yearly_Stats(ac, module)
        queue.put([ac,self.yearly_kwh, self.yearly_kwh_wp, self.yearly_in_plane_irr, self.sys_eff, self.capacity_factor, self.perfom_ratio])
        
    def bi_PVMODULE_GET_DATA_THREAD_PER_MONTH(self,QUEUE, location, module, inverter, azimuth):
        queue = Queue()
        p1 = Process(target=self.worker, args=(queue, location, module, inverter, azimuth))
        p1.start()  
        QUEUE.put(queue.get())   
        return queue.get()
    
    def worker(self, queue, location, module, inverter, azimuth, panel_tilt):
        _, data , _ = pvgis.PVGIS().retrieve_all_year(location, azimuth = azimuth, panel_tilt=panel_tilt)
        dc = system.System().dc_production(module, data, "Global irradiance on a fixed plane", "2m Air Temperature", "10m Wind speed")
        ac = system.System().ac_production(dc, inverter, module)
        self.ac_data = ac
        self.dc_data = dc
        self.irradiation_data = data
        self.location = location
        self.inverter = inverter
        self.module = module
        self.yearly_kwh, self.yearly_kwh_wp, self.yearly_in_plane_irr, self.sys_eff, self.capacity_factor, self.perfom_ratio = system.System().Yearly_Stats(ac, module)
        queue.put([ac,self.yearly_kwh, self.yearly_kwh_wp, self.yearly_in_plane_irr, self.sys_eff, self.capacity_factor, self.perfom_ratio])
        
    def PVMODULE_GET_DATA_THREAD_PER_MONTH(self,QUEUE, location, module, inverter, azimuth, panel_tilt):
        queue = Queue()
        p1 = Process(target=self.worker, args=(queue, location, module, inverter, azimuth, panel_tilt))
        p1.start()  
        QUEUE.put(queue.get())   
        return queue.get()
    
    def agro_worker(self, queue, location):
        _, data , _ = pvgis.PVGIS().retrieve_all_year(location, azimuth = 0, panel_tilt=0)
        data, agro_data = agro_indicators.Agro_Indicators().PPFD_DLI(location, data)
        queue.put([data, agro_data])
        
    def PVMODULE_GET_PPDF_DLI(self,QUEUE, location):
        queue = Queue()
        p1 = Process(target=self.agro_worker, args=(queue, location))
        p1.start()  
        QUEUE.put(queue.get())   
        return queue.get()
    


