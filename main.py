# -----------------Importing essential Libraries & Modules--------------
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from pytube import YouTube
from threading import *

# -------------------------------PyTube Setup----------------------------
# Total size container
file_size_high = 0
file_size_low = 0

# Download Progress Display for Video
def progress_high(stream=None, chunk=None, bytes_remaining=None):
    downloaded_data = (file_size_high - bytes_remaining)
    percentage = float((downloaded_data / file_size_high) * 100)
    title_vid.config(text=stream.title)
    title_vid.pack()
    display_per.config(text="{:00.0f} % Downloaded".format(percentage))
    display_per.pack()

# Download Progress Display for Audio
def progress_low(stream=None, chunk=None, bytes_remaining=None):
    downloaded_data = (file_size_low - bytes_remaining)
    percentage = float((downloaded_data / file_size_low) * 100)
    title_vid.config(text=stream.title)
    title_vid.pack()
    display_per.config(text="{:00.0f} % Downloaded".format(percentage))
    display_per.pack()

# Complete Download for Video
def down_complete_high(stream=None, filepath=None):
    print("Download Completed")
    bttn_high.config(text="Download Another Video")
    bttn_high.config(state=NORMAL)
    showinfo("Notification", "Video Downloaded Successfully")
    enter_url.delete(0,"end")
    display_per.pack_forget()
    title_vid.pack_forget()

# Complete Download for Audio
def down_complete_low(stream=None, filepath=None):
    print("Download Complete")
    bttn_low.config(text="Download Another Audio")
    bttn_low.config(state=NORMAL)
    showinfo("Notification", "Audio Downloaded Successfully")
    enter_url.delete(0,"end")
    display_per.pack_forget()
    title_vid.pack_forget()

# -----------------------Thread target for Video----------------
def startDownloadHigh(url):
    global file_size_high
    path_to_save = askdirectory()
    if path_to_save is None:
        return

    try:
        ob = YouTube(url)

        strm_high = ob.streams.get_highest_resolution()

        ob.register_on_complete_callback(down_complete_high)
        ob.register_on_progress_callback(progress_high)

        file_size_high = strm_high.filesize
        print(file_size_high)

        strm_high.download(output_path=path_to_save)
    except EXCEPTION as e:
        print(e)

# ------------------Thread target for Audio--------------------
def startDownloadLow(url):
    global file_size_low
    path_to_save_low = askdirectory()
    if path_to_save_low is None:
        return
    try:
        ob_low = YouTube(url)

        strm_low = ob_low.streams.get_audio_only()

        ob_low.register_on_complete_callback(down_complete_low)
        ob_low.register_on_progress_callback(progress_low)

        file_size_low = strm_low.filesize
        print(file_size_low)

        strm_low.download(output_path=path_to_save_low)
    except EXCEPTION as e:
        print(e)

# Multithreading for Video
def DownloadThreadHigh():
    try:
        # Changing Text of Button
        bttn_high.config(text="Please Wait...!")
        bttn_high.config(state=DISABLED)

        url = enter_url.get()
        if url == "":
            return
        print(url)

        thread = Thread(target=startDownloadHigh, args=(url,))
        thread.start()
    except EXCEPTION as e:
        print(e)

# Multithreadig for Audio
def DownloadThreadLow():
    try:
        # Changing Text of Button
        bttn_low.config(text="Please Wait...!")
        bttn_low.config(state=DISABLED)

        url = enter_url.get()
        if url == "":
            return
        print(url)

        thread_low = Thread(target=startDownloadLow, args=(url,))
        thread_low.start()
    except EXCEPTION as e:
        print(e)

# --------------------------------GUI---------------------------------
screen = Tk()
screen.title(" YouTube Video Downloader")
screen.geometry("1280x600")
screen.configure(background="#292929")
screen.iconbitmap("Resources\\dark.ico")

Heading = Label(screen, text="YouTube Video Downloader", fg="#FFF", bg="#292929", font="Courier 25 bold")
Heading.pack()

text_1 = Label(screen, text="Enter the Video URL", fg="#FFF", bg="#292929", font="Courier 18")
text_1.pack(pady="50")

enter_url = Entry(screen, width=50, bd="2", font="Courier 15 italic", justify=CENTER)
enter_url.pack()
enter_url.focus()

bttn_high = Button(screen, text="Download Video", fg="#FFF", bg="#E21919", font="Courier 15 bold", command=DownloadThreadHigh)
bttn_high.pack(pady=50)

bttn_low = Button(screen, text="Download Audio", fg="#FFF", bg="#E21919", font="Courier 15 bold", command=DownloadThreadLow)
bttn_low.pack(pady=30)

display_per = Label(screen, text="Remaining Quantity", fg="#FFF", bg="#292929", font="Courier 15")

title_vid = Label(screen, text="Video Title", fg="#FFF", bg="#292929", font="Courier 15 underline")

screen.mainloop()
