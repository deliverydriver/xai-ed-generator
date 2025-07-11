import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, "output", "request_log.jsonl")

class LogViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("xAI API Request Log Viewer")
        self.geometry("800x500")
        self.configure(bg="#f5f6fa")
        self.resizable(True, True)

        self.log_entries = []
        self.create_widgets()
        self.load_log()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("timestamp", "action", "params", "result_path"), show="headings")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("action", text="Action")
        self.tree.heading("params", text="Parameters")
        self.tree.heading("result_path", text="Result Path")
        self.tree.column("timestamp", width=160)
        self.tree.column("action", width=120)
        self.tree.column("params", width=350)
        self.tree.column("result_path", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self, bg="#f5f6fa")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="Refresh", command=self.load_log, bg="#40739e", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save As...", command=self.save_log, bg="#44bd32", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Copy Selected", command=self.copy_selected, bg="#e1b12c", fg="black").pack(side=tk.LEFT, padx=5)

    def load_log(self):
        self.tree.delete(*self.tree.get_children())
        self.log_entries = []
        if not os.path.exists(LOG_FILE):
            return
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    self.log_entries.append(entry)
                    params_str = json.dumps(entry["params"], ensure_ascii=False)[:200]
                    self.tree.insert("", "end", values=(
                        entry.get("timestamp", ""),
                        entry.get("action", ""),
                        params_str,
                        entry.get("result_path", "")
                    ))
                except Exception:
                    continue

    def save_log(self):
        if not self.log_entries:
            messagebox.showinfo("Info", "No log entries to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".jsonl", filetypes=[("JSONL files", "*.jsonl"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                for entry in self.log_entries:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            messagebox.showinfo("Saved", f"Log saved to {file_path}")

    def copy_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "No entry selected.")
            return
        text = ""
        for item in selected:
            values = self.tree.item(item, "values")
            text += "\t".join(str(v) for v in values) + "\n"
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Selected log entry copied to clipboard.")

if __name__ == "__main__":
    app = LogViewer()
    app.mainloop()