import sys
from cx_Freeze import setup, Executable

# Include tkinter as a module (needed for GUI applications)
build_exe_options = {"packages": ["tkinter"], "include_files": [], "include_msvcr": True}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" for a GUI application

executables = [Executable("gamessinput.py", base=base)]

setup(
    name="ComputationalChemistryInputBuilder",
    version="1.0",
    description="Python GUI Application for Computational Chemistry Input Building",
    options={"build_exe": build_exe_options},
    executables=executables
)
