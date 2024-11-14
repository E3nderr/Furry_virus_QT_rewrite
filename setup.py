from cx_Freeze import setup, Executable
import os

# Specify the files or folders to include
build_exe_options = {
    "packages": [],
    "include_files": [("assets", "assets")]  # Ensure assets folder is included
}

# Define the base for a Windows GUI application
base = None
if os.name == 'nt':
    base = 'Win32GUI'

setup(
    name="furry_virus",
    version="1.0",
    description=f"""
                Recreation of a popular meme gif\n\n
                I coded this as a fun side project because a friend wanted me to code a working recreation of the "wypher furry virus" meme image.\n\n
                This code does NOT harm your computer in any way, except maybe crashing python on weak hardware lol.\n
                If you plan on trying to continue or use my shitty code, my condolences... Pwease gib credit tho owo\n\n
                I tried building the python project into an exe-file but Tkinter seems to f*ck with cxfreeze and opens thousands\n
                of instances of the app when running the resulting exe file. If you figure out how to build the project into an exe somehow, congrats.\n\n
                Credit to Koiwypher for the images used, all rights remain with the original artist!
                """,
    options={"build_exe": build_exe_options},
    executables=[Executable("furry_virus_QT_debug.py", base=base)]
)