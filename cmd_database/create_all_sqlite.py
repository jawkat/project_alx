""" create the database """
import sys
import os
from sqlalchemy import create_engine, text

# Check if the action and database name are provided as arguments
if len(sys.argv) != 3:
    print("Usage: python3 script_name.py <action> <dbname>")
    print("Actions: create, delete")
    sys.exit(1)

# Get the action and database name from the command-line arguments
action = sys.argv[1]
dbname = sys.argv[2]

# Database file path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, dbname + '.db')

# Database connection URI for SQLite
SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Perform the specified action on the database
try:
    if action == 'create':
        # Connecting to the database file creates it if it doesn't exist
        with engine.connect() as connection:
            print(f"Database '{dbname}' has been successfully created at {db_path}.")
    elif action == 'delete':
        # Delete the database file if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Database '{dbname}' has been successfully deleted.")
        else:
            print(f"Database '{dbname}' does not exist.")
    else:
        print("Invalid action. Use 'create' or 'delete'.")
except Exception as e:
    print(f"An error occurred: {e}")
