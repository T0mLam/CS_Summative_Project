import tkinter as tk


class CasinoApp(tk.Tk):
    # Add docstring
    def __init__(self) -> None:
        # Add docstring
        tk.Tk.__init__(self)
        self.title('Casino')
        self.geometry('800x600')
        
    # Write your code here

    def run(self) -> None:
        # Add docstring
        self.mainloop()


# Testing
if __name__ == '__main__':
    app = CasinoApp()
    app.run()
