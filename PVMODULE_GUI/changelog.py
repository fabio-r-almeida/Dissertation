### [0.0.66] to [0.0.130] - 2023-03-20
### Added
- Added new *Graph* class.
- Multithreading yearly horizontal and vertical data acquisition with 
  - *PVGIS().retrieve_all_year_bifacial()*
  - *PVGIS().retrieve_all_year()*
### Fixed
- Improved inverter auto-selection.
- Added error exception in both *Inverter* and *PVGIS* class.
### Removed
- Irradiance class will soon be removed due to incorrect irradiance estimations.
  - This issue is believed to be cause due to the incorrect shadow calculation of the module.
