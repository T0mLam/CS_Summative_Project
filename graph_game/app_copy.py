import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
import networkx as nx
import pygame
import tkinter as tk
from tkinter import messagebox, ttk

from .db.database import authenticate, initialize_database, register_player, update_balance
from .game_logic import GraphGame
from .search_engine.search_engine import SearchEngine
# To run app.py, enter 'python3 -m graph_game.app_copy' in terminal.


class GraphGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Graph Game')
        self.geometry('800x600')
        self['bg'] = 'white'
        # Make the window resizable
        self.resizable(False, False)  

        # Initialize the database
        initialize_database()

        # Create a variable for storing the current player and their score
        self.current_player = None
        self.current_balance = None

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
            'register': Register(self),
            'leaderboard' : Leaderboard(self)
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
        
        self.register_Button = tk.Button(self, text='Register', font='Helvetica 30', bg='white', command=lambda: self.parent.switch_frame('login', 'register'))
        self.register_Button.place(relx=0.5, rely=0.5, anchor='center')

        self.login_Button = tk.Button(self, text='Login', font='Helvetica 30', bg='white', command=self.login)
        self.login_Button.place(relx=0.5, rely=0.6, anchor='center')

    def login(self):
        username = self.username_Entry.get()    
        password = self.password_Entry.get()
        user = authenticate(username, password)
        if user:
            name, balance = user
            self.parent.current_player = name
            self.parent.current_balance = balance
            self.parent.switch_frame('login', 'menu')
        else:
            messagebox.showinfo("Error", "The player is not found.")


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

        self.login_Button = tk.Button(self, text='Login', font='Helvetica 30', bg='white', command=lambda: self.parent.switch_frame('register', 'login'))
        self.login_Button.place(relx=0.5, rely=0.7, anchor='center')
        
    def register(self):
        username = self.username_Entry.get()
        password = self.password_Entry.get()
        password_repeat = self.password_repeat_Entry.get()
        if not username or not password or not password_repeat:
            messagebox.showinfo("Error", "Please fill in all the information.")
            return
        if password == password_repeat:
            register_player(username, password, 100)
            self.parent.current_player = username
            self.parent.current_balance = 100
            self.parent.switch_frame('register', 'menu')
        else:
            messagebox.showinfo("Error", "Passwords do not match.")

        
