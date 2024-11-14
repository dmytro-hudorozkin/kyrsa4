# kyrsa4/gui/app.py

import tkinter as tk
from gui.interface import PharmacyAppInterface

if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyAppInterface(root)
    root.mainloop()