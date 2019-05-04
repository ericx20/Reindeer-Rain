import cx_Freeze
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable("reindeerRain.py")]

cx_Freeze.setup(
    name = "Reindeer Rain",
    options = {
        "build_exe": {
            "packages":["pygame"],
            "include_files":[
                "background.png", "heart.png",
                "heart.wav", "hit.wav",
                "leaderboard.txt", "music.ogg",
                "player.png", "PressStart2P.ttf",
                "reindeer.png", "shield.png",
                "shield.wav",
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
            ]
        }
    },
    executables = executables,
    version = '1.0.0'
    )
