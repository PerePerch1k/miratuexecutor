import tkinter as tk
import subprocess
import threading
import time

class MiratuExecutor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Miratu Executor")

        self.lua_script = tk.Text(self.window, height=10, width=50)
        self.lua_script.pack()

        self.attach_button = tk.Button(self.window, text="Attach", command=self.start_attach_thread)
        self.attach_button.pack()

        self.inject_button = tk.Button(self.window, text="Inject", command=self.inject)
        self.inject_button.pack()

        self.process = None

    def start_attach_thread(self):
        self.detach()
        thread = threading.Thread(target=self.attach)
        thread.start()

    def attach(self):
        self.detach()
        process_list = subprocess.check_output("tasklist /NH /FI \"IMAGENAME eq RobloxPlayerBeta.exe\"", shell=True).decode("latin-1").strip().split("\n")
        if len(process_list) > 1:
            raise Exception("Multiple Roblox processes found.")
        if not process_list:
            raise Exception("No Roblox process found.")
        pid = int(process_list[0].split()[1])
        self.process = subprocess.Popen(["python", "executor.py", str(pid)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def detach(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None

    def inject(self):
        if self.process is None:
            print("Please attach to a Roblox process first.")
            return
        lua_script = self.lua_script.get("1.0", "end-1c")
        self.process.stdin.write(lua_script.encode() + b"\n")
        self.process.stdin.flush()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    executor = MiratuExecutor()
    executor.run()