class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")
        self.parent = parent

        # Play button
        play_button = tk.Button(self, text="Play", command=lambda: self.parent.switch_frame('menu', 'play')
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

        # Leaderboard Button
        leaderboard_button = tk.Button(self, text='Leaderboard', bg='white', fg='black',
                                     font='Helvetica, 40', width=10,
                                     command = lambda: self.parent.switch_frame('menu', 'leaderboard'))
        # command=self.show_leaderboard_frame)
        leaderboard_button.place(relx=0.5, rely=0.6, anchor='center')

        # Quit Button
        logout_button = tk.Button(self, text='Logout', command=lambda: self.parent.switch_frame('menu', 'login'), bg='white', fg='black', font='Helvetica, 40', width=10)
        # command=self.master.quit)
        logout_button.place(relx=0.5, rely=0.75, anchor='center')

        # Soundtrack Switch
        soundtrack_switch = tk.Checkbutton(self, text='Music', var=self.parent.soundtrack_state,
                                           command=self.parent.switch_soundtrack,
                                           onvalue=True, offvalue=False,
                                           bg='white', font='Helvetica, 20')
        soundtrack_switch.place(relx=0.93, rely=0.95, anchor='center')


class Leaderboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.search_engine = SearchEngine()
        self.players = self.search_engine.get_leaders(100)  # Get all players initially

        # Set the background color to white
        self.configure(bg="white")

        # Title
        leaderboard_label = tk.Label(self, text="Leaderboard", font=('Helvetica', 60), bg='white')
        leaderboard_label.place(relx=0.5, rely=0.12, anchor='center')

        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png")
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button 
        self.back_button = tk.Button(self, command=lambda: self.parent.switch_frame('leaderboard', 'menu'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Search Entry
        self.search_entry = tk.Entry(self, font=('Helvetica', 30))
        self.search_entry.insert(0, "Search")
        # Place the search text inside the Entry if the user does not use it 
        self.search_entry.bind("<FocusIn>", self.Text_search_if_empty)
        self.search_entry.bind("<FocusOut>", self.Text_search_if_empty_focus_out)
        # Bind the command to the entry if the key is released 
        self.search_entry.bind("<KeyRelease>", self.Searching)  
        self.search_entry.pack(side="top", padx=20, pady=(40, 0))

        # Leaderboard Table: 

        # Create a treeview widget for the table
        self.tree = ttk.Treeview(self, columns=("Place", "Name", "Score"), show="headings")
        self.tree.pack(side="top", pady=(30, 0))

        # Add Column headings
        self.tree.heading("Place", text="Place", anchor=tk.CENTER)
        self.tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree.heading("Score", text="Score", anchor=tk.CENTER)

        # Change the width of rows
        self.tree.column("Place", width=100, anchor=tk.CENTER)
        self.tree.column("Name", width=400, anchor=tk.CENTER)
        self.tree.column("Score", width=150, anchor=tk.CENTER)

        # Set font size and row height for the table
        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Helvetica', 30), rowheight=40)
        self.style.configure("Treeview.Heading", font=('Helvetica', 30),rowheight=40)
        self.style.configure("Treeview.Row", font=('Helvetica', 30), rowheight=40)

        # Add scrollbars if there are too much columns
        self.y_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.y_scrollbar.pack(side="right", fill="y")
        self.x_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.x_scrollbar.pack(side="bottom", fill="x")

        # Set scrollbars to the table
        self.tree.configure(yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)

        # Call the function to set the values in the table
        self.update_treeview()

    def update_treeview(self):
        # Delete all previous data in the treeview
        self.tree.delete(*self.tree.get_children())
        # Populate the treeview with all players initially
        for i, row in enumerate(self.players):
            self.tree.insert("", "end", values=(i + 1, *row), tags=("Treeview.Row", "Treeview", "Treeview.Heading"))

    def Text_search_if_empty(self, event):
        if self.search_entry.get() == "Search":
            self.search_entry.delete(0, tk.END)

    def Text_search_if_empty_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search")

    def Searching(self, event):
        # Set the search text to lower letters for a more comfortabel search
        search_text = self.search_entry.get().strip().lower()
        # If the search is empty, show all players 
        if not search_text or search_text == "search": 
            self.players = self.search_engine.get_leaders(100)
        else:
            # Show the only players whose name starts with the letters in the search_entry
            self.players = [player for player in self.search_engine.get_leaders(100) if player[0].lower().startswith(search_text)]
        # Update the table to see changes
        self.update_treeview()



class Play(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.game = GraphGame.random_start()
        self.game.set_base_score(100)

        # The variable for new game
        self.game_started = True

        self.configure(bg="white")

        # generated_distance_variable for putting into Label
        self.generated_distance_variable = tk.StringVar()
        self.generated_distance_variable.set("Generated distance: -")

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
        self.balance_label = tk.Label(self, text='', bg='white', fg='black', font='Helvetica, 20')
        self.balance_label.place(relx=0.8, rely=0.05, anchor='center')
        self.update_balance_label()

        # Label Bid before the scale
        self.bid_label = tk.Label(self, text = "Bid:", bg='white', fg='black',
                             font='Helvetica, 20')
        self.bid_label.place(relx=0.76, rely=0.35, anchor='center')

        # Scale with changing the bid
        self.bid_scale = tk.Scale(self, from_=0, to=self.parent.current_balance, orient=tk.HORIZONTAL,
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
        self.starting_node_combobox_label = tk.Label(self, text="Starting node:", bg='white', fg='black',
                                    font='Helvetica, 20')
        self.starting_node_combobox_label.place(relx=0.81, rely=0.46, anchor='center')

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

    def update_balance_label(self):
        self.balance_label.config(text="Balance: " + str(self.parent.current_balance))
        self.balance_label.after(1000, self.update_balance_label)

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
        self.bid_scale.config(to=self.parent.current_balance)

    def bet_start_game(self):
        if self.game_started == True:
            # Create the variable that states if all parameters are selected
            all_inputs_valid = True

            # Get the value of the bid 
            bid_amount = self.bid_scale.get()

            # Check if the bid amount is higher that zero, if it is zero, paint the label red
            if bid_amount == 0:
                self.bid_label.config(fg='red')
                all_inputs_valid = False
            else:
                self.bid_label.config(fg='black')

            # Check if the starting noded was selected, if it not, paint the label red
            starting_node = self.starting_node_combobox.get()
            if (not starting_node 
                or self.starting_node_combobox.get() == self.ending_node_combobox):
                self.starting_node_combobox_label.config(fg='red')
                all_inputs_valid = False
            else:
                self.starting_node_combobox_label.config(fg='black')

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
            
            self.parent.current_balance += score
            # Update player's balance in db ...
            update_balance(self.parent.current_player, self.parent.current_balance)

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

        self.update_max_bid()
            

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
        
        self.amount_of_losing_label = tk.Label(self, textvariable=self.amount_of_lose_variable, 
                                                font='Helvetica, 30',
                                                bg = 'white')
        self.amount_of_losing_label.place(relx= 0.5, rely= 0.88, anchor='center')


# To run app.py, enter 'python3 -m graph_game.app' in terminal.
if __name__ == '__main__':
    app = GraphGameGUI()
    app.mainloop()