import tkinter as tk
import sys
import time
import threading


# test function outside of the class
def start():
    starttime = time.time()
    for i in range(5):
        print("Waiting...", i)
        time.sleep(1)
    total = time.time() - starttime
    print("Process took: ", total)


class StdoutRedirector:
    """ allows to redirect stdout from print() statements to the widged passed
    as argument.
    ex:
    sys.stdout = StdoutRedirector(textwidget) """
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(flush=None):
        pass


# main class using tk.Tk as parent
class CoreGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.config(bg="darkgray")
        self.title("threading test")
        self.InitUI()
        self.button = tk.Button(self, text="Start", command=self.run_test)
        self.button.grid(column=0, row=1, columnspan=2)

    def InitUI(self):
        self.text_box = tk.Text(self, wrap='word', height=11, width=50)
        self.text_box.grid(column=0, row=0, columnspan=2, sticky='nswe',
                           padx=5, pady=5)
        # redirects output
        sys.stdout = StdoutRedirector(self.text_box)

    # function that calls itself meanwhile the thread is still running
    def refresh(self, thread):
        self.update()
        if thread.is_alive():
            print(f"{thread.getName()} is alive.")
            self.button.config(state=tk.DISABLED, text="Running...")
            self.after(350, lambda: self.refresh(thread))
            self.config(bg="red")
        else:
            self.button.config(state=tk.NORMAL, text="Start")
            self.config(bg="darkgray")
            print(f"{thread.getName()} is dead.")

    def run_test(self):
        thread = threading.Thread(target=start)
        thread.daemon = False
        thread.start()
        self.refresh(thread)


root = CoreGUI()
root.mainloop()
