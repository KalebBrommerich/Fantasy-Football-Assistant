#Using Python 3.12.2 64-bit
#Found a decent web framework called Flask  pip install Flask
#https://flask.palletsprojects.com/en/3.0.x/quickstart/
#Built in Python GUI seems kinda bad according to internet
#but thats too complex for now

import Webscraper
import tkinter as tk
#When GUI start
class GUI:
    def __init__(self) -> None:
        root = tk.Tk()
        root.title("Fantasy Football assistant")
        root.attributes("-fullscreen",True)
        label = tk.Label(root, text="Fantasy Football Assistant")
        label.pack(fill="none")
        quitBtn = tk.Button(root,text="Quit", command=exit)
        quitBtn.pack(anchor="ne",padx=10, pady=10)
        root.mainloop()
        pass

temp = GUI
GUI.__init__(temp)
    