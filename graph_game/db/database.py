import sqlite3  # Import the sqlite3 module for interacting with SQLite databases

class DatabaseConnection:
    """A context manager class for handling database connections."""
    
    def __init__(self, db_name):

        """Initialize the DatabaseConnection object."""
        self.db_name = db_name  # Store the name of the database file
        self.connection = None  # Initialize the connection attribute to None

    def __enter__(self):
        """Enter method for the context manager."""
        try:
            self.connection = sqlite3.connect(self.db_name)  # Establish a connection to the database
            return self.connection  # Return the database connection
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")  # Print an error message if connection fails
            raise  # Raise the exception to propagate it to the calling code
       
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method for the context manager."""
        if self.connection:  # Check if a connection exists
            try:
                self.connection.commit()  # Commit any changes to the database
            except sqlite3.Error as e:
                print(f"Error committing changes to database: {e}")  # Print an error message if commit fails
            finally:
                self.connection.close()  # Close the database connection, regardless of success or failure

    def initialize_database(db_name):
        """
        Initialize the database with necessary tables.
        Args:
            db_name (str): The name of the database file.
        """
        try:
            with DatabaseConnection(db_name) as connection:
                cursor = connection.cursor()  # Create a cursor object for executing SQL queries
                cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER, username TEXT UNIQUE, password TEXT)")  # Create players table if it does not exist
                cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, player_id INTEGER, nodes INTEGER, result TEXT)")
            print(f"Error initializing database: {e}")  # Print an error message if initialization fails

    def register_player(name, initial_balance, db_name):
        """
    Register a new player in the database.
    Args:
        name (str): The name of the player.
        initial_balance (int): The initial balance of the player.
        db_name (str): The name of the database file.
    """
    try:
        with DatabaseConnection(db_name) as connection:
            cursor = connection.cursor()  # Create a cursor object for executing SQL queries
            cursor.execute("INSERT INTO players (name, balance) VALUES (?, ?)", (name, initial_balance))  # Insert player data into players table
    except sqlite3.Error as e:
        print(f"Error registering player: {e}")  # Print an error message if registration fails
        
    def log_game(player_id, nodes, result, db_name):
        """
        Log a game played by a player in the database.
    Args:
        player_id (int): The ID of the player.
        nodes (int): The number of nodes in the game.
        result (str): The result of the game (win/loss).
        db_name (str): The name of the database file.
    """
    try:
        with DatabaseConnection(db_name) as connection:
            cursor = connection.cursor()  # Create a cursor object for executing SQL queries
            cursor.execute("INSERT INTO games (player_id, nodes, result) VALUES (?, ?, ?)", (player_id, nodes, result))  # Insert game data into games table
    except sqlite3.Error as e:
        print(f"Error logging game: {e}")  # Print an error message if logging fails
