from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": [], 
    "excludes": [],
    "includes": ["matplotlib.backends.backend_tkagg", 'matplotlib.backends.backend_qt4agg'] # <-- Include easy_gui
}

executables = [Executable('graphic.py')]

setup(name='Graphic',
      version='1.0',
      description='Graphic',
      options = {"build_exe": build_exe_options},
      executables=executables)