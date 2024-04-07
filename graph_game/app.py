from tkinter import *
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

        # Create frames
        self.main_menu_frame = MainMenu(self)
        self.play_frame = Play(self)
        self.how_to_play_frame = HowToPlay(self)
        self.leaderboards_frame = Leaderboards(self)

        # Show main menu frame
        self.main_menu_frame.pack(fill='both', expand=True)

    def switch_soundtrack(self):
        if self.soundtrack_state.get():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['bg'] = 'white'

        # Title
        title = Label(self, text="Graph Game", font=('Helvetica', 60), bg='white')
        title.place(relx=0.5, rely=0.12, anchor='center')

        # Play Button
        play_button = Button(self, text='Play', bg='white', fg='black', borderless=1, font='Helvetica, 40', width=300,
                             command=self.show_play_frame)
        play_button.place(relx=0.5, rely=0.3, anchor='center')

        # How To Play Button
        how_to_play_button = Button(self, text='How To Play', bg='white', fg='black', borderless=1,
                                    font='Helvetica, 40', width=300,
                                    command=self.show_how_to_play_frame)
        how_to_play_button.place(relx=0.5, rely=0.45, anchor='center')

        # Leaderboards Button
        leaderboards_button = Button(self, text='Leaderboards', bg='white', fg='black', borderless=1,
                                     font='Helvetica, 40', width=300,
                                     command=self.show_leaderboards_frame)
        leaderboards_button.place(relx=0.5, rely=0.6, anchor='center')

        # Quit Button
        quit_button = Button(self, text='Quit', bg='white', fg='black', borderless=1, font='Helvetica, 40', width=300,
                             command=self.master.quit)
        quit_button.place(relx=0.5, rely=0.75, anchor='center')

        # Soundtrack Switch
        soundtrack_switch = Checkbutton(self, text='Music', var=self.master.soundtrack_state,
                                        command=self.master.switch_soundtrack, onvalue=True, offvalue=False,
                                        bg='white', font='Helvetica, 20')
        soundtrack_switch.place(relx=0.93, rely=0.95, anchor='center')

    def show_play_frame(self):
        self.master.play_frame.pack(fill='both', expand=True)
        self.pack_forget()

    def show_how_to_play_frame(self):
        self.master.how_to_play_frame.pack(fill='both', expand=True)
        self.pack_forget()

    def show_leaderboards_frame(self):
        self.master.leaderboards_frame.pack(fill='both', expand=True)
        self.pack_forget()


class Play(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['bg'] = 'white'

        # Back Button
        back_button = Button(self, text='Back to Main Menu', bg='white', fg='black', borderless=1,
                             font='Helvetica, 20', width=200,
                             command=self.show_main_menu)
        back_button.place(relx=0.5, rely=0.9, anchor='center')

    def show_main_menu(self):
        # Hide the current frame
        self.pack_forget()
        # Minimize the window
        self.master.geometry('1x1')
        # Update the window
        self.master.update_idletasks()
        # Restore the window size
        self.master.geometry('800x600')
        # Show the main menu frame
        self.master.main_menu_frame.pack(fill='both', expand=True)


class HowToPlay(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['bg'] = 'white'

        # Back Button
        back_button = Button(self, text='Back to Main Menu', bg='white', fg='black', borderless=1,
                             font='Helvetica, 20', width=200,
                             command=self.show_main_menu)
        back_button.place(relx=0.5, rely=0.9, anchor='center')

    def show_main_menu(self):
        # Hide the current frame
        self.pack_forget()
        # Minimize the window
        self.master.geometry('1x1')
        # Update the window
        self.master.update_idletasks()
        # Restore the window size
        self.master.geometry('800x600')
        # Show the main menu frame
        self.master.main_menu_frame.pack(fill='both', expand=True)


class Leaderboards(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['bg'] = 'white'

        # Back Button
        back_button = Button(self, text='Back to Main Menu', bg='white', fg='black', borderless=1,
                             font='Helvetica, 20', width=200,
                             command=self.show_main_menu)
        back_button.place(relx=0.5, rely=0.9, anchor='center')

    def show_main_menu(self):
        # Hide the current frame
        self.pack_forget()
        # Minimize the window
        self.master.geometry('1x1')
        # Update the window
        self.master.update_idletasks()
        # Restore the window size
        self.master.geometry('800x600')
        # Show the main menu frame
        self.master.main_menu_frame.pack(fill='both', expand=True)


if __name__ == '__main__':
    app = GraphGameGUI()
    app.mainloop()
