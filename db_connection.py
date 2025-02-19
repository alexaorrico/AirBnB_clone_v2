from sqlalchemy import create_engine

# Replace these values with your actual database connection details
DB_USER = 'hbnb_dev'
DB_PASSWORD = 'hbnb_dev_pwd'
DB_HOST = 'localhost'
DB_PORT = '3306'  # Default MySQL port
DB_NAME = 'hbnb_dev_db'

# Create the database URL
db_url = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    # Create an engine and attempt to connect
    engine = create_engine(db_url)
    connection = engine.connect()

    # If connection successful, print a success message
    print("Database connection successful!")

    # Execute a test query to further verify the connection
    result = connection.execute("SELECT 1")
    print("Test query result:", result.fetchone()[0])

    # Close the connection
    connection.close()
except Exception as e:
    # If connection fails, print an error message
    print("Error connecting to the database:", e)

