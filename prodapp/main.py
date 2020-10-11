# -*- coding: utf-8 -*-
import os
cfgpath = '../config.ini' if os.path.isfile('../config.ini') else 'config.ini'

run = True
port_url = "http://127.0.0.1:8050/"

with open(cfgpath, 'r') as f:
    txt = [line.strip(' \n') for line in f.read().split('\n')]
    for line in txt:
        # if always_new=1, continue - else, open browser tab and exit script
        if line.startswith('always_new') and line.split('=')[-1] == '0':
            import psutil
            if sum(p.name() == 'prodapp.exe' for p in psutil.process_iter()) > 1:
                for line in txt:
                    if line.startswith('port_url'):
                        port_url = line.split('=')[-1]
                if port_url != '':
                    import webbrowser
                    webbrowser.open(port_url)
                run = False
            break
if run:
    filepath = 'app.py'
    globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals)
