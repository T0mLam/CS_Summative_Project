import sqlite3
import os

class DatabaseConnection:
    """A context manager class for handling database connections."""
    
    def __init__(self, db_name):
        """Initialize the DatabaseConnection object."""
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Enter method for the context manager."""
        try:
            self.connection = sqlite3.connect(os.path.dirname(__file__) + '/' + self.db_name)
            return self
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
       
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method for the context manager."""
        if self.connection:
            try:
                self.connection.commit()
            except sqlite3.Error as e:
                print(f"Error committing changes to database: {e}")
            finally:
                self.connection.close()

    def get_cursor(self):
        """Return the cursor for executing database commands."""
        return self.connection.cursor()

    def initialize_database(self):
        """Initialize the database with necessary tables."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER, username TEXT UNIQUE, password TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, player_id INTEGER, nodes INTEGER, result TEXT)")
            print("Database initialized successfully.")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def register_player(self, name, initial_balance):
        """Register a new player in the database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO players (name, balance) VALUES (?, ?)", (name, initial_balance))
            print("Player registered successfully.")
        except sqlite3.Error as e:
            print(f"Error registering player: {e}")
        
    def log_game(self, player_id, nodes, result):
        """Log a game played by a player in the database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO games (player_id, nodes, result) VALUES (?, ?, ?)", (player_id, nodes, result))
            print("Game logged successfully.")
        except sqlite3.Error as e:
            print(f"Error logging game: {e}")

    def authenticate(self, username, password):
        """Authenticate the user based on provided username and password."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM players WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                print("Authentication successful.")
                return True
            else:
                print("Invalid username or password.")
                return False
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return False


if __name__ == '__main__':
    with DatabaseConnection('db') as conn:
        conn.initialize_database()
        conn.register_player('Tom', 10)