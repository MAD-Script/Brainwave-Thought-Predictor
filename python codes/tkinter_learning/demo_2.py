import tkinter as tkin
import customtkinter as custkin

def convert():
    
    miles= entry_int.get()
    km = round(float(miles) * 1.609, 2)
    output_string.set(str(km))

# # settings
# custkin.set_appearance_mode("System")
# custkin.set_default_color_theme("blue")

# app frame
window = custkin.CTk()
window.geometry("500x300")

title_label = custkin.CTkLabel(master= window, 
                               text="This is a demo", 
                               font=("Arial", 50))
title_label.pack(pady=10)

# input field
input_frame = custkin.CTkFrame(master=window)

entry_int = custkin.IntVar()
entry = custkin.CTkEntry(master=input_frame,
                        width=150, 
                        textvariable=entry_int)

button = custkin.CTkButton(master=input_frame, 
                           text="Submit", 
                           width= 5, 
                           command=convert)

entry.pack(side="left", padx=10)
button.pack(side="left")
input_frame.pack(pady=10)

# output 
output_string = custkin.StringVar()
output_label = custkin.CTkLabel(master=window,
                                text="Output",
                                font=("Arial", 30),
                                textvariable=output_string)
output_label.pack(pady=10)

# run
window.mainloop()