import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
import re

class MiratuExecutor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Miratu Executor")
        self.window.geometry("400x300")

        self.is_dark_theme = tk.BooleanVar(value=True)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        self.main_frame = ttk.Frame(self.window, padding="10 10 10 10")
        self.main_frame.pack(fill="both", expand=True)

        self.heading_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.heading_frame.grid(column=0, row=0, sticky="EW")
        self.heading_frame.columnconfigure(0, weight=1)
        self.heading_frame.columnconfigure(1, weight=1)

        self.heading_label = ttk.Label(self.heading_frame, text="Miratu Executor", font=("Segoe UI", 14, "bold"))
        self.heading_label.grid(column=0, row=0, sticky="W")

        self.theme_switch = ttk.Checkbutton(self.heading_frame, text="Color Theme", variable=self.is_dark_theme, command=self.toggle_theme, style="TCheckbutton")
        self.theme_switch.grid(column=1, row=0, sticky="E")

        self.lua_script_label = ttk.Label(self.main_frame, text="Lua Script:")
        self.lua_script_label.grid(column=0, row=1, sticky="W")

        self.lua_script_text = tk.Text(self.main_frame, height=10, width=40, font=("Consolas", 12), wrap="word")
        self.lua_script_text.grid(column=0, row=2, sticky="NSEW")
        self.lua_script_text.bind("<KeyRelease>", self.highlight_syntax)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(column=0, row=3, sticky="EW")

        self.attach_button = ttk.Button(self.button_frame, text="Attach", command=self.start_attach_thread)
        self.attach_button.pack(side="left", padx=5)

        self.inject_button = ttk.Button(self.button_frame, text="Inject", command=self.inject, state="disabled")
        self.inject_button.pack(side="left", padx=5)

        self.status_label = ttk.Label(self.main_frame, text="")  # Status label
        self.status_label.grid(column=0, row=4, sticky="W")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        # Tags for syntax highlighting
        self.lua_script_text.tag_configure("keyword", foreground="#d73a49")
        self.lua_script_text.tag_configure("string", foreground="#032f62")
        self.lua_script_text.tag_configure("comment", foreground="#6a737d")
        self.lua_script_text.tag_configure("number", foreground="#005cc5")

        self.apply_theme()

        self.window.mainloop()

    def configure_styles(self):
        self.style.configure("TFrame", background="#000000")  # Default to dark theme
        self.style.configure("TLabel", font=("Segoe UI", 12), foreground="#aaa", background="#000000")
        self.style.configure("TButton", font=("Segoe UI", 12), foreground="#fff", background="#00008B", borderwidth=0)  # Dark blue buttons
        self.style.map("TButton", background=[("active", "#0000CD")])  # Lighter blue when active
        self.style.configure("TCheckbutton", font=("Segoe UI", 12), foreground="#aaa", background="#000000", indicatoron=False)

    def toggle_theme(self):
        if self.is_dark_theme.get():
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_dark_theme(self):
        self.style.configure("TFrame", background="#000000")
        self.style.configure("TLabel", foreground="#aaa", background="#000000")
        self.style.configure("TButton", foreground="#fff", background="#00008B")
        self.style.map("TButton", background=[("active", "#0000CD")])
        self.style.configure("TCheckbutton", foreground="#aaa", background="#000000")
        self.lua_script_text.configure(background="#000000", foreground="#ffffff", insertbackground="#ffffff")
        self.status_label.configure(foreground="#ff0000")

    def apply_light_theme(self):
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("TLabel", foreground="#000000", background="#ffffff")
        self.style.configure("TButton", foreground="#000000", background="#add8e6")  # Light blue buttons
        self.style.map("TButton", background=[("active", "#87CEEB")])
        self.style.configure("TCheckbutton", foreground="#000000", background="#ffffff")
        self.lua_script_text.configure(background="#ffffff", foreground="#000000", insertbackground="#000000")
        self.status_label.configure(foreground="#ff0000")

    def apply_theme(self):
        if self.is_dark_theme.get():
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def start_attach_thread(self):
        self.detach()
        thread = threading.Thread(target=self.attach)
        thread.start()

    def attach(self):
        self.detach()
        process_list = subprocess.check_output("tasklist /NH /FI \"IMAGENAME eq RobloxPlayerBeta.exe\"", shell=True).decode("latin-1").strip().split("\n")
        if len(process_list) == 1 and process_list[0].strip() == "Info: No tasks are running which match the specified criteria.":
            self.status_label.config(foreground="#ff0000", text="No Roblox process found.")
            self.inject_button.config(state="disabled")
            return
        if len(process_list) > 1:
            raise Exception("Multiple Roblox processes found.")
        pid = int(process_list[0].split()[1])
        self.process = subprocess.Popen(["python", "executor.py", str(pid)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.status_label.config(foreground="#00ff00", text="Roblox process found.")
        self.inject_button.config(state="normal")

    def detach(self):
        if getattr(self, "process", None):
            self.process.terminate()
            self.process.wait()
            self.process = None
            self.status_label.config(foreground="#ff0000", text="Roblox process detached.")
            self.inject_button.config(state="disabled")

    def inject(self):
        lua_script = self.lua_script_text.get("1.0", "end-1c")
        if not lua_script.strip():
            self.status_label.config(foreground="#ff0000", text="No Lua script provided.")
            return
        self.status_label.config(foreground="#00ff00", text="Injecting Lua script...")
        self.process.stdin.write(lua_script.encode("utf-8"))
        self.process.stdin.flush()
        time.sleep(0.5)
        self.status_label.config(foreground="#00ff00", text="Lua script injected.")

    def highlight_syntax(self, event=None):
        self.lua_script_text.tag_remove("keyword", "1.0", "end")
        self.lua_script_text.tag_remove("string", "1.0", "end")
        self.lua_script_text.tag_remove("comment", "1.0", "end")
        self.lua_script_text.tag_remove("number", "1.0", "end")

        keywords = r"\b(and|break|do|else|elseif|end|false|for|function|if|in|local|nil|not|or|repeat|return|then|true|until|while)\b"
        strings = r"(\".*?\"|\'.*?\')"
        comments = r"(--.*?$)"
        numbers = r"\b\d+\b"

        content = self.lua_script_text.get("1.0", "end-1c")

        for match in re.finditer(keywords, content, re.MULTILINE):
            self.lua_script_text.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        
        for match in re.finditer(strings, content, re.MULTILINE):
            self.lua_script_text.tag_add("string", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(comments, content, re.MULTILINE):
            self.lua_script_text.tag_add("comment", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(numbers, content, re.MULTILINE):
            self.lua_script_text.tag_add("number", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

if __name__ == "__main__":
    executor = MiratuExecutor()
    executor.run()
