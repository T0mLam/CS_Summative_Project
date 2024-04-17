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
            return self.connection
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


def initialize_database():
    """Initialize the database with necessary tables."""
    try:
        with DatabaseConnection('db') as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, balance INTEGER, username TEXT UNIQUE, password TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, player_id INTEGER, nodes INTEGER, result TEXT)")
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")


def register_player(username, password, initial_balance):
    """Register a new player in the database."""
    try:
        with DatabaseConnection('db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO players (balance, username, password) VALUES (?, ?, ?)", (initial_balance, username, password))
        print("Player registered successfully.")
    except sqlite3.Error as e:
        print(f"Error registering player: {e}")
    

def log_game(player_id, nodes, result):
    """Log a game played by a player in the database."""
    try:
        with DatabaseConnection('db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO games (player_id, nodes, result) VALUES (?, ?, ?)", (player_id, nodes, result))
        print("Game logged successfully.")
    except sqlite3.Error as e:
        print(f"Error logging game: {e}")


def authenticate(username, password):
    """Authenticate the user based on provided username and password."""
    try:
        with DatabaseConnection('db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT username, balance FROM players WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
        if user:
            print("Authentication successful.")
            return user
        else:
            print("Invalid username or password.")
            return False
    except sqlite3.Error as e:
        print(f"Error authenticating user: {e}")
        return False
    
def update_balance(username, new_balance):
    """Update the balance of a player."""
    try:
        with DatabaseConnection('db') as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE players SET balance = ? WHERE username = ?", (new_balance, username))
        print("Balance updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating balance: {e}")



if __name__ == '__main__':
    pass