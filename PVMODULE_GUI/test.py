import httpimport
with httpimport.github_repo('fabio-r-almeida', 'pvmodule', ref='main'):
    import pvmodule_version 
    print(pvmodule_version.__version__)