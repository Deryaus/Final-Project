"""--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------
COMP 593 - Final Project

Description: 
  Create a graphical user interface to interace with Nasa's Astronomy Picture
  of The Day (APOD) from a specified date and sets the image as the desktop background
  
Usage:
  python apod_viewer.py 

--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------"""
import inspect, os, apod_desktop, image_lib, ctypes, sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date

sys.stderr = open(os.devnull, 'w')

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# Create the main window
root = Tk()
root.minsize(800, 600)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Final-Project.apod_viewer')
root.withdraw()
root.iconbitmap(os.path.join(script_dir, 'nasa_logo_icon.ico'))
root.deiconify()

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=60)
root.rowconfigure(1, weight=20)
root.rowconfigure(2, weight=20)
root.title('Astronomy Picture Of The Day')

# Top frame for images
top_frm = ttk.Frame(root)
top_frm.grid(row=0, column=0, columnspan=2, pady=10, sticky=NSEW)
top_frm.columnconfigure(0, weight=1) 
top_frm.rowconfigure(0, weight=1)

# Middle frame for Image description
middle_frm = ttk.Frame(root)
middle_frm.grid(row=1,column=0, columnspan=2, padx=10, pady=10, sticky=NSEW)
middle_frm.columnconfigure(0,weight=1) 
middle_frm.rowconfigure(1,weight=1) 

# Bottom left frame for selecting title and setting desktop
btm_left_frm = ttk.LabelFrame(root, text="View Cached Image")
btm_left_frm.grid(row=2, column=0, padx=10, pady=5, sticky=SW)
btm_left_frm.columnconfigure(0,weight=1)
btm_left_frm.rowconfigure(2, weight=1)

# Bottom Right frame for selecting Date
btm_right_frm = ttk.LabelFrame(root, text="Get More Images")
btm_right_frm.grid(row=2, column=1, padx=5, pady=5, sticky=SE)
btm_right_frm.columnconfigure(1, weight=1)
btm_right_frm.rowconfigure(2, weight=1)

# Default Image Upon opening GUI
bckgrd_image = Image.open(os.path.join(script_dir,"NASA_logo.png")).resize((600,400))
nasa_logo = ImageTk.PhotoImage(bckgrd_image, Image.ANTIALIAS)
lbl_image = ttk.Label(top_frm, image=nasa_logo, anchor=CENTER)
lbl_image.grid(row=0, column=0, columnspan=2, padx=(10,10), pady=10,)

# Add widgets to bottom left frame.
lbl_cache = ttk.Label(btm_left_frm, text='Select an Image:')
lbl_cache.grid(row=0, column=0, padx=5, pady=10, sticky=W)

# Get list of titles from DB and pass to combobox
global cache_list
cache_list = sorted(apod_desktop.get_all_apod_titles())
cbox_title_sel = ttk.Combobox(btm_left_frm, width=40, values=cache_list, state='readonly')
cbox_title_sel.set('Select An Image')
cbox_title_sel.grid(row=0, column=1, padx=(5,0), pady=10, sticky=W)

# Handle button event
def handle_set_desktop():
    apod_info = apod_desktop.get_apod_path_and_expl(cbox_title_sel.get())
    image_lib.set_desktop_background_image(apod_info['file_path'])
    
# Create set as desktop button
btn_set_dsktp = ttk.Button(btm_left_frm, text='Set As Desktop', command=handle_set_desktop, state=DISABLED) 
btn_set_dsktp.grid(row=0, column=3, padx=5, pady=10, sticky=W)

# Add Widget to middle frame
lbl_desc = ttk.Label(middle_frm, text='Discover the cosmos! Each day a different image or photograph of our fascinating universe is \
featured, along with a brief explanation written by a professional astronomer.', anchor=CENTER, wraplength=750)
lbl_desc.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=NSEW)

# Handle title selection event
def title_sel(event):
    # Change min size of window
    root.minsize(800,900)
    # Enable set as desktop button upon selection
    if cbox_title_sel.current() != -1:
        btn_set_dsktp.config(state=NORMAL)
    # Retrieve Explanation and file path
    apod_info = apod_desktop.get_apod_path_and_expl(cbox_title_sel.get())
    lbl_desc['text'] = apod_info['explanation']
    # Open new Image
    new_image = Image.open(apod_info['file_path'])
    # Find out the Image Size
    image_size = new_image.size
    # Scale the image to an appropriate size
    width, height = image_lib.scale_image(image_size)
    resized_img = new_image.resize((width, height), Image.ANTIALIAS)
    new_tk_image = ImageTk.PhotoImage(resized_img)
    # Display new image in window
    lbl_image['image'] = new_tk_image
    lbl_image.image 
    
# Bind title select to combobox
cbox_title_sel.bind("<<ComboboxSelected>>", title_sel)

# Create Download Image Event handle
def download_image():
    # Change the min size of the window
    root.minsize(800,900)
    # Enable Set desktop button upon donwloading image
    btn_set_dsktp.config(state=NORMAL)
    # Retrieve Date from Calender
    apod_date = cal.get()
    # add apod to cache
    apod_id = apod_desktop.add_apod_to_cache(apod_date)
    apod_info = apod_desktop.get_apod_info(apod_id)
    if apod_info is None:
        err_msg = 'Unable to retrieve data for this date'
        messagebox.showinfo(title='Error', message=err_msg, icon='error')  
    else:
        # Populate frames with new information
        lbl_desc['text'] = apod_info['explanation']
        cbox_title_sel.set(apod_info['title'])
        # Add new title to combobox
        new_title = cbox_title_sel.get()
        if new_title not in cbox_title_sel['values']:
            cache_list.append(new_title)
            cbox_title_sel['values'] = sorted(cache_list)
        # Open new Image
        new_image = Image.open(apod_info['file_path'])   
        # Find out the Image Size
        image_size = new_image.size
        # Scale the image to an appropriate size
        width, height = image_lib.scale_image(image_size)
        resized_img = new_image.resize((width, height), Image.ANTIALIAS)
        # Display new Image in window
        global new_tk_image
        new_tk_image = ImageTk.PhotoImage(resized_img)
        lbl_image['image'] = new_tk_image
        lbl_image.image
        
# Add Widgets to the bottom right frame
START_DATE = date.fromisoformat('1995-06-16')
today = date.today()
lbl_sel_date = ttk.Label(btm_right_frm, text='Select a Date:')
lbl_sel_date.grid(row=0, column=0, padx=5, pady=10, sticky=SE)
cal = DateEntry(btm_right_frm, maxdate=today, mindate=START_DATE, state='readonly', date_pattern='yyyy-mm-dd') 
cal.grid(row=0, column=2,padx=5, pady=10, sticky=E)
# Create download image button
btn_dwnld_img = ttk.Button(btm_right_frm, text="Download Image", command=download_image)
btn_dwnld_img.grid(row=0, column=3, padx=5, pady=10, sticky=SE)

# loop until window closes
root.mainloop()