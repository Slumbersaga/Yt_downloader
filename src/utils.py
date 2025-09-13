from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import yt_dlp
from utils import validate_url, download_progress_hook, handle_error

class YTDLPGUI:
    def __init__(self, master):
        self.master = master
        master.title("YT-DLP GUI")

        self.label = Label(master, text="Enter Video URL:")
        self.label.pack()

        self.url_var = StringVar()
        self.url_entry = Entry(master, textvariable=self.url_var, width=50)
        self.url_entry.pack()

        self.download_button = Button(master, text="Download", command=self.download_video)
        self.download_button.pack()

        self.status_label = Label(master, text="")
        self.status_label.pack()

    def download_video(self):
        url = self.url_var.get()
        if not validate_url(url):
            messagebox.showerror("Error", "Please enter a valid URL (http/https).")
            return

        self.status_label.config(text="Downloading...")
        self.master.update()

        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [download_progress_hook],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text="Download completed!")
        except Exception as e:
            handle_error(e)
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="")

def main():
    root = Tk()
    gui = YTDLPGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()