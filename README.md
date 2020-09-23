<p align="center"><img src="https://media.giphy.com/media/PY0vCb69zRbH6hsIgh/giphy.gif" width="200"></p>

# ProdApp

[![PyPI version](https://badge.fury.io/py/prodapp.svg)](https://badge.fury.io/py/prodapp)

[![Watch the video](https://i.imgur.com/0pIxYK9.png)](https://youtu.be/PY1nIAvu0vc)

**Demo** - click above

## Features

### Self-scoring

 - **+5**: **poor productivity** -- didn't get much done
 - **+10**: **fair productivity** -- normal work
 - **+15**: **excellent productivity** -- laser-focused shredding of workload

### Countdown timer

 - Bleeps at 0 -> give youreslf a score
 - Change values with click + typing
 - Pausable
 - Defaults to 10 minute intervals, configurable


### Saved progress: images

Swap between daily progress pics with a button press for easy comparison

<img src="https://media.giphy.com/media/ilHKB0sNZqpKCXdDkg/giphy.gif" width="550">

### Saved progress: csv

Recover/edit data for reference or further processing

<img src="https://media.giphy.com/media/JnIuLJIml94oB6XEFS/giphy.gif" width="500">

## Installation

`pip install prodapp`

## Usage

### Command Line

```
cd path/to/prodapp
python app.py
```

Open http://127.0.0.1:8050/ in browser

### Configs

Edit `prodapp/configs.ini`:

 1. `t_max`: countdown startup/reset value, in seconds (default 600); this is how often you score yourself
 2. `t_min`: where bleeps happen (default 0)
 3. `bleeps`: number of times to replay the alarm sound (default 2)
 
### Misc

 1. **Edit data**: open `data/<current_date>.csv`, edit, save. Make sure the app is closed in the meantime.
 2. **Edit images**: can't. Must make new save.
 3. **Save data/image**: add productivity (+5/10/15), saves automatically.
 4. **Change timer reset value**: either via configs (requires app restart), or: first click reset, then change time value (e.g. to 12:00); that'll be the new reset.


### Double-click

Automate command-line steps; steps are to use with Anaconda, but can tailor to regular Python:

 1. Windows -> Search -> "Windows PowerShell" -> Right-click -> Open file location
 2. Copy "Windows PowerShell" shortcut, paste to Desktop (or another folder), rename to "prodapp" (or anything else)
 3. Right-click the pasted shortcut -> Properties -> Shortcut -> Target -> Paste step 4
 4. %windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'D:\Anaconda\shell\condabin\conda-hook.ps1' ; %condaProdapp%
 5. Windows -> Search -> "Edit system environment variables" -> Environment Variables... -> System variables -> New...
 6. Variable name: condaProdapp
 7. Variable value: conda activate dash-env; cd 'D:\Anaconda\envs\dash-env\Lib\site-packages\prodapp'; python app.py

That's it. Double-click the shortcut, and `prodapp` will start. Open http://127.0.0.1:8050/ in browser manually. Can skip `conda activate` if installing `prodapp` in base environment ("no environment").

## To-do

The app is "finished"; I don't intend to do much further, but I welcome contributors. A list that I might sometime work on, or invite others to:

  - [ ] `prodapp.exe`
  - [ ] To-do list under the red orb ([example](https://youtu.be/GwgSWPxLYlM); this is original ProdApp written in electron.js)
  - [ ] Edit values for _other_ (non-current) hours straight from application, including subtracting values
  - [ ] Make the orb functional; change color, size, rotation rate depending on total "productivity" for the day
  
