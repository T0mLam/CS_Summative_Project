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
            cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")  # Create players table if it does not exist
            cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, player_id INTEGER, nodes INTEGER, result TEXT)")
        print(f"Error initializing database: {e}")  # Print an error message if initialization fails


    
def register_player(name, initial_balance, db_name):
    
def log_game(player_id, nodes, result, db_name):
    