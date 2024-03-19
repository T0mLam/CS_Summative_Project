import tkinter as tk


class CasinoApp(tk.Tk):
    """A graphical implementation of the casino app using Tkinter"""
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title('Casino')
        self.geometry('800x600')
        
    # Write your code here

    def run(self) -> None:
        """Start the game loop"""
        self.mainloop()


# Testing
if __name__ == '__main__':
    app = CasinoApp()
    app.run()
