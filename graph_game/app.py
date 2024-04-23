import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx
import pygame
import tkinter as tk
from tkinter import messagebox, ttk

from .database.database import authenticate, get_player_history, initialize_database, log_game, registered, register_player, update_balance
from .game.game_logic import GraphGame
from .game.search_engine import SearchEngine
# To run app.py, enter 'python3 -m graph_game.app' in terminal.


class GraphGameGUI(tk.Tk):
    """The graphical user interface of the game."""
    def __init__(self):
        super().__init__()
        self.title('Graph Game')
        self.geometry('800x600')
        self['bg'] = 'white'

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

        # Create the variable for controlling the music (stop or play)
        self.soundtrack_state = tk.BooleanVar(value=True)

        # Create a frame dict
        self.frames = {
            'menu': MainMenu(self),
            'play': Play(self),
            'win': Win(self),
            'lose': Lose(self),
            'login': Login(self),
            'register': Register(self),
            'leaderboard' : Leaderboard(self),
            'history' : PlayerHistory(self)
        }

        # Show main menu frame
        self.frames['login'].pack(fill='both', expand=True)

    def switch_soundtrack(self):
        """The method that pauses and unpauses the music according to the soundtrack_state variable."""
        if self.soundtrack_state.get():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def switch_frame(self, current_frame, new_frame):
        """The method for navigating between frames."""
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
    """The login page."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Change the color of the background to white
        self.configure(bg="white")
        
        # Title of the login page
        title = tk.Label(self, text="Login", font=('Helvetica', 60), bg='white')
        title.place(relx=0.5, rely=0.12, anchor='center')

        # Username label
        self.username_Label = tk.Label(self, text="Username:", font='Helvetica 30', bg='white')
        self.username_Label.place(relx=0.2, rely=0.3, anchor='center')
        # Username entry
        self.username_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white')
        self.username_Entry.place(relx=0.5, rely=0.3, anchor='center')

        # Password label
        self.password_Label = tk.Label(self, text="Password:", font='Helvetica 30', bg='white')
        self.password_Label.place(relx=0.2, rely=0.4, anchor='center')
        # Password entry
        self.password_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white', show='*')
        self.password_Entry.place(relx=0.5, rely=0.4, anchor='center')
        
        # Show register page button
        self.register_Button = tk.Button(self, text='Register', font='Helvetica 30', bg='white', command=lambda: self.parent.switch_frame('login', 'register'))
        self.register_Button.place(relx=0.5, rely=0.5, anchor='center')

        # Login button
        self.login_Button = tk.Button(self, text='Login', font='Helvetica 30', bg='white', command=self.login)
        self.login_Button.place(relx=0.5, rely=0.6, anchor='center')

    def login(self):
        """A method for login authentication."""
        # Get the username from the entry box
        username = self.username_Entry.get() 
        # Get the password from the entry box   
        password = self.password_Entry.get()
        # Authenticate the player
        user = authenticate(username, password)
        if user:
            # Fetch the name and balance from the database
            name, balance = user
            self.parent.current_player = name
            self.parent.current_balance = balance
            self.parent.frames['play'].restart_game()
            # Load the player's history from the db
            self.parent.frames['history'].load_player_history()
            # Update the max bid in the Play Frame
            self.parent.frames['play'].update_max_bid()
            # Switch the frame from login to the menu
            self.parent.switch_frame('login', 'menu')
        else:
            # Show the error if the player was not found
            messagebox.showinfo("Error", "The player is not found.")


class Register(tk.Frame):
    """The register page."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Change the color of the background for white
        self.configure(bg="white")
        
        # The title of the register page
        title = tk.Label(self, text="Register", font=('Helvetica', 60), bg='white')
        title.place(relx=0.5, rely=0.12, anchor='center')

        # Username label
        self.username_Label = tk.Label(self, text="Username:", font='Helvetica 30', bg='white')
        self.username_Label.place(relx=0.2, rely=0.3, anchor='center')
        # Username entry
        self.username_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white')
        self.username_Entry.place(relx=0.5, rely=0.3, anchor='center')

        # Password label
        self.password_Label = tk.Label(self, text="Password:", font='Helvetica 30', bg='white')
        self.password_Label.place(relx=0.2, rely=0.4, anchor='center')
        # Password entry
        self.password_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white', show='*')
        self.password_Entry.place(relx=0.5, rely=0.4, anchor='center')
        
        # Repeat password label
        self.password_repeat_Label = tk.Label(self, text="Repeat:", font='Helvetica 30', bg='white')
        self.password_repeat_Label.place(relx=0.22, rely=0.5, anchor='center')
        # Repeat password entry
        self.password_repeat_Entry = tk.Entry(self, font='Helvetica, 30', width=15, bg='white', show='*')
        self.password_repeat_Entry.place(relx=0.5, rely=0.5, anchor='center')

        # Register button
        self.register_Button = tk.Button(self, text='Register', font='Helvetica 30', bg='white', command=self.register)
        self.register_Button.place(relx=0.5, rely=0.6, anchor='center')

        # Login page button
        self.login_Button = tk.Button(self, text='Login', font='Helvetica 30', bg='white', command=lambda: parent.switch_frame('register', 'login'))
        self.login_Button.pack(pady=(0,160),side=tk.BOTTOM)
        
    def register(self):
        """A method for registering the player."""
        # Get the user name, password and password repeat entry
        username = self.username_Entry.get()
        password = self.password_Entry.get()
        password_repeat = self.password_repeat_Entry.get()

        # Check whether the entry boxes are filled in.
        if not username or not password or not password_repeat:
            messagebox.showinfo("Error", "Please fill in all the information.")
            return
        
        # Check if the passwords in the two entry boxes are the same
        if password == password_repeat:
            if registered(username):
                messagebox.showinfo("Error", "The account has been registered.")
                return 

            # Register player with its username, password and starting balance 100
            register_player(username, password, 100)
            self.parent.current_player = username
            self.parent.current_balance = 100

            # Update the leaderboard
            self.parent.frames['leaderboard'].search_engine.fetch_all_users_to_trie()
            self.parent.frames['leaderboard'].update_all_players()
            self.parent.switch_frame('register', 'menu')

            self.parent.frames['play'].restart_game()
            # Load the player's history from the db
            self.parent.frames['history'].load_player_history()
            # Update the max bid in the Play Frame
            self.parent.frames['play'].update_max_bid()
        else:
            # Raise an error if the passwords do not match
            messagebox.showinfo("Error", "Passwords do not match.")

        
