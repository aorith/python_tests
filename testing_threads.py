import tkinter as tk
import sys
import time
import threading


def start():
    starttime = time.time()
    for i in range(5):
        print("Waiting...", i)
        time.sleep(1)
    total = time.time() - starttime
    print("Process took: ", total)


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(flush=None):
        pass


class CoreGUI(object):
    def __init__(self, parent):
        self.parent = parent
        self.parent.config(bg="darkgray")
        self.InitUI()
        self.button = tk.Button(self.parent, text="Start", command=self.test1)
        self.button.grid(column=0, row=1, columnspan=2)

    def InitUI(self):
        self.text_box = tk.Text(self.parent, wrap='word', height=11, width=50)
        self.text_box.grid(column=0, row=0, columnspan=2,
                           sticky='NSWE', padx=5, pady=5)
        sys.stdout = StdoutRedirector(self.text_box)

    def refresh(self):
        self.parent.update()
        if submit_thread.is_alive():
            print("alive.")
            self.button.config(state=tk.DISABLED)
            self.parent.after(350, self.refresh)
            self.parent.config(bg="red")
        else:
            self.button.config(state=tk.NORMAL)
            self.parent.config(bg="darkgray")
            print("dead.")

    def test1(self):
        global submit_thread
        submit_thread = threading.Thread(target=start)
        submit_thread.daemon = True
        submit_thread.start()
        self.refresh()


root = tk.Tk()
gui = CoreGUI(root)
root.mainloop()
