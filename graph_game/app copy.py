import os
import tkinter as tk

import pygame
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from game_logic import GraphGame

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
        # Change the voulme of music
        pygame.mixer.music.set_volume(0.5)
        # Loop
        pygame.mixer.music.play(-1)

        self.soundtrack_state = tk.BooleanVar(value=True)

        # Create a frame dict
        self.frames = {
            'menu': MainMenu(self),
            'play': Play(self),
            'win': Win(self),
            'lose' : Lose(self)
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
        play_button = tk.Button(self, text="Play", command=lambda: parent.switch_frame('menu', 'play')
                             , bg='white', fg='black',
                             font='Helvetica, 40', width=10)
        play_button.place(relx=0.5, rely=0.3, anchor='center')

        # Title
        title = tk.Label(self, text="Graph Game", font=('Helvetica', 60), bg='white')
        title.place(relx=0.5, rely=0.12, anchor='center')

        # How To Play Button
        how_to_play_button = tk.Button(self, text='How To Play', bg='white', fg='black',
                                    font='Helvetica, 40', width=10)
        # command=self.show_how_to_play_frame)
        how_to_play_button.place(relx=0.5, rely=0.45, anchor='center')

        # Leaderboards Button
        leaderboards_button = tk.Button(self, text='Leaderboards', bg='white', fg='black',
                                     font='Helvetica, 40', width=10)
        # command=self.show_leaderboards_frame)
        leaderboards_button.place(relx=0.5, rely=0.6, anchor='center')

        # Quit Button
        quit_button = tk.Button(self, text='Quit', bg='white', fg='black', font='Helvetica, 40', width=10)
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
        self.parent = parent
        self.game = GraphGame.random_start()
        self.game.set_base_score(100)

        self.configure(bg="white")

        self.balance = int(100)
        #Balance variable for putting into Label
        self.balance_variable = tk.StringVar()
        self.balance_variable.set("Balance: " + str(self.balance))

        # Coefficient variable
        self.coefficient = int(0)
        # Coefficient variable for putting into Label
        self.coefficient_variable = tk.StringVar()
        self.coefficient_variable.set("Coefficient: " + str(self.coefficient))

        # Chance of winning variable
        self.chance_of_winning = int(0)
        # Chance of winning variable for putting into Label
        self.chance_of_winning_variable = tk.StringVar()
        self.chance_of_winning_variable.set("Chance of Win: " + str(self.chance_of_winning) + "%")

        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png")
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button 
        self.back_button = tk.Button(self, command=lambda: parent.switch_frame('play', 'menu'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Put the back arrow image for the button
        self.buy_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/shopping_cart.png")
        # Make the image 10 times smaller
        self.resized_buy_image = self.buy_image.subsample(10, 10)

        # Button for buying credits
        self.buy_button = tk.Button(self, command=lambda: parent.switch_frame('play', 'lose'),
                            image=self.resized_buy_image, background="white")
        self.buy_button.pack(side="top", anchor="ne", padx=10, pady=10)

        #Label with the balance and balance wariable
        self.Balance_Label = tk.Label(self, textvariable=self.balance_variable, bg='white', fg='black', font='Helvetica, 20')
        self.Balance_Label.place(relx=0.8, rely=0.05, anchor='center')

        # Label Bid before the scale
        self.Bid_Label = tk.Label(self, text = "Bid:", bg='white', fg='black',
                             font='Helvetica, 20')
        self.Bid_Label.place(relx=0.76, rely=0.57, anchor='center')

        # Scale with changing the bid
        self.bid_scale = tk.Scale(self, from_=0, to=self.balance, orient=tk.HORIZONTAL,
                                  length=160,
                                  bg='white', fg='black',
                                  font = 'Helvetica, 20',
                                  )
        self.bid_scale.place(relx=0.89, rely=0.55, anchor='center')

        # Starting node combobox
        self.Starting_node_combobox = ttk.Combobox(self, width=5)
        # Fill the combobox with the values of the graph
        self.Starting_node_combobox['values'] = self.game.get_nodes()
        self.Starting_node_combobox.place(relx=0.94, rely=0.36, anchor='center')
        # Bind the method update_ending node state to the combobox
        self.Starting_node_combobox.bind("<<ComboboxSelected>>", self.update_ending_node_state)
        # Bind the same method but as Focus Out to always check if the starting node combobox value was not deleted
        self.Starting_node_combobox.bind("<FocusOut>", self.update_ending_node_state)

        # Starting node combobox label
        self.Starting_node_combobox_Label = tk.Label(self, text="Starting node:", bg='white', fg='black',
                                    font='Helvetica, 20')
        self.Starting_node_combobox_Label.place(relx=0.81, rely=0.35, anchor='center')

        # Ending node combobox
        self.Ending_node_combobox = ttk.Combobox(self, width=5, state='disabled')
        # Fill the combobox with the values of the graph
        self.Ending_node_combobox['values'] = self.game.get_nodes()
        self.Ending_node_combobox.place(relx=0.94, rely=0.46, anchor='center')

        # Ending node combobox label
        self.Ending_node_combobox_Label = tk.Label(self, text="Ending node:", bg='white', fg='black',
                                    font='Helvetica, 20')
        self.Ending_node_combobox_Label.place(relx=0.81, rely=0.45, anchor='center')

        # Coefficient label with coefficient variable
        self.Coefficient_label = tk.Label(self, textvariable=self.coefficient_variable, bg='white', font='Helvetica, 20')
        self.Coefficient_label.place(relx=0.82, rely=0.68, anchor='center')

        # Chance of winning label with chance of winning variable
        self.Chance_Of_Winning_label = tk.Label(self, textvariable=self.chance_of_winning_variable, bg='white', font='Helvetica, 20')
        self.Chance_Of_Winning_label.place(relx=0.85, rely=0.78, anchor='center')

        self.Bet_Button = tk.Button(self, text = "BET", bg = 'white', fg = 'black',
                               font='Helvetica, 25',
                               width=10,
                               command=self.Bet_Start_Game)
        self.Bet_Button.place(relx=0.86, rely=0.9, anchor='center')

        self.canvas = tk.Canvas(self, width=530, height=480, bg="white")
        self.canvas.place(relx=0.34, rely=0.59, anchor='center')

        self.update_plot()
    
    def update_ending_node_state(self, event=None):
        """Method makes ending node combobox disabled if starting node combobox is not chosen"""
        
        # Check if starting node combobox is empty
        if not self.Starting_node_combobox.get():  
            # Delete ending node selection
            self.Ending_node_combobox.set('')  
            # Disable the combobox
            self.Ending_node_combobox['state'] = 'disabled'  
        else:
            # Enable combobox
            self.Ending_node_combobox['state'] = 'normal'  

    def update_plot(self, with_labels=True):
        # Create a matplotlib figure
        self.fig = Figure(figsize=(3,3), dpi=200)
        self.ax = self.fig.add_subplot(111)

        # Drawing nodes of the graph
        nx.draw_networkx_nodes(self.game.G, self.game.node_position, ax=self.ax, node_size=150)
        nx.draw_networkx_labels(self.game.G, self.game.node_position, ax=self.ax, font_size=10)

        # Draw edges of the nodes and set the width of each edge to be proportional to its weight
        edge_width = list(nx.get_edge_attributes(self.game.G, 'weight').values())
        nx.draw_networkx_edges(self.game.G, self.game.node_position, alpha=0.5, ax=self.ax, width=edge_width)
        
        # If the labels exist - draw them
        if with_labels:
            edge_labels = nx.get_edge_attributes(self.game.G, 'weight')
            nx.draw_networkx_edge_labels(self.game.G, self.game.node_position, edge_labels)
    
        # Draw the figure on the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw() 
        self.canvas.get_tk_widget().place(relx=0.33, rely=0.60, anchor='center', width=600, height=500)
    
    def Bet_Start_Game(self):
        
        # Create the variable that states if all parameters are selected
        all_inputs_valid = True

        # Get the value of the bid 
        bid_amount = self.bid_scale.get()

        # Check if the bid amount is higher that zero, if it is zero, paint the label red
        if bid_amount == 0:
            self.Bid_Label.config(fg='red')
            all_inputs_valid = False
        else:
            self.Bid_Label.config(fg='black')

        # Check if the starting noded was selected, if it not, paint the label red
        starting_node = self.Starting_node_combobox.get()
        if not starting_node:
            self.Starting_node_combobox_Label.config(fg='red')
            all_inputs_valid = False
        else:
            self.Starting_node_combobox_Label.config(fg='black')
            self.game.set_starting_node(int(starting_node))

        # Check if the ending node was selected and get its value
        ending_node = self.Ending_node_combobox.get()

        # Check if the ending noded was selected, if it not, paint the label red
        if not ending_node:
            self.Ending_node_combobox_Label.config(fg='red')
            all_inputs_valid = False
        else:
            self.Ending_node_combobox_Label.config(fg='black')
            self.game.set_ending_node(int(ending_node))

        # If all inputs are valid -> proceed with the game logic
        if all_inputs_valid:
            self.game.set_base_score(bid_amount)
            self.game.generate_cutoff()
            self.game.calculate_node_scores()

            
            print(self.game.check_player_wins())
            print(self.game.get_player_score())

            if(self.game.check_player_wins() == True):
                self.parent.switch_frame('play', 'win')
            else:
                self.parent.switch_frame('play', 'lose')
        


class Win(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        self.amount_of_winning = int(100)
        #Balance variable for putting into Label
        self.amount_of_winning_variable = tk.StringVar()
        self.amount_of_winning_variable.set("Amount of winning: " + str(self.amount_of_winning))

        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png")
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button
        self.back_button = tk.Button(self, command=lambda: parent.switch_frame('win', 'play'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)


        # Put the back arrow image for the button
        self.win_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/win_picture.png")
        # Make the image 10 times smaller
        self.win_image = self.win_image.subsample(3, 3) 
        
        # Place the picture as a Label
        self.win_label_picture = tk.Label(self, image=self.win_image)
        self.win_label_picture.place(relx= 0.5, rely = 0.5, anchor='center')  
    
        self.you_won_label = tk.Label(self, text="YOU WON!!!", font = 'Helvetica, 50', bg = 'white')
        self.you_won_label.place(relx=0.5, rely=0.1, anchor='center')
        
        self.amount_of_winning_label = tk.Label(self, textvariable=self.amount_of_winning_variable, 
                                                font='Helvetica, 30',
                                                bg = 'white')
        self.amount_of_winning_label.place(relx= 0.5, rely= 0.88, anchor='center')

class Lose(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        self.amount_of_lose = int(100)
        #Balance variable for putting into Label
        self.amount_of_lose_variable = tk.StringVar()
        self.amount_of_lose_variable.set("You lost: " + str(self.amount_of_lose))

        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png")
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button
        self.back_button = tk.Button(self, command=lambda: parent.switch_frame('lose', 'play'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)


        # Put the back arrow image for the button
        self.lose_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/Loose_picture.png")
        # Make the image 10 times smaller
        self.lose_image = self.lose_image.subsample(3, 3) 
        
        # Place the picture as a Label
        self.lose_label_picture = tk.Label(self, image=self.lose_image)
        self.lose_label_picture.place(relx= 0.5, rely = 0.5, anchor='center')  
    
        self.you_lost_label = tk.Label(self, text="you lost):", font = 'Helvetica, 50', bg = 'white')
        self.you_lost_label.place(relx=0.5, rely=0.1, anchor='center')
        
        self.amount_of_loosing_label = tk.Label(self, textvariable=self.amount_of_lose_variable, 
                                                font='Helvetica, 30',
                                                bg = 'white')
        self.amount_of_loosing_label.place(relx= 0.5, rely= 0.88, anchor='center')

if __name__ == '__main__':
    app = GraphGameGUI()
    app.mainloop()