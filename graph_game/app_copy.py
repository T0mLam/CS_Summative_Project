import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
import networkx as nx
import pygame
import tkinter as tk
from tkinter import ttk

from .db.database import DatabaseConnection, authenticate, initialize_database, log_game, register_player
from .game_logic import GraphGame
# To run app.py, enter 'python3 -m graph_game.app_copy' in terminal.


class GraphGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Graph Game')
        self.geometry('800x600')
        self['bg'] = 'white'
        self.resizable(False, False)  # Make the window resizable

        # Initialize the database
        initialize_database()

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
            'lose': Lose(self),
            'login': Login(self),
            'register': Register(self)
        }

        # Show main menu frame
        self.frames['login'].pack(fill='both', expand=True)

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
        

class Login(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="white")
        
        title = tk.Label(self, text="Graph Game", font=('Helvetica', 60), bg='white')
        title.place(relx=0.5, rely=0.12, anchor='center')

        self.username_Label = tk.Label(self, text="Username:", font='Helvetica 30', bg='white')
        self.username_Label.place(relx=0.2, rely=0.3, anchor='center')
        self.username_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white')
        self.username_Entry.place(relx=0.5, rely=0.3, anchor='center')

        self.password_Label = tk.Label(self, text="Password:", font='Helvetica 30', bg='white')
        self.password_Label.place(relx=0.2, rely=0.4, anchor='center')
        self.password_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white', show='*')
        self.password_Entry.place(relx=0.5, rely=0.4, anchor='center')
        
        self.register_Button = tk.Button(self, text='Register', font='Helvetica 30', bg='white', command=lambda: parent.switch_frame('login', 'register'))
        self.register_Button.place(relx=0.5, rely=0.5, anchor='center')

        self.login_Button = tk.Button(self, text='Login', font='Helvetica 30', bg='white', command=self.login)
        self.login_Button.place(relx=0.5, rely=0.6, anchor='center')

    def login(self):
        username = self.username_Entry.get()
        password = self.password_Entry.get()
        user = authenticate(username, password)
        if user:
            self.parent.switch_frame('login', 'menu')


