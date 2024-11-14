from tkinter import Tk
from gui.interface import PharmacyAppInterface

if __name__ == "__main__":
    root = Tk()
    app = PharmacyAppInterface(root)
    root.mainloop()
