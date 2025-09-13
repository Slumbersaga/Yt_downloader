import os
import threading
import time
import re
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, filedialog, ttk, Frame, PhotoImage, LEFT, RIGHT, TOP, BOTTOM, X, Y, BOTH
from PIL import Image, ImageTk
import yt_dlp

class YTDLPGUI:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Video Downloader")
        master.geometry("540x420")
        master.resizable(False, False)
        self.cancelled = False
        self.download_thread = None
        self.video_info = None
        self.start_time = None

        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TEntry', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))
        style.configure('TFrame', background='#f7f7fa')
        master.configure(bg='#f7f7fa')

        # Header
        header = Label(master, text="YouTube Video Downloader", font=("Segoe UI", 16, "bold"), bg='#f7f7fa', fg="#333")
        header.pack(pady=(12, 2))

        # URL Section
        url_frame = Frame(master, bg='#f7f7fa')
        url_frame.pack(pady=8, fill=X, padx=20)
        Label(url_frame, text="Video URL:", bg='#f7f7fa').pack(side=LEFT, padx=5)
        self.url_var = StringVar()
        self.url_entry = Entry(url_frame, textvariable=self.url_var, width=38)
        self.url_entry.pack(side=LEFT, padx=5)
        Button(url_frame, text="Fetch Info", command=self.fetch_info, width=10).pack(side=LEFT, padx=5)

        # Video Info Section
        info_frame = Frame(master, bg='#f7f7fa')
        info_frame.pack(pady=2, fill=X, padx=20)
        self.thumb_label = Label(info_frame, bg='#f7f7fa')
        self.thumb_label.pack(side=LEFT, padx=5)
        self.title_var = StringVar()
        self.title_label = Label(info_frame, textvariable=self.title_var, bg='#f7f7fa', fg="#444", wraplength=320, justify=LEFT)
        self.title_label.pack(side=LEFT, padx=10)

        # Resolution Section
        res_frame = Frame(master, bg='#f7f7fa')
        res_frame.pack(pady=8, fill=X, padx=20)
        Label(res_frame, text="Resolution:", bg='#f7f7fa').pack(side=LEFT, padx=5)
        self.res_var = StringVar(value="best")
        self.res_combo = ttk.Combobox(res_frame, textvariable=self.res_var, state="readonly",
                                      values=["best", "1080p", "720p", "480p", "360p", "audio only"], width=12)
        self.res_combo.pack(side=LEFT, padx=5)

        # Output Folder Section
        out_frame = Frame(master, bg='#f7f7fa')
        out_frame.pack(pady=8, fill=X, padx=20)
        Label(out_frame, text="Save to:", bg='#f7f7fa').pack(side=LEFT, padx=5)
        self.folder_var = StringVar(value=os.getcwd())
        self.folder_entry = Entry(out_frame, textvariable=self.folder_var, width=28, state="readonly")
        self.folder_entry.pack(side=LEFT, padx=5)
        Button(out_frame, text="Browse", command=self.browse_folder, width=8).pack(side=LEFT, padx=5)
        Button(out_frame, text="Open", command=self.open_folder, width=8).pack(side=LEFT, padx=5)

        # Download and Cancel Buttons
        btn_frame = Frame(master, bg='#f7f7fa')
        btn_frame.pack(pady=10)
        self.download_button = Button(btn_frame, text="Download", command=self.start_download, bg="#4CAF50", fg="white", width=15)
        self.download_button.pack(side=LEFT, padx=10)
        self.cancel_button = Button(btn_frame, text="Cancel", command=self.cancel_download, bg="#f44336", fg="white", width=15, state="disabled")
        self.cancel_button.pack(side=LEFT, padx=10)

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=420, mode="determinate")
        self.progress.pack(pady=10)

        # Status Label
        self.status_var = StringVar()
        self.status_label = Label(master, textvariable=self.status_var, fg="#1a73e8", bg='#f7f7fa', font=("Segoe UI", 10, "italic"))
        self.status_label.pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def open_folder(self):
        folder = self.folder_var.get()
        if os.path.isdir(folder):
            os.startfile(folder)

    def is_valid_url(self, url):
        # Simple YouTube URL validation
        return re.match(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/", url)

    def fetch_info(self):
        url = self.url_var.get().strip()
        if not self.is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        self.status_var.set("Fetching video info...")
        self.title_var.set("")
        self.thumb_label.config(image='')
        self.master.update_idletasks()
        threading.Thread(target=self._fetch_info_thread, args=(url,)).start()

    def _fetch_info_thread(self, url):
        try:
            ydl_opts = {'quiet': True, 'skip_download': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            self.video_info = info
            title = info.get('title', 'Unknown Title')
            thumb_url = info.get('thumbnail')
            self.master.after(0, self._update_video_info, title, thumb_url)
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch info: {e}"))
            self.master.after(0, lambda: self.status_var.set(""))

    def _update_video_info(self, title, thumb_url):
        self.title_var.set(title)
        self.status_var.set("Video info loaded.")
        if thumb_url:
            try:
                import requests
                from io import BytesIO
                response = requests.get(thumb_url, timeout=5)
                img = Image.open(BytesIO(response.content)).resize((80, 60))
                self.thumb_img = ImageTk.PhotoImage(img)
                self.thumb_label.config(image=self.thumb_img)
            except Exception:
                self.thumb_label.config(image='')

    def get_format_string(self):
        res = self.res_var.get()
        if res == "best":
            return "bestvideo+bestaudio/best"
        elif res == "audio only":
            return "bestaudio"
        else:
            height = ''.join(filter(str.isdigit, res))
            return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

    def start_download(self):
        url = self.url_var.get().strip()
        folder = self.folder_var.get().strip()
        if not self.is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        if not os.path.isdir(folder):
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create folder: {e}")
                return
        self.cancelled = False
        self.progress["value"] = 0
        self.download_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.status_var.set("Starting download...")
        self.start_time = time.time()
        self.disable_controls()
        self.download_thread = threading.Thread(target=self.download_video, args=(url, folder))
        self.download_thread.start()

    def cancel_download(self):
        self.cancelled = True
        self.status_var.set("Cancelling download...")
        self.cancel_button.config(state="disabled")

    def download_video(self, url, folder):
        ydl_opts = {
            'format': self.get_format_string(),
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [self.download_progress_hook],
            'restrictfilenames': True,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if not self.cancelled:
                self.master.after(0, lambda: self.status_var.set("Download completed!"))
            else:
                self.master.after(0, lambda: self.status_var.set("Download cancelled."))
        except Exception as e:
            if not self.cancelled:
                self.master.after(0, lambda: messagebox.showerror("Error", str(e)))
                self.master.after(0, lambda: self.status_var.set(""))
        self.master.after(0, self.reset_buttons)

    def download_progress_hook(self, d):
        if self.cancelled:
            raise yt_dlp.utils.DownloadCancelled()
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '').strip().replace('%', '')
            try:
                percent_float = float(percent)
            except Exception:
                percent_float = 0
            eta = d.get('eta', '')
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            status = f"Downloading... {percent}% | ETA: {eta}s | Elapsed: {elapsed}s"
            self.master.after(0, lambda: self.progress.config(value=percent_float))
            self.master.after(0, lambda: self.status_var.set(status))
        elif d['status'] == 'finished':
            self.master.after(0, lambda: self.progress.config(value=100))
            self.master.after(0, lambda: self.status_var.set("Download finished. Finalizing..."))

    def reset_buttons(self):
        self.download_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.enable_controls()

    def disable_controls(self):
        self.url_entry.config(state="disabled")
        self.res_combo.config(state="disabled")
        self.folder_entry.config(state="disabled")

    def enable_controls(self):
        self.url_entry.config(state="normal")
        self.res_combo.config(state="readonly")
        self.folder_entry.config(state="readonly")

def main():
    root = Tk()
    gui = YTDLPGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()