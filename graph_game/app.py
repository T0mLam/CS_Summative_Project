import os
import tkinter as tk
from tkmacosx import Button
import pygame
from tkinter import ttk
from game_logic import GraphGame
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

class GraphGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Graph Game')
        self.geometry('800x600')
        self['bg'] = 'white'
        self.resizable(False, False)  # Make the window resizable

        # Initialize pygame mixer for music
        pygame.mixer.init()
        self.soundtrack_path = os.path.dirname(__file__) + '/audio/Menu_Audio.mp3'
        pygame.mixer.music.load(self.soundtrack_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.soundtrack_state = tk.BooleanVar(value=True)

        # Create a frame dict
        self.frames = {
            'menu': MainMenu(self),
            'play': Play(self)
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
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        # Play button
        play_button = Button(self, text="Play", command=lambda: parent.switch_frame('menu', 'play')
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
        soundtrack_switch = tk.Checkbutton(self, text='Music', var=parent.soundtrack_state,
                                           command=parent.switch_soundtrack,
                                           onvalue=True, offvalue=False,
                                           bg='white', font='Helvetica, 20')
        soundtrack_switch.place(relx=0.93, rely=0.95, anchor='center')




class Play(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        self.game = GraphGame.random_start()
        self.game.set_base_score(100)

        self.balance = int(100)
        #Balance variable for putting into Label
        balance_variable = tk.StringVar()
        balance_variable.set("Balance: " + str(self.balance))

        # Coefficient variable
        self.coefficient = int(0)
        # Coefficient variable for putting into Label
        coefficient_variable = tk.StringVar()
        coefficient_variable.set("Coefficient: " + str(self.coefficient))

        # Chance of winning variable
        self.chance_of_winning = int(0)
        # Chance of winning variable for putting into Label
        chance_of_winning_variable = tk.StringVar()
        chance_of_winning_variable.set("Chance of Win: " + str(self.chance_of_winning) + "%")

        # Put the back arrow image for the button
        back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png")
        # Make the image 10 times smaller
        resized_back_image = back_image.subsample(10, 10)

        back_button = Button(self, command=lambda: parent.switch_frame('play', 'menu'),
                             image=resized_back_image, background="white", borderless=1)
        back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Put the back arrow image for the button
        buy_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/shopping_cart.png")
        # Make the image 10 times smaller
        resized_buy_image = buy_image.subsample(10, 10)

        # Button for buying credits
        buy_button = Button(self, command=lambda: parent.switch_frame('play', 'menu'),
                            image=resized_buy_image, background="white", borderless=1)
        buy_button.pack(side="top", anchor="ne", padx=10, pady=10)

        #Label with the balance and balance wariable
        Balance_Label = tk.Label(self, textvariable=balance_variable, bg='white', fg='black', font='Helvetica, 20')
        Balance_Label.place(relx=0.8, rely=0.05, anchor='center')

        # Label Bid before the scale
        Bid_Label = tk.Label(self, text = "Bid:", bg='white', fg='black',
                             font='Helvetica, 20')
        Bid_Label.place(relx=0.76, rely=0.57, anchor='center')

        # Scale with changing the bid
        bid_scale = tk.Scale(self, from_=0, to=self.balance, orient=tk.HORIZONTAL,
                                  length=160,
                                  bg='white', fg='black',
                                  font = 'Helvetica, 20',
                                  )
        bid_scale.place(relx=0.89, rely=0.55, anchor='center')

        

        # Starting node label
        Starting_node = ttk.Combobox(self, width=5)
        Starting_node['values'] = Starting_node['values'] = self.game.get_node_numbers()
        Starting_node.place(relx=0.94, rely=0.36, anchor='center')

        # Starting node combobox
        Starting_node_Label = tk.Label(self, text = "Starting node:", bg='white', fg='black',
                                       font='Helvetica, 20')
        Starting_node_Label.place(relx=0.81, rely=0.35, anchor='center')

        # Ending node label
        Ending_node = ttk.Combobox(self, width=5)
        Ending_node['values'] = Starting_node['values'] = self.game.get_node_numbers()
        Ending_node.place(relx=0.94, rely=0.46, anchor='center')

        # Starting node combobox
        Ending_node_label = tk.Label(self, text="Ending node: ", bg='white', fg='black',
                                       font='Helvetica, 20')
        Ending_node_label.place(relx=0.81, rely=0.45, anchor='center')

        # Coefficient label with coefficient variable
        Coefficient_label = tk.Label(self, textvariable=coefficient_variable, bg='white', font='Helvetica, 20')
        Coefficient_label.place(relx=0.82, rely=0.68, anchor='center')

        # Chance of winning label with chance of winning variable
        Chance_Of_Winning_label = tk.Label(self, textvariable=chance_of_winning_variable, bg='white', font='Helvetica, 20')
        Chance_Of_Winning_label.place(relx=0.85, rely=0.78, anchor='center')

        Bet_Button = Button(self, text = "BET", bg = 'white', fg = 'black',
                               font='Helvetica, 20',
                               borderless=1,
                               width=150)
        Bet_Button.place(relx=0.87, rely=0.9, anchor='center')


        canvas = tk.Canvas(self, width=530, height=480, bg="white")
        canvas.place(relx=0.34, rely=0.59, anchor='center')


if __name__ == '__main__':
    app = GraphGameGUI()

    app.mainloop()