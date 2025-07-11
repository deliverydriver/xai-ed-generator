import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import sys

import main

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

AGE_GROUPS = ["Kids", "Teens", "Adults"]

class EduGenApp:
    def __init__(self, root):
        self.root = root
        root.title("Educational Generator")
        root.geometry("600x700")

        tk.Label(root, text="Enter Educational Topic:", font=("Arial", 12)).pack(pady=10)
        self.topic_entry = tk.Entry(root, width=50)
        self.topic_entry.pack(pady=5)

        # Style toggles
        style_frame = tk.Frame(root)
        style_frame.pack(pady=5)
        tk.Label(style_frame, text="Style:", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.style_var = tk.StringVar(value="Educational")
        tk.Radiobutton(style_frame, text="Educational", variable=self.style_var, value="Educational", command=self.toggle_custom_style).grid(row=0, column=1, padx=5)
        tk.Radiobutton(style_frame, text="Agentic", variable=self.style_var, value="Agentic", command=self.toggle_custom_style).grid(row=0, column=2, padx=5)
        self.custom_style_label = tk.Label(style_frame, text="Custom Agentic Style:")
        self.custom_style_entry = tk.Entry(style_frame, width=20)
        self.custom_style_label.grid(row=1, column=0, sticky="w", pady=2)
        self.custom_style_entry.grid(row=1, column=1, columnspan=2, pady=2)
        self.toggle_custom_style()

        # Age group toggles
        age_frame = tk.Frame(root)
        age_frame.pack(pady=5)
        tk.Label(age_frame, text="Age Group:", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.age_var = tk.StringVar(value=AGE_GROUPS[0])
        for idx, age in enumerate(AGE_GROUPS):
            tk.Radiobutton(age_frame, text=age, variable=self.age_var, value=age).grid(row=0, column=1+idx, padx=5)

        self.status = tk.StringVar()
        self.status.set("Ready.")
        tk.Label(root, textvariable=self.status, fg="blue").pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Generate Content", command=self.start_content, width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Generate Image", command=self.start_image, width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Generate Audio", command=self.start_audio, width=15).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Generate Video", command=self.start_video, width=15).grid(row=0, column=3, padx=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", maximum=4)
        self.progress.pack(pady=10)
        self.progress["value"] = 0

        tk.Button(root, text="Generate All", command=self.start_generation, bg="#4CAF50", fg="white", width=20).pack(pady=10)

        self.file_frame = tk.Frame(root)
        self.file_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.file_icons = {}
        self.session_files = []  # Track files generated in this session

    def toggle_custom_style(self):
        if self.style_var.get() == "Agentic":
            self.custom_style_label.grid()
            self.custom_style_entry.grid()
        else:
            self.custom_style_label.grid_remove()
            self.custom_style_entry.grid_remove()

    def get_inputs(self):
        topic = self.topic_entry.get().strip()
        style = self.style_var.get()
        custom_style = self.custom_style_entry.get().strip() if style == "Agentic" else ""
        age_group = self.age_var.get()
        if not topic:
            messagebox.showerror("Input Error", "Please enter a topic.")
            return None
        return topic, style, custom_style, age_group

    def start_generation(self):
        inputs = self.get_inputs()
        if not inputs:
            return
        threading.Thread(target=self.generate_all, args=inputs, daemon=True).start()

    def generate_all(self, topic, style, custom_style, age_group):
        self.progress["value"] = 0
        self.status.set("Generating content...")
        content, content_path = main.generate_content(topic, style, custom_style, age_group)
        self.session_files.append(content_path)
        self.progress["value"] = 1
        self.status.set("Content generated.")

        self.status.set("Generating image...")
        image_path = main.generate_image(content, topic, style, custom_style, age_group)
        self.session_files.append(image_path)
        self.progress["value"] = 2
        self.status.set("Image generated.")

        self.status.set("Generating audio...")
        audio_path = main.generate_audio(content, topic, style, custom_style, age_group)
        self.session_files.append(audio_path)
        self.progress["value"] = 3
        self.status.set("Audio generated.")

        self.status.set("Generating video (this may take a while)...")
        video_path = main.generate_video(content, topic, style, custom_style, age_group, callback=self.update_video_progress)
        self.session_files.append(video_path)
        self.progress["value"] = 4
        self.status.set("All files generated!")
        self.show_file_list()
        messagebox.showinfo("Done", f"All files saved in {OUTPUT_DIR}")

    def update_video_progress(self, status_data):
        if "progress" in status_data:
            try:
                progress = float(status_data['progress'])
                self.status.set(f"Video generation progress: {progress*100:.1f}%")
            except Exception:
                self.status.set("Video generation in progress...")
        else:
            self.handle_runway_api_status(status_data)

    def handle_runway_api_status(self, status_data):
        status_url = status_data.get("status_url")
        headers = status_data.get("headers", {})
        if not status_url:
            self.status.set("Invalid status data received.")
            return

        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                status_resp = requests.get(status_url, headers=headers, timeout=10)
                status_resp.raise_for_status()
                self.status.set("Runway API status checked successfully.")
                break
            except requests.exceptions.ConnectionError as e:
                self.status.set("Connection error, retrying in 10 seconds...")
                time.sleep(10)
                retries += 1
        else:
            self.status.set("Failed to connect to Runway API after multiple attempts.")

    def show_file_list(self):
        for widget in self.file_frame.winfo_children():
            widget.destroy()
        row = 0
        for fpath in self.session_files:
            fname = os.path.basename(fpath)
            icon = None
            try:
                if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    img = Image.open(fpath)
                    img.thumbnail((48, 48))
                    icon = ImageTk.PhotoImage(img)
                else:
                    icon = None
            except Exception:
                icon = None
            self.file_icons[fpath] = icon
            icon_label = tk.Label(self.file_frame, image=icon) if icon else tk.Label(self.file_frame, text="📄")
            icon_label.grid(row=row, column=0, padx=5, pady=5)
            name_label = tk.Label(self.file_frame, text=fname, anchor="w")
            name_label.grid(row=row, column=1, sticky="w")
            view_btn = tk.Button(self.file_frame, text="Open File", command=lambda p=fpath: self.open_file(p))
            view_btn.grid(row=row, column=2, padx=5)
            row += 1

    def open_file(self, path):
        if sys.platform.startswith("darwin"):
            subprocess.call(("open", path))
        elif os.name == "nt":
            os.startfile(path)
        elif os.name == "posix":
            subprocess.call(("xdg-open", path))

    def start_content(self):
        inputs = self.get_inputs()
        if not inputs:
            return
        threading.Thread(target=self.generate_content_only, args=inputs, daemon=True).start()

    def start_image(self):
        inputs = self.get_inputs()
        if not inputs:
            return
        threading.Thread(target=self.generate_image_only, args=inputs, daemon=True).start()

    def start_audio(self):
        inputs = self.get_inputs()
        if not inputs:
            return
        threading.Thread(target=self.generate_audio_only, args=inputs, daemon=True).start()

    def start_video(self):
        inputs = self.get_inputs()
        if not inputs:
            return
        threading.Thread(target=self.generate_video_only, args=inputs, daemon=True).start()

    def generate_content_only(self, topic, style, custom_style, age_group):
        self.status.set("Generating content...")
        content, content_path = main.generate_content(topic, style, custom_style, age_group)
        self.session_files.append(content_path)
        self.status.set("Content generated.")
        self.show_file_list()

    def generate_image_only(self, topic, style, custom_style, age_group):
        self.status.set("Generating image...")
        content_file_path = os.path.join(OUTPUT_DIR, "content", f"{topic.replace(' ', '_')}_content.txt")
        if os.path.exists(content_file_path):
            with open(content_file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = topic
        image_path = main.generate_image(content, topic, style, custom_style, age_group)
        self.session_files.append(image_path)
        self.status.set("Image generated.")
        self.show_file_list()

    def generate_audio_only(self, topic, style, custom_style, age_group):
        self.status.set("Generating audio...")
        content_file_path = os.path.join(OUTPUT_DIR, "content", f"{topic.replace(' ', '_')}_content.txt")
        if os.path.exists(content_file_path):
            with open(content_file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = topic
        audio_path = main.generate_audio(content, topic, style, custom_style, age_group)
        self.session_files.append(audio_path)
        self.status.set("Audio generated.")
        self.show_file_list()

    def generate_video_only(self, topic, style, custom_style, age_group):
        self.status.set("Generating video (this may take a while)...")
        content_file_path = os.path.join(OUTPUT_DIR, "content", f"{topic.replace(' ', '_')}_content.txt")
        if os.path.exists(content_file_path):
            with open(content_file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = topic
        video_path = main.generate_video(content, topic, style, custom_style, age_group, callback=self.update_video_progress)
        self.session_files.append(video_path)
        self.status.set("Video generated.")
        self.show_file_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = EduGenApp(root)
    root.mainloop()