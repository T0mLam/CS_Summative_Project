import tkinter as tk


class CasinoApp(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title('Casino')
        self.geometry('800x600')
        
    # Write your code here

    def run(self) -> None:
        self.mainloop()


if __name__ == '__main__':
    app = CasinoApp()
    app.run()