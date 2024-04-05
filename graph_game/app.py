import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphGameGUI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title('Graph Game')
        self.geometry('800x600')
    
    def run(self) -> None:
        self.mainloop()


if __name__ == '__main__':
    app = GraphGameGUI()
    app.run()