import tkinter 
import customtkinter as ctk
from pytube import YouTube


def download_video():
    try:
        yt = YouTube(link.get(), on_progress_callback=progress_function)
        stream = yt.streams.get_highest_resolution()
        
        title.configure(text=yt._title)
        title.update()
        finished.configure(text="Downloading...")
        finished.update()
        
        stream.download("videos/")
        print("Video downloaded successfully")
        finished.configure(text="Video downloaded successfully")
    except:
        print("Error while downloading video")
        finished.configure(text="Error while downloading video")

def progress_function(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = (float(abs(bytes_remaining-size)/size))*float(100)
    print(f"{progress:.2f}%")
    progress_text.configure(text=f"{progress:.2f}%")
    progress_text.update()
    
    # update progress bar
    progress_bar.set(progress/100)

# settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# app frame
app = ctk.CTk()
app.geometry("500x300")
app.title("YouTube Downloader")

# UI elements
title = ctk.CTkLabel(app, text="YouTube Downloader", font=("Arial", 20))
title.pack(pady=10)

# Link input
url_var = tkinter.StringVar()
link = ctk.CTkEntry(app,width=350, textvariable=url_var)
link.pack(pady=10)

# Finished message
finished = ctk.CTkLabel(app, text="", font=("Arial", 16))
finished.pack(pady=10)

# progress
progress_text = ctk.CTkLabel(app, text="0%", font=("Arial", 16))
progress_text.pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=10)

# Download button
download = ctk.CTkButton(app, text="Download", command=download_video)
download.pack(pady=10)

# Run the app
app.mainloop()