class Register(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="white")
        
        title = tk.Label(self, text="Register", font=('Helvetica', 60), bg='white')
        title.place(relx=0.5, rely=0.12, anchor='center')

        self.username_Label = tk.Label(self, text="Username:", font='Helvetica 30', bg='white')
        self.username_Label.place(relx=0.2, rely=0.3, anchor='center')
        self.username_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white')
        self.username_Entry.place(relx=0.5, rely=0.3, anchor='center')

        self.password_Label = tk.Label(self, text="Password:", font='Helvetica 30', bg='white')
        self.password_Label.place(relx=0.2, rely=0.4, anchor='center')
        self.password_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white', show='*')
        self.password_Entry.place(relx=0.5, rely=0.4, anchor='center')
        
        self.password_repeat_Label = tk.Label(self, text="Repeat:", font='Helvetica 30', bg='white')
        self.password_repeat_Label.place(relx=0.22, rely=0.5, anchor='center')
        self.password_repeat_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white', show='*')
        self.password_repeat_Entry.place(relx=0.5, rely=0.5, anchor='center')

        self.register_Button = tk.Button(self, text='Register', font='Helvetica 30', bg='white', command=self.register)
        self.register_Button.place(relx=0.5, rely=0.6, anchor='center')

        self.login_Button = tk.Button(self, text='Login', font='Helvetica 30', bg='white', command=lambda: parent.switch_frame('register', 'login'))
        self.login_Button.place(relx=0.5, rely=0.7, anchor='center')
        
    def register(self):
        username = self.username_Entry.get()
        password = self.password_Entry.get()
        password_repeat = self.password_repeat_Entry.get()
        if password == password_repeat:
            register_player(username, password, 0)
            self.parent.switch_frame('register', 'menu')
        else:
            print("Passwords do not match.")

        
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

        # The variable for new game
        self.game_started = True

        self.configure(bg="white")

        self.balance = int(100)
        # Balance variable for putting into Label
        self.balance_variable = tk.StringVar()
        self.balance_variable.set("Balance: " + str(self.balance))

        # generated_distance_variable for putting into Label
        self.generated_distance_variable = tk.StringVar()
        self.generated_distance_variable.set("Generated distance: -")

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
        self.Bid_Label.place(relx=0.76, rely=0.35, anchor='center')

        # Scale with changing the bid
        self.bid_scale = tk.Scale(self, from_=0, to=self.balance, orient=tk.HORIZONTAL,
                                  length=160,
                                  bg='white', fg='black',
                                  font = 'Helvetica, 20',
                                  )
        self.bid_scale.place(relx=0.89, rely=0.33, anchor='center')
         # Bind the method update_bid_scale_combobox_state to the combobox
        self.bid_scale.bind("<ButtonRelease-1>", self.update_bid_scale_combobox_state)

        # Starting node combobox
        self.starting_node_combobox = ttk.Combobox(self, width=5, state='disabled')
        # Fill the combobox with the values of the graph
        self.starting_node_combobox['values'] = self.game.get_nodes()
        self.starting_node_combobox.place(relx=0.94, rely=0.46, anchor='center')
        # Bind the method update_starting_ending_node_combobox_state to the combobox
        self.starting_node_combobox.bind("<<ComboboxSelected>>", self.update_starting_ending_node_combobox_state)
        # Bind the same method but as Focus Out to always check if the starting node combobox value was not deleted
        self.starting_node_combobox.bind("<FocusOut>", self.update_starting_ending_node_combobox_state)

        # Starting node combobox label
        self.Starting_node_combobox_Label = tk.Label(self, text="Starting node:", bg='white', fg='black',
                                    font='Helvetica, 20')
        self.Starting_node_combobox_Label.place(relx=0.81, rely=0.46, anchor='center')

        # Ending node combobox
        self.ending_node_combobox = ttk.Combobox(self, width=5, state='disabled')
        # Fill the combobox with the values of the graph
        self.ending_node_combobox['values'] = self.game.get_nodes()
        self.ending_node_combobox.place(relx=0.94, rely=0.57, anchor='center')

        # Ending node combobox label
        self.Ending_node_combobox_Label = tk.Label(self, text="Ending node:", bg='white', fg='black',
                                    font='Helvetica, 20')
        self.Ending_node_combobox_Label.place(relx=0.81, rely=0.57, anchor='center')

        # generated_distance_label with coefficient variable
        self.generated_distance_label = tk.Label(self, textvariable=self.generated_distance_variable, bg='white', font='Helvetica, 20')
        self.generated_distance_label.place(relx=0.86, rely=0.68, anchor='center')

        self.bet_button = tk.Button(self, text = "BET", bg = 'white', fg = 'black',
                               font='Helvetica, 25',
                               width=10,
                               command=self.bet_start_game)
        self.bet_button.place(relx=0.86, rely=0.9, anchor='center')

        self.canvas = tk.Canvas(self, width=530, height=480, bg="white")
        self.canvas.place(relx=0.34, rely=0.59, anchor='center')

        self.update_plot()

    def update_bid_scale_combobox_state(self, event=None):
        # Check if bid_scale node combobox is empty
        if not self.bid_scale.get():  
            # Delete starting node selection
            self.starting_node_combobox.set('')  
            # Disable the combobox
            self.starting_node_combobox['state'] = 'disabled'  
        else:
            # Enable starting_node combobox
            self.starting_node_combobox['state'] = 'normal'  
            # Disable bid_scale combobox
            self.bid_scale.configure(state='disabled')

            # Set the base score for the score generator
            base_score = self.bid_scale.get()
            self.game.set_base_score(int(base_score))
    
    def update_starting_ending_node_combobox_state(self, event=None):
        """Method makes ending node combobox disabled if starting node combobox is not chosen"""
        
        # Check if starting node combobox is empty
        if not self.starting_node_combobox.get():  
            # Delete ending node selection
            self.ending_node_combobox.set('')  
            # Disable the combobox
            self.ending_node_combobox['state'] = 'disabled'  
        else:
            # Enable ending_node combobox
            self.ending_node_combobox['state'] = 'normal'  
            # Disable starting_node combobox
            self.starting_node_combobox['state'] = 'disable' 

            # Set the starting node for the graph game
            starting_node = self.starting_node_combobox.get()
            self.game.set_starting_node(int(starting_node))

            # Update the plot with node scores
            self.game.generate_cutoff()
            self.update_plot(with_node_scores=True)

            # Update the generated distance label of the game 
            self.generated_distance_variable.set('Generated distance: ' + str(self.game.cutoff_distance))

    def update_plot(self, with_node_scores=False, result=False):
        # Create a matplotlib figure
        self.fig = Figure(figsize=(3,3), dpi=200)
        self.ax = self.fig.add_subplot(111)

        # Drawing nodes of the graph
        nx.draw_networkx_nodes(self.game.G, self.game.node_position, ax=self.ax, node_size=150)
        nx.draw_networkx_labels(self.game.G, self.game.node_position, ax=self.ax, font_size=10)

        # Draw edges of the nodes and set the width of each edge to be proportional to its weight
        edge_width = list(nx.get_edge_attributes(self.game.G, 'weight').values())
        nx.draw_networkx_edges(self.game.G, self.game.node_position, alpha=0.5, ax=self.ax, width=edge_width)

        if with_node_scores:
            if not self.game.starting_node or not self.game.score_generator:
                raise NameError('The score_generator or the starting node have not been defined.')

            # Get the shortest distances from the starting node to all other nodes
            node_to_dist = self.game.shortest_path(starting_node=self.game.starting_node)

            # Map the distance to each node to its score using the score_generator
            for node, dist in node_to_dist.items():
                node_to_dist[node] = self.game.score_generator.calculate_score(dist)

            # Create score labels for the networkx graph visualization
            label_pos = {}
            for node, coords in self.game.node_position.items():
                # Set the label to be 0.135 units above the original node position
                label_pos[node] = (coords[0], coords[1] + 0.135)

            nx.draw_networkx_labels(self.game.G, 
                                    pos=label_pos,
                                    ax=self.ax,
                                    labels=node_to_dist,
                                    font_size=4, 
                                    font_weight='bold')
        
        # If the labels exist - draw them
        if result:
            # Find the shortest distance between the starting node and the ending node
            shortest_dist = self.game.shortest_path(self.game.starting_node, self.game.ending_node)
        
            # Find all the nodes between the shortest path using the nx library
            path = nx.shortest_path(self.game.G, source=self.game.starting_node, target=self.game.ending_node)
            path_edges = list(zip(path,path[1:]))

            # Draw the edges between in green if the player wins, red otherwise
            if shortest_dist < self.game.cutoff_distance:
                nx.draw_networkx_edges(self.game.G, self.game.node_position, ax=self.ax, edgelist=path_edges, edge_color='g', width=3)
            else:
                nx.draw_networkx_edges(self.game.G, self.game.node_position, ax=self.ax, edgelist=path_edges, edge_color='r', width=3)

            edge_labels = nx.get_edge_attributes(self.game.G, 'weight')
            nx.draw_networkx_edge_labels(self.game.G, self.game.node_position, edge_labels, ax=self.ax, font_size=4)
            
        # Draw the figure on the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw() 
        self.canvas.get_tk_widget().place(relx=0.33, rely=0.60, anchor='center', width=600, height=500)

    # Function to update the maximum value of the bid scale
    def update_max_bid(self):
        self.bid_scale.config(to=self.balance)

    def bet_start_game(self):
        if self.game_started == True:
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
            starting_node = self.starting_node_combobox.get()
            if (not starting_node 
                or self.starting_node_combobox.get() == self.ending_node_combobox):
                self.Starting_node_combobox_Label.config(fg='red')
                all_inputs_valid = False
            else:
                self.Starting_node_combobox_Label.config(fg='black')

            # Check if the ending node was selected and get its value
            ending_node = self.ending_node_combobox.get()

            # Check if the ending noded was selected, if it not, paint the label red
            if( not ending_node 
               or self.starting_node_combobox.get() == self.ending_node_combobox.get()):
                self.Ending_node_combobox_Label.config(fg='red')
                all_inputs_valid = False
            else:
                self.Ending_node_combobox_Label.config(fg='black')
                self.game.set_ending_node(int(ending_node))

            # If all inputs are valid -> proceed with the game logic
            if all_inputs_valid:
                score = self.game.get_player_score()
                
                if(self.game.check_player_wins() == True):
                    self.parent.frames['win'].amount_of_winning_variable.set("Amount of winning: " + str(score))
                    self.parent.switch_frame('play', 'win')
                else:
                    score*=-1
                    self.parent.frames['lose'].amount_of_lose_variable.set("You lost: " + str(score)) 
                    score*=-1
                    self.parent.switch_frame('play', 'lose')

            self.update_plot(result=True, with_node_scores=True)
            self.game_started = False

            self.bet_button.config(text="Play Again")
            self.bet_button.update()

            self.starting_node_combobox['state'] = 'disabled'
            self.ending_node_combobox['state'] = 'disabled'
            self.starting_node_combobox.set('') 
            self.ending_node_combobox.set('')
            self.bid_scale.set(0)
            self.bid_scale['state'] = 'disabled' 
            
            self.balance += score

        else:
            self.bet_button.config(text="Play Again")
            self.game = GraphGame.random_start()
            self.update_plot(result=False)  
            self.game_started = True

            self.starting_node_combobox['state'] = 'disabled'
            self.bid_scale['state'] = 'normal' 

            self.starting_node_combobox['values'] = self.game.get_nodes()
            self.ending_node_combobox['values'] = self.game.get_nodes()

            self.starting_node_combobox.set('') 
            self.ending_node_combobox.set('')  
            self.bid_scale.set(0)

            self.ending_node_combobox['state'] = 'disabled'

            self.bid_scale.set(0)  

            self.bet_button.config(text="BET")
            self.bet_button.update()

            # Update the generated distance label of the game 
            self.generated_distance_variable.set('Generated distance: -')        

        self.balance_variable.set(f'Balance: {self.balance}')
        self.update_max_bid()
        # update ... user score in db
            

class Win(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        #Balance variable for putting into Label
        self.amount_of_winning_variable = tk.StringVar()
        self.amount_of_winning_variable.set("Amount of winning: " + str(self.amount_of_winning_variable))

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

        #Balance variable for putting into Label
        self.amount_of_lose_variable = tk.StringVar()
        self.amount_of_lose_variable.set("You lost: " + str(self.amount_of_lose_variable))

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


# To run app.py, enter 'python3 -m graph_game.app_copy' in terminal.
if __name__ == '__main__':
    app = GraphGameGUI()
    register_player("Artem123", "123", 100)
    app.mainloop()