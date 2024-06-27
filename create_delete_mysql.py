"""  create or delete a mysql database"""
import sys
from sqlalchemy import create_engine, text

# Check if the action and database name are provided as arguments
if len(sys.argv) != 3:
    print("Usage: python3 script_name.py <action> <dbname>")
    print("Actions: create, delete")
    sys.exit(1)

# Get the action and database name from the command-line arguments
action = sys.argv[1]
dbname = sys.argv[2]

# Database connection URI
# Replace 'sqluser', 'password', and 'localhost' with your MySQL credentials
SQLALCHEMY_DATABASE_URI = 'mysql://sqluser:password@localhost/mysql'

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Perform the specified action on the database
try:
    with engine.connect() as connection:
        if action == 'create':
            sql_statement = text(f"CREATE DATABASE IF NOT EXISTS {dbname}")
            connection.execute(sql_statement)
            print(f"Database '{dbname}' has been successfully created.")
        elif action == 'delete':
            sql_statement = text(f"DROP DATABASE IF EXISTS {dbname}")
            connection.execute(sql_statement)
            print(f"Database '{dbname}' has been successfully deleted.")
        else:
            print("Invalid action. Use 'create' or 'delete'.")
except Exception as e:
    print(f"An error occurred: {e}")
