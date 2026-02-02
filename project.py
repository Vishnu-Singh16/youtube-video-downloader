import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import yt_dlp

# ---------------- Progress Hook ----------------
def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
        try:
            percent = float(percent_str)
            progress_bar['value'] = percent
            status_label.config(text=f"Downloading... {percent}%")
            root.update_idletasks()
        except:
            pass

    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        status_label.config(text="Download finished ✅")

# ---------------- Download Function ----------------
def download():
    url = url_entry.get().strip()
    choice = option.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    progress_bar['value'] = 0
    status_label.config(text="Starting download...")

    try:
        # VIDEO (single file, no ffmpeg)
        if choice == "video":
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [progress_hook],
            }
        # AUDIO ONLY (m4a, no ffmpeg)
        else:
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',
                'outtmpl': '%(title)s.m4a',
                'progress_hooks': [progress_hook],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Download completed successfully!")

    except Exception as e:
        status_label.config(text="Error ❌")
        messagebox.showerror("Error", str(e))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("480x360")
root.resizable(False, False)

# PNG icon for window
try:
    icon = PhotoImage(file="youtube.png")
    root.iconphoto(False, icon)
except:
    pass

# Title
tk.Label(root, text="YouTube Downloader", font=("Arial", 14, "bold")).pack(pady=8)

# Logo inside window (optional but looks good)
try:
    logo = PhotoImage(file="youtube.png")
    logo_label = tk.Label(root, image=logo)
    logo_label.image = logo  # keep reference
    logo_label.pack(pady=5)
except:
    pass

# URL Entry
tk.Label(root, text="Enter YouTube URL:").pack()
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Options
option = tk.StringVar(value="video")
tk.Radiobutton(root, text="Download Video (MP4)", variable=option, value="video").pack()
tk.Radiobutton(root, text="Download Audio (M4A)", variable=option, value="audio").pack()

# Download Button
tk.Button(root, text="Download", width=22, command=download).pack(pady=15)

# Progress Bar
progress_bar = ttk.Progressbar(root, length=420, mode="determinate")
progress_bar.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

root.mainloop()


