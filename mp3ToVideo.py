import os
import subprocess
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, font


class RetroTerminalMP3ToVideoConverter:
    def __init__(self, master):
        self.master = master
        master.title("Audio Video Creator")
        master.geometry("550x300")

        # Retro terminal color palette
        self.colors = {
            'background': '#000000',
            'text_primary': '#00FF00',  # Bright green
            'text_secondary': '#00AA00',  # Darker green
            'button_primary': '#005500',
            'button_secondary': '#00FF00',
            'entry_background': '#000000',
            'entry_text': '#00FF00'
        }
        master.configure(bg=self.colors['background'])

        # Custom fonts (use a monospace font for true terminal feel)
        self.title_font = font.Font(family="Courier", size=14, weight="bold")
        self.label_font = font.Font(family="Courier", size=10)
        self.button_font = font.Font(family="Courier", size=10, weight="bold")

        # Main container
        self.container = tk.Frame(master, bg=self.colors['background'])
        self.container.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        # Title
        self.title_label = tk.Label(
            self.container,
            text="AUDIO VIDEO CONVERTER",
            font=self.title_font,
            bg=self.colors['background'],
            fg=self.colors['text_primary']
        )
        self.title_label.pack(pady=(0, 10))

        # MP3 Selection Frame
        self.mp3_frame = self._create_file_selection_frame(
            "MP3 FILE:",
            self.select_mp3
        )
        self.mp3_frame.pack(fill=tk.X, pady=5)

        # PNG Selection Frame
        self.png_frame = self._create_file_selection_frame(
            "COVER IMAGE:",
            self.select_png
        )
        self.png_frame.pack(fill=tk.X, pady=5)

        # Convert Button
        self.convert_button = tk.Button(
            self.container,
            text="CREATE VIDEO",
            command=self.convert,
            font=self.button_font,
            bg=self.colors['button_primary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['button_secondary'],
            activeforeground=self.colors['background'],
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.convert_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(
            self.container,
            text="",
            font=self.label_font,
            bg=self.colors['background'],
            fg=self.colors['text_secondary']
        )
        self.status_label.pack(pady=5)

        # Paths to store
        self.mp3_path = tk.StringVar()
        self.png_path = tk.StringVar()

    def _create_file_selection_frame(self, label_text, browse_command):
        frame = tk.Frame(self.container, bg=self.colors['background'])

        # Label
        label = tk.Label(
            frame,
            text=label_text,
            font=self.label_font,
            bg=self.colors['background'],
            fg=self.colors['text_primary']
        )
        label.pack(side=tk.TOP, anchor='w')

        # Entry and Browse Container
        entry_container = tk.Frame(frame, bg=self.colors['background'])
        entry_container.pack(fill=tk.X, pady=(3, 0))

        # Entry
        entry = tk.Entry(
            entry_container,
            font=self.label_font,
            width=50,
            state='readonly',
            bg=self.colors['entry_background'],
            fg=self.colors['entry_text'],
            insertbackground=self.colors['text_primary'],
            relief=tk.FLAT,
            readonlybackground=self.colors['entry_background'],
            disabledbackground=self.colors['entry_background'],
            disabledforeground=self.colors['entry_text']
        )
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        # Browse Button
        browse_btn = tk.Button(
            entry_container,
            text="BROWSE",
            command=browse_command,
            font=self.label_font,
            bg=self.colors['button_primary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['button_secondary'],
            activeforeground=self.colors['background'],
            relief=tk.FLAT
        )
        browse_btn.pack(side=tk.RIGHT)

        # Store reference for later use
        if label_text == "MP3 FILE:":
            self.mp3_entry = entry
        else:
            self.png_entry = entry

        return frame

    def select_mp3(self):
        filename = filedialog.askopenfilename(
            filetypes=[("MP3 Files", "*.mp3")],
            title="Select MP3 File"
        )
        if filename:
            self.mp3_path.set(filename)
            self.mp3_entry.config(state='normal')
            self.mp3_entry.delete(0, tk.END)
            self.mp3_entry.insert(0, os.path.basename(filename))
            self.mp3_entry.config(state='readonly')

    def select_png(self):
        filename = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png")],
            title="Select Cover Image"
        )
        if filename:
            self.png_path.set(filename)
            self.png_entry.config(state='normal')
            self.png_entry.delete(0, tk.END)
            self.png_entry.insert(0, os.path.basename(filename))
            self.png_entry.config(state='readonly')

    def convert(self):
        mp3 = self.mp3_path.get()
        png = self.png_path.get()

        if not mp3 or not png:
            messagebox.showerror(
                "ERROR",
                "PLEASE SELECT BOTH MP3 AND PNG FILES",
                icon='warning'
            )
            return

        # Start a thread for the conversion process
        conversion_thread = threading.Thread(target=self._run_conversion, args=(mp3, png))
        conversion_thread.start()

        # Start the animation for "COMPUTER IS THINKING..."
        self._animate_status_label("COMPUTER IS THINKING")

    def _run_conversion(self, mp3, png):
        try:
            # Video creation logic
            output_path = self._create_video_from_audio_and_image(mp3, png)

            # Stop animation and show success
            self.stop_animation = True
            self.status_label.config(text="")  # Clear status
            messagebox.showinfo("SUCCESS", f"VIDEO CREATED AT:\n{output_path}")
        except Exception as e:
            # Stop animation and show error
            self.stop_animation = True
            self.status_label.config(text="")  # Clear status
            messagebox.showerror("ERROR", str(e), icon='error')

    def _animate_status_label(self, base_text):
        """Animates the status label with a '...' effect."""
        self.stop_animation = False
        def animate():
            dots = ""
            while not self.stop_animation:
                self.status_label.config(text=f"{base_text}{dots}")
                self.master.update()  # Force the UI to update
                dots = "." if dots == "..." else dots + "."
                time.sleep(0.5)  # Wait 500ms between updates

        threading.Thread(target=animate, daemon=True).start()

    def _create_video_from_audio_and_image(self, mp3_path, png_path):
        """Create video from MP3 and PNG using FFmpeg."""
        mp3_dir = os.path.dirname(mp3_path)
        mp3_filename = os.path.splitext(os.path.basename(mp3_path))[0]
        output_video_path = os.path.join(mp3_dir, f"{mp3_filename}.mp4")

        ffmpeg_command = [
            "ffmpeg",
            "-loop", "1",
            "-i", png_path,
            "-i", mp3_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]

        try:
            subprocess.run(ffmpeg_command, check=True)
            return output_video_path
        except Exception as e:
            raise RuntimeError(f"VIDEO CREATION FAILED: {e}")


def main():
    root = tk.Tk()
    root.resizable(False, False)  # Prevent window resizing
    app = RetroTerminalMP3ToVideoConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
