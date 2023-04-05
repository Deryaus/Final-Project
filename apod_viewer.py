"""--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------




--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------"""

from tkinter import *
from tkinter import ttk
import inspect, os, apod_desktop, image_lib
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date


# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
root = Tk()
#root.geometry('800x600')
root.minsize(800, 600)
root.maxsize(1000, 800)
root.iconbitmap(os.path.join(script_dir, 'nasa_logo.ico'))
root.columnconfigure(0, weight=60)
root.columnconfigure(1, weight=40)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.title('Astronomy Picture Of The Day')

# Add Frames to the window.
# Top frame for picture
top_frm = ttk.Frame(root)
top_frm.grid(row=0, column=0, columnspan=2, pady=10, sticky=NSEW)
top_frm.columnconfigure(0, weight=1) 
top_frm.rowconfigure(0, weight=1)


# Middle frame for Image description
middle_frm = ttk.Frame(root)
middle_frm.grid(row=1,column=0, columnspan=2, padx=10, pady=10, sticky=NSEW)
middle_frm.columnconfigure(0,weight=50) 
middle_frm.rowconfigure(1,weight=50) 


# Bottom left frame for selecting title and setting desktop
btm_left_frm = ttk.LabelFrame(root, text="View Cached Image")
btm_left_frm.grid(row=2, column=0, padx=10, pady=5, sticky=SW)
btm_left_frm.columnconfigure(0,weight=50)
btm_left_frm.rowconfigure(2, weight=50)
# Bottom Right frame for selecting Date
btm_right_frm = ttk.LabelFrame(root, text="Get More Images")
btm_right_frm.grid(row=2, column=1, padx=10, pady=5, sticky=SW)
btm_right_frm.columnconfigure(1, weight=50)
btm_right_frm.rowconfigure(2, weight=50)
# Default Image Upon opening GUI
bckgrd_image = Image.open(os.path.join(script_dir,"nasa.png")).resize((550,350))
nasa_logo = ImageTk.PhotoImage(bckgrd_image)
lbl_logo = ttk.Label(top_frm, image=nasa_logo, anchor=CENTER)
lbl_logo.grid(row=0, column=0, columnspan=2, padx=(100,100), pady=10,)


# Add widgets to bottom left frame.
lbl_cache = ttk.Label(btm_left_frm, text='Select an Image:')
lbl_cache.grid(row=0, column=0, padx=5, pady=10, sticky=W)
# Get list of titles from DB and pass to combobox
cache_list = apod_desktop.get_all_apod_titles()
cbox_title_sel = ttk.Combobox(btm_left_frm, width=30, values=cache_list, state='readonly')
cbox_title_sel.set('Select An Image')
cbox_title_sel.grid(row=0, column=1, padx=5, pady=10, sticky=W)
# Create set as desktop button
btn_set_dsktp = ttk.Button(btm_left_frm, text='Set As Desktop', command=image_lib.set_desktop_background_image, state=DISABLED) 
btn_set_dsktp.grid(row=0, column=3, padx=5, pady=10, sticky=W)


# Add Widget to be filled in for middle frame
lbl_desc = ttk.Label(middle_frm, text='', anchor=CENTER, wraplength=750)
lbl_desc.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=NSEW)
lbl_desc.grid_propagate(0)
# Create title Selection event
#TODO finish event Handling
def title_sel(event):
    if cbox_title_sel.current() != -1:
        btn_set_dsktp.config(state=NORMAL)
    #TODO once title is selected Display the image
    image_title = cbox_title_sel.get()
    pass

# Bind button state to combobox
cbox_title_sel.bind("<<ComboboxSelected>>", title_sel)


# Creat Download Image Event handle
#TODO finish button handling
def download_image():
    apod_date = cal.get()
    apod_id = apod_desktop.add_apod_to_cache(apod_date)
    apod_info = apod_desktop.get_apod_info(apod_id)
    # Populate middle frame with explanation
    lbl_desc['text'] = apod_info['explanation']
    


# Add Widgets to the bottom right frame
START_DATE = date.fromisoformat('1995-06-16')
today = date.today()
lbl_sel_date = ttk.Label(btm_right_frm, text='Select a Date:')
lbl_sel_date.grid(row=0, column=0, padx=5, pady=10, sticky=E)
cal = DateEntry(btm_right_frm, maxdate=today, mindate=START_DATE, state='readonly', date_pattern='yyyy-mm-dd') 
cal.grid(row=0, column=2,padx=5, pady=10, sticky=E)
btn_dwnld_img = ttk.Button(btm_right_frm, text="Download Image", command=download_image)
btn_dwnld_img.grid(row=0, column=3, padx=5, pady=10, sticky=E)



root.mainloop()