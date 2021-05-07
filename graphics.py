from tkinter import *
from tkinter import filedialog
from save import *


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Spotlight Wallpaper Grabber")
        self.root.geometry("420x80+500+250")

        self.path = StringVar()

        self.label = Label(self.root, text="Save Wallpaper to ")
        self.entry = Entry(self.root, textvariable=self.path)
        self.browse_btn = Button(self.root, text="Browse", command=self.browse)
        self.save_btn = Button(self.root, text=" Save ", command=self.execute)

        self.label.pack(side=LEFT, padx=10)
        self.entry.pack(side=LEFT, expand=True, fill=X, padx=10)
        self.browse_btn.pack(side=LEFT, padx=10)
        self.save_btn.pack(side=LEFT, padx=10)

        self.root.mainloop()

    def browse(self):
        self.path.set(filedialog.askdirectory())

    def execute(self):
        if self.entry.get():
            sl = SaveToLocal()
            self.save_btn.configure(text="{} Saved ✔".format(sl.execute(self.entry.get())))
