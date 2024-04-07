import tkinter as tk
from tkmacosx import Button
import pygame


class GraphGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Graph Game')
        self.geometry('800x600')
        self['bg'] = 'white'
        self.resizable(True, True)  # Make the window resizable

        # Initialize pygame mixer for music
        pygame.mixer.init()
        self.soundtrack = './Audio/Menu_Audio.mp3'
        pygame.mixer.music.load(self.soundtrack)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.soundtrack_state = tk.BooleanVar(value=True)

        # Create a frame dict
        self.frames = {
            'menu': MainMenu(self, self.switch_frame, self.soundtrack_state),
            'play': Play(self, self.switch_frame)
        }

        # Show main menu frame
        self.frames['menu'].pack(fill='both', expand=True)

    def switch_soundtrack(self):
        if self.soundtrack_state.get():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

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
    def __init__(self, parent, switch_frame, soundtrack_state):
        super().__init__(parent)
        self.configure(bg="white")
        self.soundtrack_state = soundtrack_state

        # Play button
        play_button = Button(self, text="Play", command=lambda: switch_frame('menu', 'play')
                             , bg='white', fg='black', borderless=1,
                             font='Helvetica, 40', width=300)
        play_button.place(relx=0.5, rely=0.3, anchor='center')

        # Title
        title = tk.Label(self, text="Graph Game", font=('Helvetica', 60), bg='white')
        title.place(relx=0.5, rely=0.12, anchor='center')

        # How To Play Button
        how_to_play_button = Button(self, text='How To Play', bg='white', fg='black', borderless=1,
                                    font='Helvetica, 40', width=300)
        # command=self.show_how_to_play_frame)
        how_to_play_button.place(relx=0.5, rely=0.45, anchor='center')

        # Leaderboards Button
        leaderboards_button = Button(self, text='Leaderboards', bg='white', fg='black', borderless=1,
                                     font='Helvetica, 40', width=300)
        # command=self.show_leaderboards_frame)
        leaderboards_button.place(relx=0.5, rely=0.6, anchor='center')

        # Quit Button
        quit_button = Button(self, text='Quit', bg='white', fg='black', borderless=1, font='Helvetica, 40', width=300)
        # command=self.master.quit)
        quit_button.place(relx=0.5, rely=0.75, anchor='center')

        # Soundtrack Switch
        soundtrack_switch = tk.Checkbutton(self, text='Music', var=self.soundtrack_state,
                                           command=parent.switch_soundtrack,
                                           onvalue=True, offvalue=False,
                                           bg='white', font='Helvetica, 20')
        soundtrack_switch.place(relx=0.93, rely=0.95, anchor='center')


class Play(tk.Frame):
    def __init__(self, parent, switch_frame):
        super().__init__(parent)
        self.configure(bg="white")

        # Put the back arrow image for the button
        back_image = tk.PhotoImage(file="./Images/back_arrow.png")
        # Make the image 10 times smaller
        resized_back_image = back_image.subsample(10, 10)

        back_button = Button(self, text="Back", command=lambda: switch_frame('play', 'menu'),
                             image=resized_back_image, background="white", borderless=1, )
        back_button.pack(side="top", anchor="nw", padx=10, pady=10)


# Create an instance of the GraphGameGUI class and start the application
gui = GraphGameGUI()
gui.mainloop()