class MainMenu(tk.Frame):
    """The main menu page."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Change the color of the background for white  
        self.configure(bg="white")

        # Title
        title = tk.Label(self, text="Graph Game", font=('Helvetica', 60), bg='white')
        title.pack(pady=(50,20),side=tk.TOP)

        # Play button
        play_button = tk.Button(self, text="Play", command=lambda: self.parent.switch_frame('menu', 'play'),
                                bg='white', fg='black', font='Helvetica, 40', width=10)
        play_button.pack(pady = 10, side = tk.TOP)

        # How to play button
        history_Button = tk.Button(self, text='History', bg='white', fg='black',
                                   font='Helvetica, 40', width=10,
                                   command=lambda: self.parent.switch_frame('menu', 'history'))
        history_Button.pack(pady= 10)

        # Leaderboard button
        leaderboard_button = tk.Button(self, text='Leaderboard', bg='white', fg='black',
                                       font='Helvetica, 40', width=10,
                                       command=lambda: self.parent.switch_frame('menu', 'leaderboard'))
        leaderboard_button.pack(pady=10)

        # Quit button
        logout_button = tk.Button(self, text='Logout', command=lambda: self.parent.switch_frame('menu', 'login'),
                                  bg='white', fg='black', font='Helvetica, 40', width=10)
        logout_button.pack(pady=10)

        # Soundtrack switch
        soundtrack_switch = tk.Checkbutton(self, text='Music', var=self.parent.soundtrack_state,
                                            command=self.parent.switch_soundtrack,
                                            onvalue=True, offvalue=False,
                                            bg='white', font='Helvetica, 20')
        soundtrack_switch.place(relx=0.93, rely=0.95, anchor='center')


class Leaderboard(tk.Frame):
    """The leaderboard page which displays the player rank and their balances."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Create an instance of the SearchEngine class
        self.search_engine = SearchEngine()
        # Get 100 top players from the database
        self.players = self.search_engine.get_leaders(100)  

        # Set the background color to white
        self.configure(bg="white")

        # Title for the leaderboard page
        leaderboard_label = tk.Label(self, text="Leaderboard", font=('Helvetica', 60), bg='white')
        leaderboard_label.place(relx=0.5, rely=0.12, anchor='center')

        # The back arrow image for the return button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png", master=self)
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Return button 
        self.back_button = tk.Button(self, command=lambda: self.parent.switch_frame('leaderboard', 'menu'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Recommended words for the search entry combobox
        self.words_for_autocompletion = []
        # Search entry combobox
        self.search_entry = ttk.Combobox(self, values=self.words_for_autocompletion) 
        self.search_entry.bind("<FocusIn>", self.text_search_if_empty)  
        self.search_entry.bind("<FocusOut>", self.text_search_if_empty_focus_out)
        # Bind the command to the entry if the key is released 
        self.search_entry.bind("<KeyRelease>", self.searching)
        self.search_entry.pack(side="top", padx=20, pady=(40, 0))  

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

    def update_all_players(self):
        # Update all players in the treeview
        self.players = self.search_engine.get_leaders(100)
        self.update_treeview()

    def update_treeview(self):
        # Delete all previous data in the treeview
        self.tree.delete(*self.tree.get_children())
        # Populate the treeview with all players initially
        for i, row in enumerate(self.players):
            self.tree.insert("", "end", values=(i + 1, *row), tags=("Treeview.Row", "Treeview", "Treeview.Heading"))

    def text_search_if_empty(self, event):
        # If the entry box is empty, put the search text
        if self.search_entry.get() == "Search":
            self.search_entry.delete(0, tk.END)

    def text_search_if_empty_focus_out(self, event):
        # Always put the search text in the entry even if user stopped using the entry box
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search")

    def searching(self, event):
        # Get the text from the text entry
        search_text = self.search_entry.get().strip()
        # Search for the list of words for autocompletion
        self.words_for_autocompletion = self.search_engine.complete_search(search_text)
        self.search_entry.config(values=self.words_for_autocompletion[:5])
    
        if not search_text or search_text == "search": 
            # If the search is empty, show all players 
            self.players = self.search_engine.get_leaders(100)
        else:
            # Show the only players whose name starts with the letters in the search_entry
            self.players = self.search_engine.search_results(search_text)   
        # Update the table to see the changes
        self.update_treeview()


class PlayerHistory(tk.Frame):
    """The player history page which displays the previous game records of the player."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Set the background color to white        
        self.configure(bg="white")
        
        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png", master=self)
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button 
        self.back_button = tk.Button(self, command=lambda: self.parent.switch_frame('history', 'menu'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # History Label
        self.history_label = tk.Label(self, text="History", font="Helvetica 60", background="white")
        self.history_label.place(relx=0.5, rely=0.05, anchor='center')
    
        # Create the treeview for storing the history of the player
        self.history_tree = ttk.Treeview(self, columns=("Bid", "Start Node", "End Node", "Outcome", "Score", "Date"), 
                                         show="headings")
        
        # Set column headings
        self.history_tree.heading("Bid", text="Bid")
        self.history_tree.heading("Start Node", text="Starting Node")
        self.history_tree.heading("End Node", text="Ending Node")
        self.history_tree.heading("Outcome", text="Outcome")
        self.history_tree.heading("Score", text="Score")
        self.history_tree.heading("Date", text="Date")
        
        # Set column widths
        self.history_tree.column("Bid", width=40)
        self.history_tree.column("Start Node", width=100)
        self.history_tree.column("End Node", width=80)
        self.history_tree.column("Outcome", width=50)
        self.history_tree.column("Score", width=20)
        self.history_tree.column("Date", width=150)
        
        # Change the font size 
        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Helvetica', 20))
        self.style.configure("Treeview.Heading", font=('Helvetica', 20))
        self.style.configure("Treeview.Row", font=('Helvetica', 20))

        # Add scrollbar
        self.history_tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=self.history_tree_scrollbar.set)
        
        self.history_tree.pack(side="top", padx=10, pady=10, fill="both", expand=True)
        self.history_tree_scrollbar.pack(side="right", fill="y")

    def load_player_history(self):
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get player history
        history = get_player_history(self.parent.current_player) 
        if history:
            # Insert history into treeview
            for bid, start, end, outcome, score, date in history:
                self.history_tree.insert("", "end", values=(bid, start, end, outcome, score, date))
    
    
class Play(tk.Frame):
    """The page for the gameplay.

    The player first set the bid amount.
    Then select the starting node out of the existing nodes, generated in the graph.
    After that player selects the ending node and clicks BET.
    
    If the player won - > Go to the winning frame.
    If the player lost - > Go to the losing frame.
    If the player did not select all the options - > The game will not start.
    When the player came back from the winning or loosing frame - > disable the widgets and 
    show the direction from the first node to the last.
    If the player score is lower than 1 - > Give him extra 50 score.
    
    Set the player bid, starting node, ending node, score, win or lose and entry date to the history.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.game = GraphGame.random_start()

        # The variable for new game
        self.game_started = True

        self.configure(bg="white")

        # generated_distance_variable for putting into Label
        self.generated_distance_variable = tk.StringVar()
        self.generated_distance_variable.set("Generated distance: -")

        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png", master=self)
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button 
        self.back_button = tk.Button(self, command=lambda: parent.switch_frame('play', 'menu'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)

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
        self.bet_button.pack(padx = (550,0), pady= (0,30), side = tk.BOTTOM)

        self.canvas = tk.Canvas(self, width=530, height=480, bg="white")
        self.canvas.place(relx=0.34, rely=0.59, anchor='center')

        self.update_plot()

    def update_balance_label(self):
        self.balance_label.config(text="Balance: " + str(self.parent.current_balance))
        self.balance_label.after(1000, self.update_balance_label)

    def update_bid_scale_combobox_state(self, event=None):
        """The method, which does not let the player choose the ending node if the starting was not chosen."""
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
        """Method makes ending node combobox disabled if starting node combobox is not chosen."""
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

    def update_plot(self, with_node_scores=False, result=False):
        """Update the graph each round of the game."""
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
            
            # Expand the graph to accomodate the score labels
            self.ax.set_ylim(tuple(i*1.2 for i in self.ax.get_ylim()))
        
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

    def restart_game(self):
        """Re-generate a new game and clean up previous entries."""
        # Start the new game
        self.game = GraphGame.random_start()
        self.update_plot(result=False)  
        self.game_started = True

        # Make the starting and ending node entry disabled as the bid has not been chosen
        self.starting_node_combobox['state'] = 'disabled'
        self.ending_node_combobox['state'] = 'disabled'

        # Enable the bid scale
        self.bid_scale['state'] = 'normal' 

        # Update the values of starting end ending node comboboxes as there is a new graph  
        self.starting_node_combobox['values'] = self.game.get_nodes()
        self.ending_node_combobox['values'] = self.game.get_nodes()

        # Clear the values of the comboboxes
        self.starting_node_combobox.set('') 
        self.ending_node_combobox.set('')  
        self.bid_scale.set(0)

        # Change the text of the bet button to BET
        self.bet_button.config(text="BET")
        self.bet_button.update()

        # Update the generated distance label of the game 
        self.generated_distance_variable.set('Generated distance: -')        

        # Check if the player balance is less than one and give the player extra points
        if(self.parent.current_balance < 1):
            # Raise an alert
            tk.messagebox.showinfo(title="Broke", message="Your balance is less than 1, here are 50 extra score")
            # Update the new score in the database and in game
            update_balance(self.parent.current_player, 50)
            self.parent.current_balance = 50

    def bet_start_game(self):
        """A method that gets the input nodes and bid after the bet button was pressed and handle the play again button press."""
        if self.game_started:
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

                # Check if the player wins
                if(self.game.check_player_wins()):
                    # Set the amount of winning label
                    self.parent.frames['win'].amount_of_winning_variable.set("Amount of winning: " + str(score))
                    # Go to the winning frame
                    self.parent.switch_frame('play', 'win')
                else:
                    score*=-1
                    # Set the amount of losing label
                    self.parent.frames['lose'].amount_of_lose_variable.set("You lost: " + str(score)) 
                    score*=-1
                    # Go to the losing frame
                    self.parent.switch_frame('play', 'lose')

            # Update the graph to see the results
            self.update_plot(result=True, with_node_scores=True)

             # Set the variable of the game state to False to make the game finished
            self.game_started = False

            # Change the bet button text to play again
            self.bet_button.config(text="Play Again")
            self.bet_button.update()

            # Disable the widgets and clear their values
            self.starting_node_combobox['state'] = 'disabled'
            self.ending_node_combobox['state'] = 'disabled'
            self.starting_node_combobox.set('') 
            self.ending_node_combobox.set('')
            self.bid_scale.set(0)
            self.bid_scale['state'] = 'disabled' 

            # Update the generated distance label of the game 
            self.generated_distance_variable.set('Generated distance: ' + str(self.game.cutoff_distance))
            
            self.parent.current_balance += score
            # Update player's balance in db ...
            update_balance(self.parent.current_player, self.parent.current_balance)

            # Update the leaderboard
            self.parent.frames['leaderboard'].searching(event=None)
        

            # Record the game to the history
            outcome = 'win' if self.game.check_player_wins() else 'loss'
            log_game(self.parent.current_player, int(bid_amount), int(starting_node), int(ending_node), outcome, score)

            # Update the player history
            self.parent.frames['history'].load_player_history()

        else:
            self.restart_game()
            
            # Update the max value of the bid scale
            self.update_max_bid()


class Win(tk.Frame):
    """The winning page which displays the amount that the player wins."""
    def __init__(self, parent):
        super().__init__(parent)
        # Change the background color to white
        self.configure(bg="white")

        # Balance variable for putting into Label
        self.amount_of_winning_variable = tk.StringVar()
        self.amount_of_winning_variable.set("Amount of winning: " + str(self.amount_of_winning_variable))

        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png", master=self)
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button
        self.back_button = tk.Button(self, command=lambda: parent.switch_frame('win', 'play'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)


        # Put the back arrow image for the button
        self.win_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/win_picture.png", master=self)
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
    """The lose page which displays the amount that the player loses."""
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        #Balance variable for putting into Label
        self.amount_of_lose_variable = tk.StringVar()
        self.amount_of_lose_variable.set("You lost: " + str(self.amount_of_lose_variable))

        # Put the back arrow image for the button
        self.back_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/back_arrow.png", master=self)
        # Make the image 10 times smaller
        self.resized_back_image = self.back_image.subsample(10, 10) 
        # Back Button
        self.back_button = tk.Button(self, command=lambda: parent.switch_frame('lose', 'play'),
                             image=self.resized_back_image, background="white")
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Put the back arrow image for the button
        self.lose_image = tk.PhotoImage(file=os.path.dirname(__file__) + "/images/Loose_picture.png", master=self)
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


if __name__ == '__main__':
    app = GraphGameGUI()
    app.mainloop()