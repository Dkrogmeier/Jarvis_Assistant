import os
import subprocess as sp

paths = {
    # 'notepad': % windir %\system32\notepad.exe
    'discord': "C:\Users\Dakota\AppData\Local\Discord\app-1.0.9005\Discord.exe"
    # 'calculator':
    # 'league':
    # 'chrome':
    # 'vs code':
}


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_discord():
    os.startfile(paths['discord'])


def open_cmd():
    os.system('start cmd')
