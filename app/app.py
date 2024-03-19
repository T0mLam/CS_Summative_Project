import tkinter as tk


class CasinoApp(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title('Casino')
        self.geometry('800x600')
        