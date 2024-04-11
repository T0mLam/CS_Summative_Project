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
    
def register_player(name, initial_balance, db_name):
    
def log_game(player_id, nodes, result, db_name):
    