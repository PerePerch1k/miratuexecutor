import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time

class MiratuExecutor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Miratu Executor")
        self.window.geometry("400x300")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#000")
        self.style.configure("TLabel", font=("Segoe UI", 12), foreground="#aaa", background="#000")
        self.style.configure("TButton", font=("Segoe UI", 12), foreground="#fff", background="#7A288A", borderwidth=0)
        self.style.map("TButton", background=[("active", "#8e24aa")])

        self.main_frame = ttk.Frame(self.window, padding="10 10 10 10")
        self.main_frame.pack(fill="both", expand=True)

        self.lua_script_label = ttk.Label(self.main_frame, text="Lua Script:")
        self.lua_script_label.grid(column=0, row=0, sticky="W")

        self.lua_script_text = tk.Text(self.main_frame, height=10, width=40, font=("Consolas", 12), wrap="word", background="#000", foreground="#fff")  # White text on black background
        self.lua_script_text.grid(column=0, row=1, sticky="NSEW")

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(column=0, row=2, sticky="EW")

        self.attach_button = ttk.Button(self.button_frame, text="Attach", command=self.start_attach_thread)
        self.attach_button.pack(side="left", padx=5)

        self.inject_button = ttk.Button(self.button_frame, text="Inject", command=self.inject, state="disabled")
        self.inject_button.pack(side="left", padx=5)

        self.status_label = ttk.Label(self.main_frame, text="", foreground="#f00") # Red text label
        self.status_label.grid(column=0, row=3, sticky="W")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        self.window.mainloop()

    def start_attach_thread(self):
        self.detach()
        thread = threading.Thread(target=self.attach)
        thread.start()

    def attach(self):
        self.detach()
        process_list = subprocess.check_output("tasklist /NH /FI \"IMAGENAME eq RobloxPlayerBeta.exe\"", shell=True).decode("latin-1").strip().split("\n")
        if len(process_list) == 1 and process_list[0].strip() == "Info: No tasks are running which match the specified criteria.":
            self.status_label.config(foreground="#f00", text="No Roblox process found.")
            self.inject_button.config(state="disabled")
            return
        if len(process_list) > 1:
            raise Exception("Multiple Roblox processes found.")
        pid = int(process_list[0].split()[1])
        self.process = subprocess.Popen(["python", "executor.py", str(pid)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.status_label.config(foreground="#0f0", text="Roblox process found.")
        self.inject_button.config(state="normal")

    def detach(self):
        if getattr(self, "process", None):
            self.process.terminate()
            self.process.wait()
            self.process = None
            self.status_label.config(foreground="#f00", text="Roblox process detached.")
            self.inject_button.config(state="disabled")

    def inject(self):
        lua_script = self.lua_script_text.get("1.0", "end-1c")
        if not lua_script.strip():
            self.status_label.config(foreground="#f00", text="No Lua script provided.")
            return
        self.status_label.config(foreground="#0f0", text="Injecting Lua script...")
        self.process.stdin.write(lua_script.encode("utf-8"))
        self.process.stdin.flush()
        time.sleep(0.5)
        self.status_label.config(foreground="#0f0", text="Lua script injected.")

if __name__ == "__main__":
    executor = MiratuExecutor()
    executor.run()
