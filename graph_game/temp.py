import tkinter as tk
from tkmacosx import Button


class GraphGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Graph Game')
        self.geometry('800x600')
        self['bg'] = 'white'
        self.resizable(True, True)  # Make the window resizable

        # Create a frame dict
        self.frames = {
            'menu': MainMenu(self, self.switch_frame),
            'play': Play(self, self.switch_frame)
        }
        
        # Show main menu frame
        self.frames['menu'].pack(fill='both', expand=True)

    def switch_frame(self, current_frame, new_frame):
        # Hide the current frame
        self.frames[current_frame].pack_forget()
        # Minimize the window
        self.geometry('1x1')
        # Update the window
        self.update_idletasks()
        # Restore the window size
        self.geometry('800x600')
        # Show the main menu frame
        self.frames[new_frame].pack(fill='both', expand=True)


class MainMenu(tk.Frame):
    def __init__(self, parent, switch_frame):
        super().__init__(parent)
        self.configure(bg="red")

        play_button = Button(self, text="Play", command=lambda: switch_frame('menu', 'play'))
        play_button.pack()

        label = tk.Label(self, text="Main Menu Frame")
        label.pack()

        
class Play(tk.Frame):
    def __init__(self, parent, switch_frame):
        super().__init__(parent)
        self.configure(bg="blue")

        back_button = Button(self, text="Back", command=lambda: switch_frame('play', 'menu'))
        back_button.pack()

        label = tk.Label(self, text="Play Frame")
        label.pack()


# Create an instance of the GraphGameGUI class and start the application
gui = GraphGameGUI()
gui.mainloop()