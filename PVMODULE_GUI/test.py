import httpimport
with httpimport.github_repo('fabio-r-almeida', 'pvmodule', ref='main'):
    import module
    import inverter

module.Modules().list_modules()
print(inverter.Inverters().list_inverters())





