"""--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------




--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------"""

from tkinter import *
from tkinter import ttk
import inspect
import os
import apod_desktop
from PIL import Image, ImageTk


# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
root = Tk()
root.geometry('600x400')

root.title('Astronomy Picture Of The Day')
root.iconbitmap(r'C:\temp\favicon.ico')
bckgrd_image = Image.open(r'C:\temp\images\19.jpg')
bckgrd_image = bckgrd_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
bphoto = ImageTk.PhotoImage(bckgrd_image)
label = Label(root, image=bphoto, width=600, height=400)
button = Button(root, text='something somethin')
button.place(x=350,y=350,)

label.pack()
root.mainloop()