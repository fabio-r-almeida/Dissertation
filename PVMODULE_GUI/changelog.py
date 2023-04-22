
\033[1m Added \033[0m
- Added new *Graph* class.
- Multithreading yearly horizontal and vertical data acquisition with 
  - *PVGIS().retrieve_all_year_bifacial()*
  - *PVGIS().retrieve_all_year()*
\033[1m Fixed \033[0m
- Improved inverter auto-selection.
- Added error exception in both *Inverter* and *PVGIS* class.
\033[1m Removed \033[0m
- Irradiance class will soon be removed due to incorrect irradiance estimations.
  - This issue is believed to be cause due to the incorrect shadow calculation of the module.
