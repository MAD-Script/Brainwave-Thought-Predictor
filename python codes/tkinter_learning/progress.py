from tkinter import ttk
import customtkinter as ctk
import datetime as dt
import time


# settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")
window = ctk.CTk()


# screen attributes
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

win_geo_x = screen_width*0.9
win_geo_y = screen_height*0.9

window_x = int(screen_width/2 - win_geo_x/2)
window_y = int(screen_height/2 - win_geo_y/2)


# window frame
window.geometry(f"{int(win_geo_x)}x{int(win_geo_y)}+{window_x}+{window_y}")
window.title("Progress Bar")
window.minsize(int(win_geo_x/3), int(win_geo_y/3))

window.overrideredirect(True)
#### size grip not visible
# grip_style = ttk.Style()
# grip_style.configure("TSizegrip", background="#1a1a1a")
# grip_style.configure("TSizegrip", foreground="#4a4d50")
# grip = ttk.Sizegrip(window,style="TSizegrip")
# # window.resizable(True, True)
# grip.place(relx=1.0, rely=1.0, anchor="se")



# window attributes
# window.attributes("-topmost", True)

# security event
window.bind("<Escape>", lambda event: window.quit())

# UI elements
title = ctk.CTkLabel(window, text="", 
                     font=("Arial", 250), 
                     anchor="center")
title.pack(expand=True, fill='both')

# progrss frame
progress_frame = ttk.Frame(window)
progress_frame.pack(fill='both')

# progress bar
progress_bar = ttk.Progressbar(progress_frame,
                               orient="horizontal",
                               mode="determinate",
                               maximum=60,
                               length=win_geo_x,
                               )
progress_bar.grid(row=0, 
                  column=0, 
                  sticky="ew")

# blank frame
blank = ttk.Frame(progress_frame)
blank.grid(row=0, column=0, sticky="nsew")

def show_word(word):
        progress_bar.tkraise()
        progress_bar["value"] = 0
        title.configure(text=word)
        title.configure(font=("Arial", 100))
        title.pack(expand=True, fill='both')
        progress_step()
    
    
def progress_step():
    progress_bar.tkraise()
    print(progress_bar['value'])
    if progress_bar['value'] < 59:
        progress_bar.step()
        window.after(100, progress_step)
    else:
        progress_bar.stop()
        # progress_bar.lower()
        # progress_bar.pack_forget()
        next_screen()
        # window.after(1000, window.quit)

def next_screen():
        progress_bar["value"] = 60
        progress_bar.lower()

        title.configure(text="Ready for next word? ")
        title.configure(font=("Arial", 100))
        
        window.bind("<Key>", lambda event: wait_screen() if event.char == "y" else exit_screen()) 
        
def exit_screen():
        progress_bar["value"] = 60
        progress_bar.lower()

        title.configure(text="Thank you ! closing in 3 seconds ")
        title.configure(font=("Arial", 100))
        
        window.after(3000, window.quit())

def start_program():
        title.configure(text="Ready to start? ")
        title.configure(font=("Arial", 100))
        window.bind("<Key>", lambda event: wait_screen() if event.char == "y" else exit_screen())        

def wait_screen():
        for i in range(1,4):
                title.configure(text=i)
                title.update_idletasks()
                time.sleep(1)
        window.after(100,show_word("Hello"))
        
start_program()
window.mainloop()