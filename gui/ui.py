'''
module for handing a simple GUI for this thing

follow tutorials here:
https://realpython.com/pysimplegui-python/

and here:
https://realpython.com/python-gui-with-wxpython/
'''

# imports
import os.path
import PySimpleGUI as sg

# layout
layout = [
    [sg.Text("Hello from PySimpleGUI")], 
    [sg.Button('OK')]
]

# create window
window = sg.Window('Demo', layout)

# event loop
while True:
    event, values = window.read()
    # end process if uses closes window
    # or presses the 'OK' button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()